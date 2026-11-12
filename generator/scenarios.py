"""Catálogo de cenários injetados (famílias P, B, L, N — D-06/D-16).

STATUS: catálogo PROVISÓRIO (P18-P23 abertas, dono: Yasmin). Foi desenhado a partir da spec e da
arquitetura, SEM consultar a fórmula da D3, mas precisa de ratificação para valer como desenho cego.
Cada cenário é uma função independente: trocar/adicionar um é editar CATALOG no fim do arquivo.
O rótulo nunca entra em `corp`: só em ground_truth (episodes + event_labels).
"""

import numpy as np

from . import config as cfg
from .core import Body
from .normal import _t, pick_res
from .world import rand_ip

E = cfg.E


class X:
    def __init__(self, world, sink, rng):
        self.W, self.S, self.rng = world, sink, rng

    # ---- seleção -----------------------------------------------------------------------
    def pick(self, pred, fallback=None):
        c = [
            e
            for e in self.W.emps
            if pred(e) and e.works[self.W.eval_start :].sum() > 40
        ]
        if not c and fallback:
            c = [
                e
                for e in self.W.emps
                if fallback(e) and e.works[self.W.eval_start :].sum() > 40
            ]
        return c[int(self.rng.integers(len(c)))]

    def day(self, e):
        w = np.flatnonzero(e.works[self.W.eval_start :]) + self.W.eval_start
        return int(w[int(self.rng.integers(len(w)))])

    def run(self, e, length):
        w = np.flatnonzero(e.works[self.W.eval_start :]) + self.W.eval_start
        s = int(self.rng.integers(0, max(1, len(w) - length)))
        return [int(i) for i in w[s : s + length]]

    def ep(self, fam, code, e, desc, mal):
        return self.S.episode(fam, code, e.id, desc, mal)

    # ---- origem ------------------------------------------------------------------------
    def office(self, e):
        return e.office_ip, False

    def home_vpn(self, e):
        return self.S.vpn_ip(), True

    def home(self, e):
        return e.home_ip, False

    def atk(self):
        return rand_ip(self.W, self.rng, int(self.rng.choice(self.W.r_ext_for))), False

    def ext_dom(self):
        return rand_ip(self.W, self.rng, int(self.rng.choice(self.W.r_ext_dom))), False

    def reenable(self, e, di_end):
        """Reativação do MFA por TI (remediação; sem rótulo). Devolve o epoch do fim da janela."""
        world = self.W
        if di_end >= world.ndays:
            return int(world.day_epoch[-1] + 86400)
        adm = self.pick(lambda a: a.persona == "it_privileged")
        bd = Body()
        bd.add(60, E["SYSTEM_CONFIG"], 0, cfg.SUB["mfa_enabled"], 1, e.id)
        self.sess(adm, 11.0, di_end, 300, bd, self.office(adm), -1)
        return _t(world, e, di_end, 11.0)

    def mfa(self, e, t):
        from .world import mfa_at

        return mfa_at(self.W, e, t)

    # ---- construtores de corpo ---------------------------------------------------------
    def accesses(self, bd, ids, t0, t1, edit_p=0.2):
        ts = np.sort(self.rng.uniform(t0, t1, len(ids)))
        for dt, r in zip(ts, ids, strict=True):
            bd.add(dt, E["FILE_ACCESS"], r, int(self.rng.random() < edit_p))

    def download(self, bd, dt, res, size, dest):
        bd.add(dt, E["FILE_DOWNLOAD"], res, int(size), dest)

    def top_sens(self, e, n, min_sens=0):
        a = e.allowed[self.W.res_sens[e.allowed] >= min_sens]
        if len(a) == 0:
            a = e.allowed
        s = self.W.res_sens[a]
        w = np.exp(1.5 * s)
        w = w / w.sum()
        return self.rng.choice(a, size=n, p=w)

    def sess(self, e, hour, di, duration, bd, origin, ep, dev=None, **kw):
        t = _t(self.W, e, di, hour)
        ip, vpn = origin
        return self.S.session(
            e.id,
            t,
            duration,
            bd.arrays() if isinstance(bd, Body) else bd,
            ip,
            vpn,
            e.dev_nb if dev is None else dev,
            kw.pop("mfa", self.mfa(e, t)),
            ep,
            **kw,
        )


