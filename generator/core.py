"""Sink: acumula sessões e eventos. Toda ação pertence a uma sessão (seção 9)."""
import numpy as np
from . import config as C

_Z = np.zeros(0, np.int64)


class Body:
    """Eventos do corpo de uma sessão: (dt desde o login, tipo, recurso, a1, a2, a3, resultado)."""
    def __init__(self):
        self.r = []

    def add(self, dt, et, res=0, a1=0, a2=0, a3=0, result=0):
        self.r.append((int(dt), et, int(res), int(a1), int(a2), int(a3), result))
        return self

    def arrays(self):
        if not self.r:
            return [_Z] * 7
        a = np.array(self.r, dtype=np.int64)
        a = a[np.argsort(a[:, 0], kind='stable')]
        return [a[:, i] for i in range(7)]


class Sink:
    def __init__(self, W, rng):
        self.W, self.rng = W, rng
        self.ch = []
        self.s = dict(emp=[], dev=[], vpn=[], ip=[], t0=[], t1=[], ep=[])
        self.eps = []

    def episode(self, family, code, emp_id, desc, malicious):
        self.eps.append((len(self.eps), family, code, emp_id, desc, int(malicious)))
        return len(self.eps) - 1

    def vpn_ip(self):
        r = self.W.ranges[self.W.r_vpn]
        return int(r['base'] + self.rng.integers(1, r['size'] - 1))

    def session(self, emp_id, t_first, D, body, ip, vpn, dev, mfa, ep=-1, n_wrong=0,
                gap=(4, 40), wait=(600, 2700), lo=None):
        """t_first = primeira tentativa de login (início da sessão); D = duração após o login."""
        rng = self.rng
        t = int(t_first)
        at, ar, ac = [], [], []
        for i in range(n_wrong):
            if i < 5:
                at.append(t); ar.append(1); ac.append(4 if rng.random() < .03 else 1)
            else:
                at.append(t); ar.append(2); ac.append(2)
            t += int(rng.uniform(*gap)) + 1
        if n_wrong >= 5:
            t += int(rng.uniform(*wait))
        n_mfa_fail = 0
        if mfa and rng.random() < .008:
            at.append(t); ar.append(1); ac.append(3); n_mfa_fail = 1
            t += int(rng.uniform(10, 40))
        t_login = t
        bd = body if body is not None else [_Z] * 7
        D = int(max(D, (bd[0].max() + 1) if len(bd[0]) else 1, 2))
        na = len(at)
        lo = int(rng.choice(3, p=[.82, .16, .02])) if lo is None else lo
        et = np.concatenate([np.zeros(na + 1, np.int64), bd[1], [1]])
        tt = np.concatenate([np.array(at, np.int64), [t_login], t_login + bd[0], [t_login + D]])
        rs = np.concatenate([np.array(ar, np.int64), [0], bd[6], [0]])
        rv = np.concatenate([np.zeros(na + 1, np.int64), bd[2], [0]])
        a1 = np.concatenate([np.array([1 if c == 3 else 0 for c in ac], np.int64), [int(bool(mfa))], bd[3], [lo]])
        a2 = np.concatenate([np.array(ac, np.int64), [0], bd[4], [0]])
        a3 = np.concatenate([np.zeros(na + 1, np.int64), bd[5], [0]])
        sid = len(self.s['emp'])
        n = len(tt)
        self.ch.append((tt, et, rs, rv, a1, a2, a3, np.arange(n, dtype=np.int64), np.full(n, sid, np.int64)))
        s = self.s
        s['emp'].append(emp_id); s['dev'].append(dev); s['vpn'].append(bool(vpn)); s['ip'].append(int(ip))
        s['t0'].append(int(t_first)); s['t1'].append(int(t_login + D)); s['ep'].append(int(ep))
        return sid, t_login
