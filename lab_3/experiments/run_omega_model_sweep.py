#!/usr/bin/env python3
from __future__ import annotations

from common import ROOT, make_mesh, run

L, H, ell, h = 4.0, 1.0, 1.0, 1.0
Gamma = -2.0
prefix = make_mesh("omega_model_mesh", L, H, ell, h, 0.05)

cases = [
    ("constant_q0", "constant", 0.0),
    ("power_q1", "power", 1.0),
    ("power_q2", "power", 2.0),
]

for name, model, power in cases:
    run([
        "python3", "solver/run_case.py",
        "--mesh-prefix", prefix,
        "--out", ROOT / "results" / "omega_model_sweep" / name,
        "--L", L, "--H", H, "--l", ell, "--h", h,
        "--Gamma", Gamma,
        "--degree", 1,
        "--alpha", 0.5,
        "--omega-model", model,
        "--omega-power", power,
    ])