# =========================================================================== P — pontuais (D1)
def p01_forca_bruta(x):
    r, e = (
        x.rng,
        x.pick(
            lambda e: e.persona != "it_privileged" and not e.mfa0,
            lambda e: e.persona != "it_privileged",
        ),
    )
    di = x.day(e)
    n = int(r.integers(15, 41))
    ep = x.ep(
        "P",
        "P01_forca_bruta",
        e,
        f"{n} tentativas em <2 min de faixa externa; sucesso após o lockout",
        True,
    )
    bd = Body()
    x.accesses(bd, x.top_sens(e, int(r.integers(8, 21)), 2), 5, 900)
    x.sess(
        e,
        r.choice([0, 1, 2, 3, 4]) + r.random(),
        di,
        1200,
        bd,
        x.atk(),
        ep,
        dev=0,
        mfa=False,
        n_wrong=n,
        gap=(0.5, 3),
        wait=(1500, 2100),
    )


def p02_download_restrito_removivel(x):
    r = x.rng
    e = x.pick(
        lambda e: e.dept in ("hr", "board") and e.persona in ("day_admin", "management")
    )
    di = x.day(e)
    ep = x.ep(
        "P",
        "P02_download_restrito_removivel",
        e,
        "download de recursos restritos para dispositivo removível",
        True,
    )
    bd = Body()
    res = x.top_sens(e, int(r.integers(8, 16)), 3)
    ts = np.sort(r.uniform(60, 1500, len(res)))
    for dt, rr in zip(ts, res, strict=True):
        x.download(bd, dt, rr, r.uniform(5e7, 4e8), 2)
    bd.add(
        1600,
        E["EXTERNAL_DEVICE"],
        0,
        0,
        int(r.integers(80, 300)),
        int(r.uniform(3e8, 2e9)),
    )
    x.sess(e, r.uniform(14, 17), di, 1900, bd, x.office(e), ep)


def p03_escalada_privilegio_noite(x):
    r, e = x.rng, x.pick(lambda e: e.persona != "it_privileged" and e.mfa0)
    di = x.day(e)
    ep = x.ep(
        "P",
        "P03_escalada_privilegio_noite",
        e,
        "conta comum escala privilégio, desliga MFA e acessa console",
        True,
    )
    bd = Body()
    sub = cfg.SUB
    bd.add(30, E["SYSTEM_CONFIG"], 0, sub["privilege_escalation"], 0, 0)
    bd.add(90, E["SYSTEM_CONFIG"], 0, sub["permission_grant"], 0, 0)
    bd.add(150, E["SYSTEM_CONFIG"], 0, sub["mfa_disabled"], 0, 0)
    for k, rr in enumerate(r.choice(x.W.sys_ids["console"], 4, replace=False)):
        bd.add(300 + 60 * k, E["FILE_ACCESS"], rr)
    h = r.uniform(1, 4)
    t = _t(x.W, e, di, h)
    x.W.mfa_off.setdefault(e.id, []).append((t + 150, x.reenable(e, di + 10)))
    x.sess(e, h, di, 900, bd, x.home_vpn(e), ep)


def p04_externo_sem_vpn_sem_mfa(x):
    r, e = (
        x.rng,
        x.pick(
            lambda e: e.persona != "it_privileged" and not e.mfa0,
            lambda e: e.persona != "it_privileged",
        ),
    )
    di = x.day(e)
    ep = x.ep(
        "P",
        "P04_externo_sem_vpn_sem_mfa",
        e,
        "logon de faixa externa estrangeira, sem VPN e sem MFA, madrugada",
        True,
    )
    bd = Body()
    x.accesses(bd, x.top_sens(e, int(r.integers(6, 13)), 3), 10, 700)
    x.download(bd, 800, x.top_sens(e, 1, 3)[0], r.uniform(2e7, 1e8), 0)
    x.sess(e, r.uniform(2, 4.5), di, 1000, bd, x.atk(), ep, dev=0, mfa=False)


