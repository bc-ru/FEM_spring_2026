#!/usr/bin/env python3
"""Run one vortex-potential flow case from the command line."""
from __future__ import annotations

import argparse
from pathlib import Path

try:
    from .problem import CaseParameters
    from .solve_stream import solve_case
except ImportError:
    from problem import CaseParameters
    from solve_stream import solve_case


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mesh-prefix", required=True, help="Prefix without _mesh.xdmf/_facets.xdmf")
    parser.add_argument("--out", required=True)
    parser.add_argument("--L", type=float, default=4.0)
    parser.add_argument("--H", type=float, default=1.0)
    parser.add_argument("--l", type=float, default=1.0)
    parser.add_argument("--h", type=float, default=1.0)
    parser.add_argument("--Gamma", type=float, default=-2.0)
    parser.add_argument("--degree", type=int, default=1, choices=[1, 2, 3])
    parser.add_argument("--alpha", type=float, default=0.5)
    parser.add_argument("--tol-psi", type=float, default=1.0e-8)
    parser.add_argument("--tol-omega", type=float, default=1.0e-8)
    parser.add_argument("--max-iter", type=int, default=200)
    parser.add_argument("--initial-eps", type=float, default=0.05)
    parser.add_argument("--initial-vortex-x", type=float, default=2.0)
    args = parser.parse_args()

    params = CaseParameters(
        L=args.L,
        H=args.H,
        l=args.l,
        h=args.h,
        Gamma=args.Gamma,
        degree=args.degree,
        alpha=args.alpha,
        tol_psi=args.tol_psi,
        tol_omega=args.tol_omega,
        max_iter=args.max_iter,
        initial_eps=args.initial_eps,
        initial_vortex_x=args.initial_vortex_x,
    )
    metrics = solve_case(Path(args.mesh_prefix), params, Path(args.out))
    for key, value in metrics.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
