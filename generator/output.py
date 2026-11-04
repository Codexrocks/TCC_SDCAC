"""Montagem dos eventos, tabelas de apoio, ground truth e escrita em disco."""
import gzip, os
import numpy as np
import pandas as pd
from . import config as C
from .world import ip_str

ET = np.array(C.ETYPES, dtype=object)
RS = np.array(C.RESULTS, dtype=object)
_LOGIN = np.array([f'{{"mfa_used":{"true" if m else "false"},"failure_reason":{("null" if not r else chr(34) + C.FAIL_REASONS[r] + chr(34))}}}'
                   for m in (0, 1) for r in range(5)], dtype=object)
_LOGOUT = np.array([f'{{"reason":"{r}"}}' for r in C.LOGOUT_REASONS], dtype=object)
_FA = np.array([f'{{"action":"{a}"}}' for a in C.ACTIONS], dtype=object)
_WEB = np.array([f'{{"domain":"{d}","category":"{c}"}}' for d, c in C.DOMAINS], dtype=object)


class Run:
    pass


def assemble(W, S, run_id, seed):
    R = Run(); R.W, R.run_id, R.seed = W, run_id, seed
    cols = [np.concatenate(c) for c in zip(*S.ch)]
    t, et, rs, rv, a1, a2, a3, seq, sid = cols
    s = {k: np.array(v) for k, v in S.s.items()}
    lo_w, hi_w = W.day_epoch[0] + 3 * 3600, W.day_epoch[-1] + 86400 + 3 * 3600      # janela simulada em UTC
    ok_s = (s['t0'] >= lo_w) & (s['t1'] < hi_w)                                    # sessão inteira dentro da janela
    remap = np.cumsum(ok_s) - 1
    keep = ok_s[sid]
    t, et, rs, rv, a1, a2, a3, seq, sid = [c[keep] for c in (t, et, rs, rv, a1, a2, a3, seq, sid)]
    sid = remap[sid]
    s = {k: v[ok_s] for k, v in s.items()}
    o = np.lexsort((seq, sid, t))
    R.t, R.et, R.rs, R.rv, R.a1, R.a2, R.a3, R.sid = [c[o] for c in (t, et, rs, rv, a1, a2, a3, sid)]
    R.s = s
    R.nS, R.N = len(s['emp']), len(R.t)
    rng = np.random.default_rng([seed, run_id, 5])
    b = rng.integers(0, 256, (R.nS, 16), dtype=np.uint8)
    b[:, 6] = (b[:, 6] & 0x0f) | 0x40; b[:, 8] = (b[:, 8] & 0x3f) | 0x80
    h = b.tobytes().hex()
    R.s_uuid = np.array([f'{h[i:i+8]}-{h[i+8:i+12]}-{h[i+12:i+16]}-{h[i+16:i+20]}-{h[i+20:i+32]}' for i in range(0, R.nS * 32, 32)], dtype=object)
    R.s_ipstr = np.array([ip_str(i) for i in s['ip']], dtype=object)
    R.lat = np.minimum(np.exp(rng.normal(np.log(2.0), .6, R.N)) + (rng.random(R.N) < .03) * rng.exponential(300, R.N), 3600).astype(np.int64) + 1
    R.eps = pd.DataFrame(S.eps, columns=['episode_id', 'family', 'scenario_code', 'employee_id', 'description', 'is_malicious'])
    R.eps['scenario_code'] = R.eps.scenario_code.str[:3]
    R.eps = R.eps[R.eps.episode_id.isin(np.unique(s['ep'][s['ep'] >= 0]))].reset_index(drop=True)
    return R