def p05_nuvem_exfiltracao_rapida(x):
    r = x.rng
    e = x.pick(
        lambda e: e.dept in ("admin_finance", "legal", "sales", "engineering_product")
    )
    di = x.day(e)
    ep = x.ep(
        "P",
        "P05_nuvem_exfiltracao_rapida",
        e,
        "navegação em armazenamento em nuvem + downloads para storage externo",
        True,
    )
    bd = Body()
    for k, d in enumerate(r.choice(cfg.CLOUD_IDX, 3)):
        bd.add(20 + 25 * k, E["WEB_BROWSING"], 0, d)
    res = x.top_sens(e, 10, 2)
    for k, rr in enumerate(res):
        x.download(bd, 120 + 40 * k, rr, r.uniform(2e7, 2e8), 1)
    x.sess(e, r.uniform(10, 16), di, 700, bd, x.office(e), ep)


def p06_conta_comum_altera_permissoes(x):
    r, e = x.rng, x.pick(lambda e: e.persona != "it_privileged")
    di = x.day(e)
    ep = x.ep(
        "P",
        "P06_conta_comum_altera_permissoes",
        e,
        "conta comum tenta mudar permissões à noite (bloqueado)",
        True,
    )
    bd = Body()
    sub = cfg.SUB
    bd.add(20, E["SYSTEM_CONFIG"], 0, sub["privilege_escalation"], 0, 0, 2)
    for k in range(3):
        bd.add(
            60 + 40 * k,
            E["SYSTEM_CONFIG"],
            0,
            sub["permission_grant"],
            0,
            int(r.choice(x.W.all_ids)),
            2,
        )
    bd.add(
        240,
        E["SYSTEM_CONFIG"],
        0,
        sub["permission_grant"],
        0,
        int(r.choice(x.W.all_ids)),
        1,
    )
    x.sess(e, r.uniform(22.3, 23.5), di, 400, bd, x.office(e), ep)


# =========================================================================== B — de contexto (D2)
def b01_volume_atipico(x):
    r = x.rng
    e = x.pick(lambda e: e.persona in ("day_admin", "sales_traveler", "management"))
    di = x.day(e)
    ep = x.ep(
        "B",
        "B01_volume_atipico",
        e,
        "volume ~5x o habitual, no horário, de dentro do escritório, sem recurso sensível",
        True,
    )
    n = int(e.mu * 4)
    ids = pick_res(x.W, r, e, n)
    ids = ids[x.W.res_sens[ids] <= 1]
    bd = Body()
    x.accesses(bd, ids, 5, 3 * 3600)
    x.sess(e, 10.0, di, 3 * 3600 + 60, bd, x.office(e), ep)


def b02_recurso_novo(x):
    r = x.rng
    e = x.pick(
        lambda e: (
            e.persona in ("hybrid_eng", "it_privileged", "sales_traveler", "shift_ops")
        )
    )
    di = x.day(e)
    ep = x.ep(
        "B",
        "B02_recurso_novo",
        e,
        "varredura de recursos permitidos que a pessoa nunca tocou (sigilo baixo)",
        True,
    )
    pool = np.array(
        [i for i in e.allowed if i not in set(e.hab_ids) and x.W.res_sens[i] <= 1]
    )
    ids = r.choice(pool, size=min(len(pool), int(r.integers(25, 41))), replace=False)
    bd = Body()
    x.accesses(bd, ids, 5, 2400)
    x.sess(e, r.uniform(10, 15), di, 2500, bd, x.office(e), ep)


