#!/usr/bin/env python3
from __future__ import annotations

from common import ROOT, make_mesh, run

L, H, ell = 4.0, 1.0, 1.0
Gamma = -2.0
for h in [0.5, 0.75, 1.0]:
    tag = str(h).replace(".", "p")
    prefix = make_mesh(f"height_h{tag}", L, H, ell, h, 0.05)
    run([
        "python3", "solver/run_case.py",
        "--mesh-prefix", prefix,
        "--out", ROOT / "results" / "height_sweep" / f"h_{tag}",
        "--L", L, "--H", H, "--l", ell, "--h", h,
        "--Gamma", Gamma,
        "--degree", 1,
        "--alpha", 0.5,
    ])