def _attrs(R, lo, hi):
    et, a1, a2, a3 = R.et[lo:hi], R.a1[lo:hi], R.a2[lo:hi], R.a3[lo:hi]
    out = np.empty(len(et), dtype=object)
    m = et == 0; out[m] = _LOGIN[a1[m] * 5 + a2[m]]
    m = et == 1; out[m] = _LOGOUT[a1[m]]
    m = et == 2; out[m] = _FA[a1[m]]
    m = et == 3; out[m] = ['{"size_bytes":%d,"destination":"%s"}' % (s, C.DESTS[d]) for s, d in zip(a1[m], a2[m])]
    m = et == 4; out[m] = ['{"device_type":"%s","files_copied_count":%d,"bytes_copied":%d}' % (C.DEVTYPES[d], f, b) for d, f, b in zip(a1[m], a2[m], a3[m])]
    m = et == 5; out[m] = _WEB[a1[m]]
    m = et == 6; out[m] = ['{"action_subtype":"%s","initiated_by":"%s","target_employee_id":%s}' % (C.SUBTYPES[a], C.INITIATORS[i], 'null' if not tg else tg) for a, i, tg in zip(a1[m], a2[m], a3[m])]
    m = et == 7; out[m] = ['{"campaign_id":"camp-%d","outcome":"%s"}' % (c, C.OUTCOMES[o]) for c, o in zip(a1[m], a2[m])]
    return out


def _uuids(n, rng):
    b = rng.integers(0, 256, (n, 16), dtype=np.uint8)
    b[:, 6] = (b[:, 6] & 0x0f) | 0x40; b[:, 8] = (b[:, 8] & 0x3f) | 0x80
    h = b.tobytes().hex()
    return [f'{h[i:i+8]}-{h[i+8:i+12]}-{h[i+12:i+16]}-{h[i+16:i+20]}-{h[i+20:i+32]}' for i in range(0, n * 32, 32)]


def _iso(t):
    return np.datetime_as_string(t.astype('datetime64[s]'), unit='s', timezone='UTC')


def write(R, out_dir, slice_n=250_000):
    W = R.W
    base = os.path.join(out_dir, f'run_{R.run_id:03d}')
    for d in ('corp', 'ground_truth'): os.makedirs(os.path.join(base, d), exist_ok=True)
    corp, gt = os.path.join(base, 'corp'), os.path.join(base, 'ground_truth')
    s = R.s; R.mal_by_id = np.zeros(int(R.eps.episode_id.max()) + 1 if len(R.eps) else 1, np.int64); R.mal_by_id[R.eps.episode_id.values] = R.eps.is_malicious.values
    ep_of_event_total = np.zeros(int(R.eps.episode_id.max()) + 1 if len(R.eps) else 1, np.int64)
    rng = np.random.default_rng([R.seed, R.run_id, 9])
    with gzip.open(f'{corp}/events.csv.gz', 'wt') as fe, gzip.open(f'{gt}/event_labels.csv.gz', 'wt') as fl:
        first = True
        for lo in range(0, R.N, slice_n):
            hi = min(R.N, lo + slice_n); sid = R.sid[lo:hi]
            eid = np.array(_uuids(hi - lo, rng), dtype=object)
            rv = pd.Series(R.rv[lo:hi]).where(lambda x: x > 0).astype('Int64')
            df = pd.DataFrame({
                'run_id': R.run_id, 'event_id': eid, 'employee_id': s['emp'][sid],
                'occurred_at': _iso(R.t[lo:hi]), 'ingested_at': _iso(R.t[lo:hi] + R.lat[lo:hi]),
                'event_type': ET[R.et[lo:hi]], 'result': RS[R.rs[lo:hi]],
                'ip_address': R.s_ipstr[sid], 'device_id': s['dev'][sid], 'session_id': R.s_uuid[sid],
                'resource_id': rv, 'is_vpn': s['vpn'][sid], 'attributes': _attrs(R, lo, hi)})
            df.to_csv(fe, index=False, header=first); first = False
            ep = s['ep'][sid]; m = ep >= 0
            if m.any():
                lab = pd.DataFrame({'run_id': R.run_id, 'event_id': eid[m], 'episode_id': ep[m],
                                    'label': np.where(R.mal_by_id[ep[m]] == 1, 'malicious', 'benign')})
                lab.to_csv(fl, index=False, header=(lo == 0))
                np.add.at(ep_of_event_total, ep[m], 1)
    # --- tabelas de apoio -------------------------------------------------------------
    emps = pd.DataFrame([dict(employee_id=e.id, department=e.dept, role=e.persona, manager_id=None, persona=e.persona,
                              privileged=e.priv0 > 0, site={'SP': 'vila_sede', 'MAO': 'porto_verde'}[e.site],
                              timezone=f'UTC{e.tz:+d}', hired_at=e.hired) for e in W.emps])
    head = emps.groupby('department').employee_id.transform('min')
    emps['manager_id'] = np.where(emps.employee_id == head, None, head).astype(object)
    emps.to_csv(f'{corp}/employees.csv', index=False)
    pd.DataFrame(W.res).to_csv(f'{corp}/resources.csv', index=False)
    pd.DataFrame(W.devices).to_csv(f'{corp}/devices.csv', index=False)
    pd.DataFrame([{k: r[k] for k in ('cidr', 'type', 'country', 'city')} for r in W.ranges]).to_csv(f'{corp}/network_ranges.csv', index=False)
    pd.DataFrame({'session_id': R.s_uuid, 'employee_id': s['emp'], 'started_at': _iso(s['t0']), 'ended_at': _iso(s['t1']),
                  'is_vpn': s['vpn'], 'device_id': s['dev']}).to_csv(f'{corp}/sessions.csv', index=False)
    hr = [dict(employee_id=e.id, kind='vacation', start_date=W.days[a], end_date=W.days[b]) for e in W.emps for a, b in e.vac_blocks]
    hr += [dict(employee_id=i, kind=k, start_date=W.days[a], end_date=W.days[b]) for i, k, a, b in W.hr_extra]
    pd.DataFrame(hr).to_csv(f'{corp}/hr_calendar.csv', index=False)
    _account_state(R, corp)
    _device_state(R, corp)
    # --- gabarito -------------------------------------------------------------------
    eps = R.eps.copy(); eps.insert(1, 'run_id', R.run_id)
    t0 = pd.Series(s['t0']).groupby(s['ep']).min(); t1 = pd.Series(s['t1']).groupby(s['ep']).max()
    eps['started_at'] = _iso(t0.reindex(eps.episode_id).values.astype(np.int64))
    eps['ended_at'] = _iso(t1.reindex(eps.episode_id).values.astype(np.int64))
    eps['n_events'] = ep_of_event_total[eps.episode_id.values]
    eps['catalog_version'] = 'provisorio-v1'
    eps.to_csv(f'{gt}/episodes.csv', index=False)
    return base