def b03_horario_atipico_individual(x):
    r = x.rng
    e = x.pick(lambda e: e.persona == "day_admin" and e.site == "SP")
    di = x.day(e)
    ep = x.ep(
        "B",
        "B03_horario_atipico_individual",
        e,
        "sessão 20h-22h do escritório, fora do hábito da pessoa (dentro do corte fixo da C0)",
        True,
    )
    n = int(r.integers(8, 16))
    bd = Body()
    x.accesses(bd, pick_res(x.W, r, e, n), 5, 6000)
    x.sess(e, 20.1, di, 6100, bd, x.office(e), ep)


def b04_origem_nova(x):
    r = x.rng
    e = x.pick(lambda e: e.persona in ("day_admin", "it_privileged"))
    di = x.day(e)
    ep = x.ep(
        "B",
        "B04_origem_nova",
        e,
        "origem externa doméstica inédita, sem viagem declarada, no horário",
        True,
    )
    n = int(r.integers(8, 16))
    bd = Body()
    x.accesses(bd, pick_res(x.W, r, e, n), 5, 3000)
    x.sess(e, r.uniform(10, 16), di, 3100, bd, x.ext_dom(), ep)


# =========================================================================== L — longitudinais (D3)
def l01_exfiltracao_gradual(x):
    r = x.rng
    e = x.pick(
        lambda e: e.dept in ("admin_finance", "legal", "sales", "engineering_product")
    )
    days = x.run(e, 21)
    ep = x.ep(
        "L",
        "L01_exfiltracao_gradual",
        e,
        "21 dias de downloads crescentes e migração para storage externo; nenhum dia notável",
        True,
    )
    for k, di in enumerate(days):
        bd = Body()
        nd = 1 + min(3, int(k * 0.15))
        ids = x.top_sens(e, nd, 1 if k > 5 else 0)
        for j, rr in enumerate(ids):
            dest = 1 if r.random() < 0.1 + 0.4 * k / 21 else 0
            x.download(bd, 60 + 120 * j, rr, np.exp(r.normal(np.log(8e6), 0.5)), dest)
        bd.add(30, E["WEB_BROWSING"], 0, int(r.choice(cfg.CLOUD_IDX)))
        x.accesses(bd, pick_res(x.W, r, e, 3), 200, 900)
        x.sess(
            e,
            r.uniform(14, 16),
            di,
            1200,
            bd,
            x.office(e) if r.random() < 0.6 else x.home_vpn(e),
            ep,
        )


def l02_reconhecimento_lateral(x):
    r = x.rng
    e = x.pick(
        lambda e: (
            e.persona in ("day_admin", "hybrid_eng", "sales_traveler", "it_privileged")
        )
    )
    days = x.run(e, 20)
    ep = x.ep(
        "L",
        "L02_reconhecimento_lateral",
        e,
        "20 dias ampliando recursos novos, do baixo ao alto sigilo",
        True,
    )
    pool = np.array([i for i in e.allowed if i not in set(e.hab_ids)])
    if len(pool) < 10:
        pool = e.allowed
    for k, di in enumerate(days):
        n = 2 + int(k * 0.35)
        w = np.exp((0.4 + 1.6 * k / 20) * x.W.res_sens[pool])
        w /= w.sum()
        ids = r.choice(pool, size=min(n, len(pool)), replace=False, p=w)
        bd = Body()
        x.accesses(bd, ids, 30, 900)
        x.sess(e, r.uniform(10, 16), di, 1000, bd, x.office(e), ep)


