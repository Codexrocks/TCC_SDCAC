"""python -m generator --seeds 10 --out out [--scale 1.0] [--days 365] [--start 2026-01-01]"""
import argparse, time
from datetime import date
import numpy as np
from . import checks, output
from .core import Sink
from .normal import simulate_normal
from .scenarios import inject
from .world import build_world

p = argparse.ArgumentParser()
p.add_argument('--seeds', type=int, default=1, help='número de execuções (run_id 1..N, semente base + i)')
p.add_argument('--seed0', type=int, default=42)
p.add_argument('--out', default='out')
p.add_argument('--scale', type=float, default=1.0, help='fração do efetivo (250 funcionários = 1.0)')
p.add_argument('--days', type=int, default=365)
p.add_argument('--start', default='2026-01-01')
p.add_argument('--scenario-scale', type=float, default=1.0)
a = p.parse_args()
start = date.fromisoformat(a.start)
for run_id in range(1, a.seeds + 1):
    seed = a.seed0 + run_id - 1; t0 = time.time()
    W = build_world(seed, start, a.days, a.scale)
    S = Sink(W, np.random.default_rng([seed, 21]))
    inject(W, S, np.random.default_rng([seed, 31]), a.scenario_scale)     # cenários primeiro: registram overrides
    simulate_normal(W, S, np.random.default_rng([seed, 41]))
    R = output.assemble(W, S, run_id, seed)
    res = checks.run(R, full_scale=(a.scale == 1.0 and a.days >= 365))
    checks.report(res)
    base = output.write(R, a.out)
    print(f'run {run_id} (seed {seed}): {R.N:,} eventos, {R.nS:,} sessões, {len(R.eps)} episódios -> {base}  [{time.time() - t0:.0f}s]')
    print(R.eps.groupby('family').size().to_dict())
