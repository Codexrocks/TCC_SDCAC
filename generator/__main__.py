"""python -m generator --seeds 10 --out out [--scale 1.0] [--days 365] [--start 2026-01-01]"""

import argparse
import time
from datetime import date

import numpy as np

from . import checks, output
from .core import Sink
from .normal import simulate_normal
from .scenarios import inject
from .world import build_world

p = argparse.ArgumentParser()
p.add_argument(
    "--seeds",
    type=int,
    default=1,
    help="número de execuções (run_id 1..N, semente base + i)",
)
p.add_argument("--seed0", type=int, default=42)
p.add_argument("--out", default="out")
p.add_argument(
    "--scale",
    type=float,
    default=1.0,
    help="fração do efetivo (250 funcionários = 1.0)",
)
p.add_argument("--days", type=int, default=365)
p.add_argument("--start", default="2026-01-01")
p.add_argument("--scenario-scale", type=float, default=1.0)
a = p.parse_args()
start = date.fromisoformat(a.start)
for run_id in range(1, a.seeds + 1):
    seed = a.seed0 + run_id - 1
    t0 = time.time()
    world = build_world(seed, start, a.days, a.scale)
    sink = Sink(world, np.random.default_rng([seed, 21]))
    inject(
        world, sink, np.random.default_rng([seed, 31]), a.scenario_scale
    )  # cenários primeiro: registram overrides
    simulate_normal(world, sink, np.random.default_rng([seed, 41]))
    data = output.assemble(world, sink, run_id, seed)
    res = checks.run(data, full_scale=(a.scale == 1.0 and a.days >= 365))
    checks.report(res)
    base = output.write(data, a.out)
    print(
        f"run {run_id} (seed {seed}): {data.N:,} eventos, {data.nS:,} sessões, {len(data.eps)} episódios -> {base}  [{time.time() - t0:.0f}s]"
    )
    print(data.eps.groupby("family").size().to_dict())