def l03_postura_degradando(x):
    r = x.rng
    e = x.pick(lambda e: e.mfa0 and e.persona != "it_privileged")
    days = x.run(e, 21)
    ep = x.ep(
        "L",
        "L03_postura_degradando",
        e,
        "MFA desligado, patch parado, cópia física recorrente e clique em phishing",
        True,
    )
    di0 = days[0]
    t0 = _t(x.W, e, di0, 21.0)
    x.W.mfa_off.setdefault(e.id, []).append((t0 + 30, x.reenable(e, di0 + 30)))
    x.W.dev_nopatch[e.dev_nb] = di0
    x.W.phish_force[(e.id, int(x.W.yyyymm[di0]))] = 2
    bd = Body()
    bd.add(30, E["SYSTEM_CONFIG"], 0, cfg.SUB["mfa_disabled"], 0, 0)
    x.sess(e, 21.0, di0, 300, bd, x.home_vpn(e), ep)
    for k, di in enumerate(days):
        if k % 3 == 1:
            bd = Body()
            bd.add(
                120,
                E["EXTERNAL_DEVICE"],
                0,
                0,
                int(r.integers(5, 41)),
                int(r.uniform(5e6, 6e7)),
            )
            x.sess(e, r.uniform(10, 16), di, 600, bd, x.office(e), ep)


def l04_horario_deslizante(x):
    r = x.rng
    e = x.pick(lambda e: e.persona in ("day_admin", "hybrid_eng", "management"))
    days = x.run(e, 20)
    ep = x.ep(
        "L",
        "L04_horario_deslizante",
        e,
        "20 dias com sessão noturna remota deslizando de 19h para 2h",
        True,
    )
    for k, di in enumerate(days):
        bd = Body()
        x.accesses(bd, pick_res(x.W, r, e, int(r.integers(6, 11))), 20, 3000)
        x.sess(e, 19.0 + 0.35 * k, di, 3300, bd, x.home_vpn(e), ep)


# =========================================================================== N — controle negativo
def n01_escalada_legitima(x):
    r = x.rng
    e = x.pick(
        lambda e: e.persona in ("day_admin", "hybrid_eng") and e.dept != "it_infra"
    )
    days = x.run(e, 21)
    di0 = days[0]
    ep = x.ep(
        "N",
        "N01_escalada_legitima",
        e,
        "mudança de projeto: acesso a mais recursos, faixa horária e volume maiores, sem conduta indevida",
        False,
    )
    x.W.hr_extra.append((e.id, "role_change", di0, di0))
    adm = x.pick(lambda a: a.persona == "it_privileged")
    bd = Body()
    bd.add(60, E["SYSTEM_CONFIG"], 0, cfg.SUB["permission_grant"], 1, e.id)
    x.sess(adm, 11.0, di0, 300, bd, x.office(adm), ep)
    sysk = "crm" if e.dept != "sales" else "repo"
    newp = np.array(x.W.sys_ids[sysk] + x.W.sys_ids["portal"])
    for k, di in enumerate(days):
        n = 3 + int(k * 0.6)
        use_new = r.random(n) < 0.6
        ids = np.where(use_new, r.choice(newp, n), pick_res(x.W, r, e, n))
        bd = Body()
        x.accesses(bd, ids, 30, 1800)
        x.sess(e, r.uniform(10, 15), di, 1900, bd, x.office(e), ep)
        if r.random() < 0.4:
            bd = Body()
            x.accesses(bd, pick_res(x.W, r, e, int(r.integers(5, 11))), 30, 3000)
            x.sess(e, 19.0, di, 3100, bd, x.home_vpn(e), ep)


def n02_troca_de_aparelho(x):
    e = x.pick(lambda e: e.mfa0)
    di = x.day(e)
    ep = x.ep(
        "N",
        "N02_troca_de_aparelho",
        e,
        "MFA desligado e religado na troca de aparelho, mesma noite",
        False,
    )
    h = 18.0
    t = _t(x.W, e, di, h)
    x.W.mfa_off.setdefault(e.id, []).append((t + 30, t + 7000))
    bd = Body()
    bd.add(30, E["SYSTEM_CONFIG"], 0, cfg.SUB["mfa_disabled"], 0, 0)
    x.accesses(bd, [x.W.mail_id] * 3, 60, 3000)
    bd.add(7000, E["SYSTEM_CONFIG"], 0, cfg.SUB["mfa_enabled"], 0, 0)
    x.sess(e, h, di, 7100, bd, x.home_vpn(e), ep)


