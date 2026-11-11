"""Organização simulada: pessoas, personas, calendário, recursos, dispositivos e faixas de rede."""

import ipaddress
from datetime import date, timedelta

import numpy as np
from dateutil.easter import easter

from . import config as cfg


class Obj:  # saco de atributos
    pass


def br_holidays(year):
    e = easter(year)
    fixed = [
        (1, 1),
        (4, 21),
        (5, 1),
        (9, 7),
        (10, 12),
        (11, 2),
        (11, 15),
        (11, 20),
        (12, 25),
    ]
    out = {date(year, m, d) for m, d in fixed}
    out |= {
        e - timedelta(days=48),
        e - timedelta(days=47),
        e - timedelta(days=2),
        e + timedelta(days=60),
    }
    return out


def build_world(seed, start, days, scale=1.0):
    rng = np.random.default_rng([seed, 11])
    world = Obj()
    world.seed, world.start, world.ndays, world.scale = seed, start, days, scale
    world.days = [start + timedelta(days=i) for i in range(days)]
    hol = set()
    for y in sorted({d.year for d in world.days}):
        hol |= br_holidays(y)
    world.is_hol = np.array([d in hol for d in world.days])
    world.wd = np.array([d.weekday() for d in world.days])
    world.day_epoch = np.array(
        [(d - date(1970, 1, 1)).days * 86400 for d in world.days], dtype=np.int64
    )
    world.yyyymm = np.array([d.year * 100 + d.month for d in world.days])
    world.eval_start = min(cfg.EVAL_START_DAY, max(1, days // 3))

    # fim de mês: últimos 3 dias úteis de cada mês
    world.month_end = np.zeros(days, bool)
    for m in np.unique(world.yyyymm):
        idx = [
            i
            for i in np.flatnonzero(world.yyyymm == m)
            if world.wd[i] < 5 and not world.is_hol[i]
        ]
        world.month_end[idx[-3:]] = True

    # ---------------------------------------------------------------- faixas de rede (ASSUNÇÃO P12)
    data = []

    def add(cidr, typ, country, city):
        n = ipaddress.ip_network(cidr)
        data.append(
            dict(
                cidr=cidr,
                type=typ,
                country=country,
                city=city,
                base=int(n.network_address),
                size=n.num_addresses,
            )
        )

    add("10.10.0.0/16", "office", "XA", "vila_sede")
    add("10.20.0.0/16", "office", "XA", "porto_verde")
    add("10.99.0.0/16", "vpn", "XA", "vila_sede")
    for i in range(8):
        add(f"198.18.{i}.0/24", "home", "XA", "vila_sede")
    for i in range(8, 12):
        add(f"198.18.{i}.0/24", "home", "XA", "porto_verde")
    for i in range(12, 16):
        add(f"198.18.{i}.0/24", "home", "XA", "vila_nova")
    for j, c in enumerate(["serra_alta", "baia_azul", "campo_largo", "lago_grande"]):
        for k in range(2):
            add(f"198.19.{j * 2 + k}.0/24", "external", "XA", c)
    for j, (c, cc) in enumerate(
        [("terra_nova", "XB"), ("ilha_cinza", "XC"), ("monte_real", "XD")]
    ):
        for k in range(4):
            add(f"198.19.{16 + j * 4 + k}.0/24", "external", cc, c)
    world.ranges = data
    world.r_office = {"SP": 0, "MAO": 1}
    world.r_vpn = 2
    world.r_home = {
        "vila_sede": [3 + i for i in range(8)],
        "porto_verde": [11 + i for i in range(4)],
        "vila_nova": [15 + i for i in range(4)],
    }
    world.r_ext_dom = [
        i
        for i, r in enumerate(data)
        if r["type"] == "external" and r["country"] == "XA"
    ]
    world.r_ext_for = [
        i
        for i, r in enumerate(data)
        if r["type"] == "external" and r["country"] != "XA"
    ]

    # ---------------------------------------------------------------- recursos (D-39)
    res, world.sys_ids = [], {}

    def addres(key, name, sens, owner, n):
        ids = []
        for k in range(1, n + 1):
            res.append(
                dict(
                    resource_id=len(res) + 1,
                    system=key,
                    name=f"{name}_{k:03d}" if n > 1 else name,
                    sensitivity=sens,
                    owner_department=owner,
                )
            )
            ids.append(len(res))
        world.sys_ids[key] = ids

    for key, (nm, sens, n, dep) in cfg.SYSTEMS.items():
        owner = {
            "crm": "sales",
            "repo": "engineering_product",
            "fs_conf_fin": "admin_finance",
            "fs_conf_leg": "legal",
            "erp": "admin_finance",
            "contracts": "legal",
            "payroll": "hr",
            "dossier": "hr",
            "console": "it_infra",
        }.get(key, "")
        addres(key, nm, sens, owner, n)
    depts = sorted({c[0] for c in cfg.COHORTS})
    for d in depts:
        addres("fs_own_" + d, f"arquivos_{d}", "internal", d, cfg.FS_OWN_N)
    world.res = res
    world.res_sens = np.array(
        [0] + [cfg.SENS.index(r["sensitivity"]) for r in res], dtype=np.int64
    )
    world.mail_id = world.sys_ids["mail"][0]
    world.portal_ids = world.sys_ids["portal"]
    world.mob_ids = np.array([world.mail_id] + world.portal_ids)

    # ---------------------------------------------------------------- funcionários (D-37/38)
    emps, nid = [], 0
    for dept, persona, site, n in cfg.COHORTS:
        n = max(1, round(n * scale)) if scale != 1.0 else n
        for _ in range(n):
            nid += 1
            e = Obj()
            e.id, e.dept, e.persona, e.site, e.tz = (
                nid,
                dept,
                persona,
                site,
                cfg.TZ[site],
            )
            p = cfg.PERSONAS[persona]
            e.mu = float(
                np.clip(
                    rng.normal((p["lo"] + p["hi"]) / 2, (p["hi"] - p["lo"]) / 6),
                    p["lo"],
                    p["hi"],
                )
            )
            e.hire_idx = int(rng.integers(1, 60)) if rng.random() < 0.04 else 0
            e.hired = (
                start + timedelta(days=e.hire_idx)
                if e.hire_idx
                else date(start.year - int(rng.integers(1, 8)), 1, 1)
            )
            e.priv0 = (
                2
                if (persona == "it_privileged" and rng.random() < 0.4)
                else (1 if persona in ("it_privileged", "management") else 0)
            )
            e.mfa0 = bool(
                rng.random()
                < (cfg.MFA0_PRIV if dept in ("it_infra", "board") else cfg.MFA0_BASE)
            )
            e.p_err = float(
                np.clip(rng.lognormal(np.log(0.03), 0.5), 0.005, 0.15)
            )  # P17 (ASSUNÇÃO)
            e.susc = float(np.clip(rng.lognormal(0, 0.35), 0.4, 2.2))
            e.bias = float(rng.normal(0, 0.5))
            e.shift = int(rng.integers(3))
            a = int(rng.integers(7))
            e.off = (a, (a + 1) % 7)
            e.home_days = [(0, 2), (1, 3), (2, 4), (0, 3)][int(rng.integers(4))]
            e.usb_rate = {"hybrid_eng": 0.02, "it_privileged": 0.015}.get(
                persona, 0.006
            )
            # férias: 1-2 blocos, 22-30 dias corridos (hr_calendar)
            e.vac_blocks, e.vac = [], np.zeros(days, bool)
            tot = int(rng.integers(22, 31))
            nb = int(rng.integers(1, 3))
            for b in range(nb):
                length = tot // nb if b == 0 else tot - tot // nb
                s0 = int(rng.integers(0, max(1, days - length)))
                e.vac[s0 : s0 + length] = True
                e.vac_blocks.append((s0, min(days - 1, s0 + length - 1)))
            e.sick = rng.random(days) < 0.012
            wd_ok = (
                ~np.isin(world.wd, e.off)
                if persona == "shift_ops"
                else (world.wd < 5) & ~world.is_hol
            )
            e.works = wd_ok & ~e.vac & ~e.sick & (np.arange(days) >= e.hire_idx)
            e.base_off = ~wd_ok
            # origem
            city = (
                "porto_verde"
                if site == "MAO"
                else ("vila_nova" if rng.random() < 0.2 else "vila_sede")
            )
            e.home_r = int(rng.choice(world.r_home[city]))
            e.home_ip = rand_ip(world, rng, e.home_r)
            e.office_ip = rand_ip(world, rng, world.r_office[site])
            e.phish = {}
            for m in np.unique(world.yyyymm):
                idx = np.flatnonzero(world.yyyymm == m)
                if len(idx) > 10:
                    e.phish[int(idx[min(len(idx) - 1, int(rng.integers(7, 21)))])] = (
                        int(m)
                    )
            emps.append(e)
    world.emps, world.emp_by_id = emps, {e.id: e for e in emps}
    world.payroll_staff = set([e.id for e in emps if e.dept == "hr"][:5])

    # acesso permitido (matriz D-39) e recursos habituais (base do padrão D-24)
    for e in emps:
        ids = []
        for key, (nm, sens, n, dep) in cfg.SYSTEMS.items():
            ok = (dep is None) or (
                e.id in world.payroll_staff or e.dept == "board"
                if dep == "hr5+board"
                else e.dept in dep
            )
            if ok:
                ids += world.sys_ids[key]
        ids += world.sys_ids["fs_own_" + e.dept]
        e.allowed = np.array(sorted(set(ids)))
        pool = np.array(
            [i for i in e.allowed if i != world.mail_id and i not in world.portal_ids]
        )
        k = min(len(pool), int(rng.integers(12, 26)))
        chosen = rng.choice(pool, size=k, replace=False)
        hab = np.concatenate([[world.mail_id, world.portal_ids[0]], chosen])
        w = 1.0 / np.arange(1, len(hab) + 1) ** 0.9
        e.hab_ids, e.hab_p = hab, w / w.sum()
        e.mob_ids = world.mob_ids

    # ---------------------------------------------------------------- dispositivos (D-41)
    dev = [
        dict(
            device_id=0,
            owner_employee_id=None,
            device_type="unknown_external",
            corporate=False,
        )
    ]
    for e in emps:
        dev.append(
            dict(
                device_id=len(dev),
                owner_employee_id=e.id,
                device_type="notebook",
                corporate=True,
            )
        )
        e.dev_nb = len(dev) - 1
        e.dev_ph = 0
    order = rng.permutation(len(emps))
    n_corp = round(cfg.CORP_PHONE_FRAC * len(emps))
    n_pers = (
        round(cfg.PERSONAL_PHONE_N * len(emps) / 250)
        if scale != 1.0
        else cfg.PERSONAL_PHONE_N
    )
    for j, ix in enumerate(order[: n_corp + n_pers]):
        e = emps[ix]
        dev.append(
            dict(
                device_id=len(dev),
                owner_employee_id=e.id,
                device_type="corporate_phone" if j < n_corp else "personal_phone",
                corporate=j < n_corp,
            )
        )
        e.dev_ph = len(dev) - 1
        e.ph_personal = j >= n_corp
    world.devices = dev
    world.nb_devices = [e.dev_nb for e in emps]

    # ---------------------------------------------------------------- janelas de manutenção TI (D-38)
    world.maint = {}
    it = [e.id for e in emps if e.persona == "it_privileged"]
    for m in np.unique(world.yyyymm):
        fr = [
            i
            for i in np.flatnonzero(world.yyyymm == m)
            if world.wd[i] == 4 and not world.is_hol[i] and i >= 0
        ]
        if fr and it:
            di = fr[min(1, len(fr) - 1)]
            for eid in rng.choice(it, size=min(5, len(it)), replace=False):
                world.maint[(int(eid), int(di))] = int(m)

    # overrides registrados pelos cenários
    world.mfa_off, world.dev_nopatch, world.phish_force, world.hr_extra = {}, {}, {}, []
    world.all_ids = np.array([e.id for e in emps])
    return world


def rand_ip(world, rng, ridx):
    r = world.ranges[ridx]
    return int(r["base"] + rng.integers(1, r["size"] - 1))


def ip_str(i):
    return f"{(i >> 24) & 255}.{(i >> 16) & 255}.{(i >> 8) & 255}.{i & 255}"


def mfa_at(world, e, t):
    if not e.mfa0:
        return False
    for a, b in world.mfa_off.get(e.id, ()):
        if a <= t < b:
            return False
    return True
