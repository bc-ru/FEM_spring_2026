#!/usr/bin/env python3
from __future__ import annotations

from common import ROOT, make_mesh, run

L, H, ell, h = 4.0, 1.0, 1.0, 1.0
Gamma = -2.0
for name, lc in [("base_coarse", 0.10), ("base_medium", 0.05), ("base_fine", 0.025)]:
    prefix = make_mesh(name, L, H, ell, h, lc)
    run([
        "python3", "solver/run_case.py",
        "--mesh-prefix", prefix,
        "--out", ROOT / "results" / name / "p1_Gamma-2",
        "--L", L, "--H", H, "--l", ell, "--h", h,
        "--Gamma", Gamma,
        "--degree", 1,
        "--alpha", 0.5,
    ])