def n03_pico_fim_de_mes(x):
    r = x.rng
    e = x.pick(lambda e: e.dept == "admin_finance")
    cand = [i for i in np.flatnonzero(x.W.month_end & e.works) if i >= x.W.eval_start]
    di = int(r.choice(cand))
    ep = x.ep(
        "N",
        "N03_pico_fim_de_mes",
        e,
        "fechamento do mês: volume ~2x e expediente até 21h30, legítimo",
        False,
    )
    bd = Body()
    x.accesses(bd, pick_res(x.W, r, e, int(e.mu * 1.2)), 10, 3 * 3600)
    x.sess(e, 9.0, di, 3 * 3600 + 60, bd, x.office(e), ep)
    bd = Body()
    x.accesses(bd, pick_res(x.W, r, e, int(e.mu * 0.4)), 10, 9000)
    x.sess(e, 19.0, di, 9100, bd, x.office(e), ep)


def n04_erro_humano_lockout(x):
    e = x.pick(lambda e: e.persona != "shift_ops")
    days = x.run(e, 2)
    ep = x.ep(
        "N",
        "N04_erro_humano_lockout",
        e,
        "troca de senha seguida de lockout por erro de digitação (celular antigo)",
        False,
    )
    bd = Body()
    bd.add(40, E["SYSTEM_CONFIG"], 0, cfg.SUB["password_change"], 0, 0)
    x.sess(e, 18.5, days[0], 120, bd, x.home_vpn(e), ep)
    bd = Body()
    x.accesses(bd, [x.W.mail_id] * 3, 20, 400)
    x.sess(e, 18.5, days[1], 500, bd, x.home(e), ep, n_wrong=6)


def n05_download_grande_legitimo(x):
    r = x.rng
    e = x.pick(lambda e: e.dept in ("engineering_product", "admin_finance", "legal"))
    di = x.day(e)
    ep = x.ep(
        "N",
        "N05_download_grande_legitimo",
        e,
        "entrega de projeto: 1-2 arquivos de 300-900 MB para disco local",
        False,
    )
    bd = Body()
    for k in range(int(r.integers(1, 3))):
        x.download(bd, 120 + 200 * k, pick_res(x.W, r, e, 1)[0], r.uniform(3e8, 9e8), 0)
    x.sess(e, r.uniform(14, 16), di, 1200, bd, x.office(e), ep)


CATALOG = [  # (código, família, função, execuções por semente)
    ("P01", "P", p01_forca_bruta, 4),
    ("P02", "P", p02_download_restrito_removivel, 4),
    ("P03", "P", p03_escalada_privilegio_noite, 4),
    ("P04", "P", p04_externo_sem_vpn_sem_mfa, 4),
    ("P05", "P", p05_nuvem_exfiltracao_rapida, 4),
    ("P06", "P", p06_conta_comum_altera_permissoes, 4),
    ("B01", "B", b01_volume_atipico, 4),
    ("B02", "B", b02_recurso_novo, 4),
    ("B03", "B", b03_horario_atipico_individual, 4),
    ("B04", "B", b04_origem_nova, 4),
    ("L01", "L", l01_exfiltracao_gradual, 3),
    ("L02", "L", l02_reconhecimento_lateral, 3),
    ("L03", "L", l03_postura_degradando, 3),
    ("L04", "L", l04_horario_deslizante, 3),
    ("N01", "N", n01_escalada_legitima, 3),
    ("N02", "N", n02_troca_de_aparelho, 4),
    ("N03", "N", n03_pico_fim_de_mes, 4),
    ("N04", "N", n04_erro_humano_lockout, 4),
    ("N05", "N", n05_download_grande_legitimo, 4),
]


def inject(world, sink, rng, scale=1):
    x = X(world, sink, rng)
    for _code, _fam, fn, n in CATALOG:
        for _ in range(max(1, round(n * scale))):
            fn(x)
