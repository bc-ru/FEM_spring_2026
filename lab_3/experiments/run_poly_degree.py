#!/usr/bin/env python3
from __future__ import annotations

from common import ROOT, make_mesh, run

L, H, ell, h = 4.0, 1.0, 1.0, 1.0
Gamma = -2.0
prefix = make_mesh("degree_mesh", L, H, ell, h, 0.05)
for p in [1, 2, 3]:
    run([
        "python3", "solver/run_case.py",
        "--mesh-prefix", prefix,
        "--out", ROOT / "results" / "degree_sweep" / f"p{p}",
        "--L", L, "--H", H, "--l", ell, "--h", h,
        "--Gamma", Gamma,
        "--degree", p,
        "--alpha", 0.4,
    ])
