"""Tráfego legítimo: rotina por persona, calendário (D-27), ruído legítimo e estado diário."""
import numpy as np
from . import config as C
from .core import Body
from .world import mfa_at, rand_ip

TYPE_MAP = np.array([C.E['FILE_ACCESS'], C.E['FILE_DOWNLOAD'], C.E['WEB_BROWSING'],
                     C.E['EXTERNAL_DEVICE'], C.E['SYSTEM_CONFIG']])
MIXN = {k: np.array(v) / sum(v) for k, v in C.MIX.items()}
DOM_P = np.array(C.DOMAIN_P) / sum(C.DOMAIN_P)
PH_BASE = np.array([.25, .55, .15, .05])


def pick_res(W, rng, e, k):
    r = e.hab_ids[rng.choice(len(e.hab_ids), size=k, p=e.hab_p)]
    nov = rng.random(k) < .03                       # novidade legítima: recurso permitido, fora do hábito
    if nov.any():
        r = np.where(nov, rng.choice(e.allowed, size=k), r)
    return r.astype(np.int64)


def body_random(W, rng, e, n, D, lunch_off=None, extra=()):
    D = int(D)
    z = np.zeros(n, np.int64)
    if n > 0:
        if lunch_off is not None and 1800 < lunch_off < D - 3600 - 1800:
            raw = rng.uniform(1, D - 3601, n)
            raw = np.where(raw >= lunch_off, raw + 3600, raw)
        else:
            raw = rng.uniform(1, max(D - 1, 2), n)
        dt = raw.astype(np.int64)
        typ = rng.choice(5, size=n, p=MIXN[e.persona])
        et = TYPE_MAP[typ]
        res, a1, a2, a3 = z.copy(), z.copy(), z.copy(), z.copy()
        fa, fd, wb, ex, sy = (typ == i for i in range(5))
        k = fa | fd
        res[k] = pick_res(W, rng, e, int(k.sum()))
        a1[fa] = (rng.random(int(fa.sum())) < .25).astype(np.int64)                 # edit
        m = int(fd.sum())
        if m:
            sens = W.res_sens[res[fd]]
            a1[fd] = np.clip(np.exp(rng.normal(np.log(1.2e6) + .35 * sens, 1.0)), 2e3, 6e8).astype(np.int64)
            a2[fd] = rng.choice(3, size=m, p=[.955, .04, .005])
        a1[wb] = rng.choice(len(C.DOMAINS), size=int(wb.sum()), p=DOM_P)
        m = int(ex.sum())
        if m:
            a1[ex] = rng.choice(3, size=m, p=[.55, .15, .30])
            a2[ex] = 1 + rng.poisson(6, m)
            a3[ex] = a2[ex] * np.exp(rng.normal(np.log(1.5e6), .8, m)).astype(np.int64)
        m = int(sy.sum())
        if m:
            if e.persona == 'it_privileged':
                a1[sy] = rng.choice([C.SUB['password_change'], C.SUB['permission_grant']], size=m, p=[.35, .65])
                a2[sy] = 1
                a3[sy] = rng.choice(W.all_ids, size=m)
            else:
                a1[sy] = C.SUB['password_change']
        arr = [dt, et, res, a1, a2, a3, z.copy()]
    else:
        arr = [np.zeros(0, np.int64)] * 7
    if extra:
        ex_a = np.array(extra, dtype=np.int64)
        arr = [np.concatenate([arr[i], ex_a[:, i]]) for i in range(7)]
        o = np.argsort(arr[0], kind='stable')
        arr = [a[o] for a in arr]
    return arr


def body_mobile(rng, e, n, D):
    dt = np.sort(rng.uniform(1, max(D - 1, 2), n)).astype(np.int64)
    z = np.zeros(n, np.int64)
    return [dt, np.full(n, C.E['FILE_ACCESS'], np.int64), rng.choice(e.mob_ids, n).astype(np.int64), z, z, z, z]


