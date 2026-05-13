#!/usr/bin/env python3
from __future__ import annotations

from common import ROOT, make_mesh, run

L, H, ell, h = 4.0, 1.0, 1.0, 1.0
prefix = make_mesh("gamma_mesh", L, H, ell, h, 0.05)
for Gamma in [-1.0, -2.0, -3.0]:
    tag = str(Gamma).replace("-", "m").replace(".", "p")
    run([
        "python3", "solver/run_case.py",
        "--mesh-prefix", prefix,
        "--out", ROOT / "results" / "gamma_sweep" / f"Gamma_{tag}",
        "--L", L, "--H", H, "--l", ell, "--h", h,
        "--Gamma", Gamma,
        "--degree", 1,
        "--alpha", 0.5,
    ])