def _account_state(R, corp):
    W = R.W; m = (R.et == C.E['SYSTEM_CONFIG']) & (R.rs == 0) & np.isin(R.a1, [C.SUB['mfa_disabled'], C.SUB['mfa_enabled'], C.SUB['privilege_escalation']])
    emp_ev = R.s['emp'][R.sid[m]]; tgt = np.where(R.a3[m] > 0, R.a3[m], emp_ev)
    st = {e.id: [(int(W.day_epoch[0]), e.mfa0, e.priv0)] for e in W.emps}
    for t, a, eid in zip(R.t[m], R.a1[m], tgt):
        _, mfa, pv = st[int(eid)][-1]
        if a == C.SUB['mfa_disabled']: mfa = False
        elif a == C.SUB['mfa_enabled']: mfa = True
        else: pv = min(2, pv + 1)
        st[int(eid)].append((int(t), mfa, pv))
    rows = []
    for eid, L in st.items():
        for i, (t, mfa, pv) in enumerate(L):
            rows.append(dict(run_id=R.run_id, employee_id=eid, valid_from=_iso(np.array([t]))[0],
                             valid_to=_iso(np.array([L[i + 1][0]]))[0] if i + 1 < len(L) else None,
                             mfa_enabled=mfa, privilege_level=pv))
    pd.DataFrame(rows).to_csv(f'{corp}/account_state.csv', index=False)
    R.n_state_changes = len(rows) - len(W.emps)


def _device_state(R, corp):
    from .normal import device_states
    rng = np.random.default_rng([R.seed, R.run_id, 3])
    dev, day, age, av = device_states(R.W, rng)
    pd.DataFrame({'run_id': R.run_id, 'device_id': dev, 'date': np.array(R.W.days, dtype='datetime64[D]')[day],
                  'patch_age_days': age, 'antivirus_active': av}).to_csv(f'{corp}/device_state_daily.csv.gz', index=False, compression='gzip')
