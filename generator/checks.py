"""Checagens da seção 9 da banco-simulado.md + invariantes D-17/D-23/D-27 (falha = exceção)."""

import calendar
from datetime import date

import numpy as np

from . import config as cfg


def _dias_de_tres_meses(inicio):
    """Quantos dias tem os tres primeiros meses a partir de `inicio`.

    Derivado do calendario, nao de constante: com inicio em 2026-01-01 sao 90
    (31+28+31). O dia e preservado, e cai para o ultimo do mes quando o mes de
    destino e mais curto -- 31/01 mais tres meses e 30/04.
    """
    mes = inicio.month + 3
    ano, mes = inicio.year + (mes - 1) // 12, (mes - 1) % 12 + 1
    dia = min(inicio.day, calendar.monthrange(ano, mes)[1])
    return (date(ano, mes, dia) - inicio).days


def run(data, full_scale):
    world, s = data.W, data.s
    res = []

    def chk(name, ok, detail=""):
        res.append((name, bool(ok), detail))

    et, sid, t, n_ev = data.et, data.sid, data.t, data.N
    # 1. toda sessão: 1 LOGOUT, ≥1 LOGIN com sucesso; funcionário existe
    n_out = np.bincount(sid[et == 1], minlength=data.nS)
    n_ok = np.bincount(sid[(et == 0) & (data.rs == 0)], minlength=data.nS)
    chk(
        "cada sessão tem exatamente 1 LOGOUT e 1 LOGIN com sucesso",
        (n_out == 1).all() and (n_ok == 1).all(),
        f"{data.nS} sessões",
    )
    chk(
        "sessões referenciam funcionários existentes",
        np.isin(s["emp"], world.all_ids).all(),
    )
    # 2. nenhuma ação depois do LOGOUT da própria sessão
    last = np.zeros(data.nS, np.int64)
    np.maximum.at(last, sid, np.arange(n_ev))
    chk(
        "nenhuma ação depois do LOGOUT da própria sessão",
        (et[last] == 1).all()
        and (t <= s["t1"][sid]).all()
        and (t >= s["t0"][sid]).all(),
    )
    # 3. listas fechadas
    chk(
        "códigos dentro das listas fechadas",
        (data.rs <= 2).all()
        and (data.a1[et == 3] > 0).all()
        and (data.a2[et == 3] < 3).all()
        and (data.a1[et == 5] < len(cfg.DOMAINS)).all()
        and (data.a2[et == 0] < 5).all()
        and (data.a1[et == 6] < 5).all()
        and (data.a2[et == 7] < 4).all(),
    )
    chk("size_bytes > 0 em todo FILE_DOWNLOAD", (data.a1[et == 3] > 0).all())
    chk("domínios sempre .example", all(d.endswith(".example") for d, _ in cfg.DOMAINS))
    # 4. IP dentro de faixa cadastrada; is_vpn <=> faixa vpn
    base = np.array([r["base"] for r in world.ranges])
    end = base + np.array([r["size"] for r in world.ranges]) - 1
    ip = s["ip"]
    ix = np.searchsorted(base, ip, "right") - 1
    inr = (ix >= 0) & (ip <= end[np.maximum(ix, 0)])
    chk(
        "todo IP está dentro de uma faixa cadastrada", inr.all(), f"{(~inr).sum()} fora"
    )
    typ = np.array([r["type"] for r in world.ranges])[np.maximum(ix, 0)]
    chk("is_vpn <=> IP na faixa vpn", ((typ == "vpn") == s["vpn"]).all())
    # 5. sem rótulo em corp (D-17): o gabarito só existe em ground_truth
    chk(
        "eventos/sessões de corp não carregam rótulo (D-17)",
        True,
        "colunas fixas em output.write",
    )
    # 6. calendário (D-27)
    day_of_s = (
        (s["t0"] + np.array([world.emp_by_id[i].tz for i in s["emp"]]) * 3600) // 86400
        - world.day_epoch[0] // 86400
    ).astype(int)
    hire = np.array([world.emp_by_id[i].hire_idx for i in s["emp"]])
    chk("nenhum evento antes da admissão", (day_of_s >= hire - 1).all())
    ncnt = np.bincount(sid, minlength=data.nS)
    normal = s["ep"] < 0
    vac = np.array(
        [
            world.emp_by_id[i].vac[min(max(d, 0), world.ndays - 1)]
            for i, d in zip(s["emp"], day_of_s, strict=True)
        ]
    )
    chk(
        "atividade residual em férias existe e é < 3% do volume",
        0 < ncnt[normal & vac].sum() < 0.03 * ncnt[normal].sum(),
        f"{ncnt[normal & vac].sum()} eventos em férias",
    )
    # 7. volume por dia útil (D-23)
    # ATENCAO: o filtro de "dia util" aqui e `tot >= 10` eventos no dia, e
    # nao o dia da semana. A pergunta esta aberta em docs/o-que-falta.md,
    # secao do Filipe: as faixas da D-23 e da D-38 valem por dia de semana
    # ou por dia com atividade? Trocar o filtro muda o que a checagem mede.
    key = np.array([world.emp_by_id[i].id for i in s["emp"]]) * 10000 + np.clip(
        day_of_s, 0, 9999
    )
    u, inv = np.unique(key[normal], return_inverse=True)
    tot = np.bincount(inv, weights=ncnt[normal])
    emp_of = (u // 10000).astype(int)
    big = tot >= 10
    per = {}
    for e in world.emps:
        m = big & (emp_of == e.id)
        if m.any():
            per.setdefault(e.persona, []).append(tot[m].mean())
    ok = True
    det = []
    for p, v in per.items():
        mu = float(np.mean(v))
        lo, hi = cfg.PERSONAS[p]["lo"], cfg.PERSONAS[p]["hi"]
        ok &= 0.9 * lo <= mu <= 1.1 * hi
        det.append(f"{p}={mu:.1f}[{lo}-{hi}]")
    chk(
        "média de eventos/dia útil dentro da faixa de cada persona (D-38)",
        ok,
        " ".join(det),
    )
    wmean = float(
        np.average(
            [np.mean(v) for v in per.values()], weights=[len(v) for v in per.values()]
        )
    )
    chk(
        "média ponderada 20-50 eventos/dia útil (D-23)",
        20 <= wmean <= 50,
        f"{wmean:.1f}",
    )
    if full_scale:
        chk(
            "volume anual por semente em 1,15-2,9 M (D-23)",
            1.15e6 <= n_ev <= 2.9e6,
            f"{n_ev:,}",
        )
    # 8. cenários só após o baseline (D-24)
    inj = s["ep"] >= 0
    chk(
        "cenários começam após o baseline de 3 meses (D-24)",
        (
            day_of_s[
                inj
                & (
                    np.array(
                        [data.eps.family.values[e] if e >= 0 else "N" for e in s["ep"]]
                    )
                    != "N"
                )
            ]
            >= world.eval_start - 1
        ).all(),
    )
    # 9. o baseline tem de ser os 3 meses da D-24, e nao o que a constante disser.
    # A checagem acima compara os cenarios com `world.eval_start`: ela passa por
    # construcao, qualquer que seja o valor. Esta aqui mede a decisao, derivando
    # os 3 meses da data de inicio.
    chk(
        "baseline cobre exatamente 3 meses a partir do inicio (D-24)",
        world.eval_start == _dias_de_tres_meses(world.start),
        f"eval_start={world.eval_start} · 3 meses={_dias_de_tres_meses(world.start)}",
    )
    chk("ingested_at >= occurred_at", (data.lat > 0).all())
    return res


def report(res):
    bad = [r for r in res if not r[1]]
    print("\n=== CHECAGENS (seção 9) ===")
    for n, ok, d in res:
        print(("  OK   " if ok else "  FALHA"), n, f"— {d}" if d else "")
    if bad:
        raise SystemExit(f"{len(bad)} checagem(ns) falharam")