def _origin(W, S, rng, e, kind, vpn):
    if vpn:
        return S.vpn_ip(), True
    if kind == 'office':
        return e.office_ip, False
    if kind == 'home':
        return e.home_ip, False
    return rand_ip(W, rng, int(rng.choice(W.r_ext_dom))), False


def _t(W, e, di, hour):
    """hora local (float) do dia di -> epoch UTC (D-27/D-40: tz por funcionário)."""
    return int(W.day_epoch[di] + int(hour * 3600) - e.tz * 3600)


def simulate_normal(W, S, rng):
    W.all_ids = np.array([e.id for e in W.emps])
    for e in W.emps:
        p = C.PERSONAS[e.persona]
        pend = []
        for di in range(W.ndays):
            if di < e.hire_idx or e.sick[di]:
                continue
            if di in e.phish:
                pend.append(e.phish[di])
            wd = int(W.wd[di])

            if not e.works[di]:                                           # residual declarado (D-27)
                if e.vac[di]: pr = C.RESIDUAL_P['vacation']
                elif e.persona == 'management': pr = C.RESIDUAL_P_MGMT
                elif e.persona == 'shift_ops': pr = .03
                elif W.is_hol[di]: pr = C.RESIDUAL_P['holiday']
                else: pr = C.RESIDUAL_P['weekend']
                if rng.random() < pr:
                    hs = rng.uniform(9, 20); vpn = rng.random() < .5
                    ip, vpn = _origin(W, S, rng, e, 'home', vpn)
                    t0 = _t(W, e, di, hs)
                    D = rng.uniform(600, 2700)
                    S.session(e.id, t0, D, body_mobile(rng, e, int(rng.integers(3, 9)), D), ip, vpn,
                              e.dev_nb, mfa_at(W, e, t0))
                continue

            mu = e.mu * (1.45 if (e.persona == 'sales_traveler' and W.month_end[di]) else 1.0)
            if e.dept == 'admin_finance' and W.month_end[di]: mu *= 1.3
            n_tot = max(10, int(rng.lognormal(np.log(mu) - .5 * .22 ** 2, .22)))

            # horário (hora local) -----------------------------------------------------------
            if e.persona == 'shift_ops':
                hs = {0: 6.0, 1: 14.0, 2: 22.0}[e.shift] + rng.normal(0, .15)
                span = rng.normal(8.0, .15)
            else:
                hs = float(np.clip(rng.normal(p['start'] + e.bias, .4), 5.5, 11.5))
                span = rng.normal(9.3, .8) if e.persona == 'management' else rng.normal(p['span'] - .4, .6)
                if e.dept == 'operations_support' and e.site == 'MAO' and rng.random() < .2:
                    span = rng.uniform(21.0, 21.8) - hs                      # D-40: encerra 21:30 em Manaus
                span = max(span, 4.0)
            # local de acesso ----------------------------------------------------------------
            kind, vpn, r = 'office', False, rng.random()
            if e.persona == 'hybrid_eng' and wd in e.home_days:
                kind, vpn = 'home', rng.random() < .6
            elif e.persona == 'sales_traveler':
                if r < .30: kind, vpn = 'external', rng.random() < .55
                elif r < .45: kind, vpn = 'home', rng.random() < .5
            elif e.persona == 'it_privileged' and r < .2:
                kind, vpn = 'home', rng.random() < .8
            elif e.persona == 'management' and r < .08:
                kind, vpn = 'home', rng.random() < .7
            ip, vpn = _origin(W, S, rng, e, kind, vpn)

            # sessões extras (noite da gestão, celular) --------------------------------------
            extras, n_extra = [], 0
            if e.persona == 'management' and rng.random() < .30:
                n = int(rng.integers(6, 13)); n_extra += n + 2
                extras.append(('eve', 20 + rng.uniform(0, 1), rng.uniform(.7, 1.8) * 3600, n))
            if e.dev_ph and rng.random() < .35:
                n = int(rng.integers(3, 9)); n_extra += n + 2
                extras.append(('mob', 18.5 + rng.uniform(0, 3), rng.uniform(300, 1500), n))

            # sessão principal ---------------------------------------------------------------
            n_core = max(4, n_tot - 2 - n_extra)
            t0 = _t(W, e, di, hs)
            D = span * 3600
            extra_ev = []
            while pend:
                m = pend.pop(0)
                if (e.id, m) in W.phish_force: oc = W.phish_force[(e.id, m)]
                else:
                    pr = PH_BASE.copy(); pr[2:] *= e.susc; pr /= pr.sum()
                    oc = int(rng.choice(4, p=pr))
                extra_ev.append((int(rng.uniform(.1, .9) * D), C.E['PHISHING_SIM'], 0, m, oc, 0, 0))
            lunch = None if e.persona == 'shift_ops' else int((12.25 - hs) * 3600)
            body = body_random(W, rng, e, n_core, D, lunch, extra_ev)
            p1 = e.p_err * (1.6 if (wd == 0 or (di > 0 and e.vac[di - 1])) else 1.0)
            nw = 0
            while rng.random() < p1 and nw < 6:
                nw += 1; p1 = .30
            S.session(e.id, t0, D, body, ip, vpn, e.dev_nb, mfa_at(W, e, t0), n_wrong=nw)

            for kd, h, dd, n in extras:
                if kd == 'eve':
                    ip2, v2 = _origin(W, S, rng, e, 'home', rng.random() < .7)
                    tt = _t(W, e, di, h)
                    S.session(e.id, tt, dd, body_random(W, rng, e, n, dd), ip2, v2, e.dev_nb, mfa_at(W, e, tt))
                else:
                    ip2, v2 = _origin(W, S, rng, e, 'home', rng.random() < .2)
                    tt = _t(W, e, di, h)
                    S.session(e.id, tt, dd, body_mobile(rng, e, n, dd), ip2, v2, e.dev_ph, mfa_at(W, e, tt))

            # janela de manutenção noturna (N06) ---------------------------------------------
            if (e.id, di) in W.maint:
                ep = S.episode('N', 'N06_manutencao_noturna_ti', e.id, 'janela de manutenção noturna legítima (D-38)', False)
                n = int(rng.integers(60, 111)); Dm = rng.uniform(3.5, 4.5) * 3600
                bd = Body(); cons = W.sys_ids['console']
                for dt in np.sort(rng.uniform(1, Dm - 1, n)):
                    u = rng.random()
                    if u < .55: bd.add(dt, C.E['FILE_ACCESS'], rng.choice(cons))
                    elif u < .80: bd.add(dt, C.E['SYSTEM_CONFIG'], 0, C.SUB['permission_grant'], 1, int(rng.choice(W.all_ids)))
                    else: bd.add(dt, C.E['FILE_ACCESS'], pick_res(W, rng, e, 1)[0])
                vpn = rng.random() < .6
                ip2, v2 = _origin(W, S, rng, e, 'home' if vpn else 'office', vpn)
                tt = _t(W, e, di, 22.0)
                S.session(e.id, tt, Dm, bd.arrays(), ip2, v2, e.dev_nb, mfa_at(W, e, tt), ep=ep)


def device_states(W, rng):
    """Estado diário do notebook (seção 4): idade do patch e antivírus ativo."""
    dev, day, age_l, av_l = [], [], [], []
    n = W.ndays
    for e in W.emps:
        med = C.PATCH_MEDIAN.get(e.dept, C.PATCH_MEDIAN['default'])
        nop = W.dev_nopatch.get(e.dev_nb)
        age = int(rng.integers(0, 2 * med + 1))
        reset = rng.random(n) < 1.0 / (2 * med)
        av = rng.random(n) > .005
        ages = np.empty(n, np.int64)
        for di in range(n):
            if reset[di] and not (nop is not None and di >= nop):
                age = 0
            else:
                age += 1
            ages[di] = age
        dev.append(np.full(n, e.dev_nb)); day.append(np.arange(n)); age_l.append(ages); av_l.append(av)
    return (np.concatenate(dev), np.concatenate(day), np.concatenate(age_l), np.concatenate(av_l))
