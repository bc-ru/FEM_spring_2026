from __future__ import annotations

import argparse
from pathlib import Path

from fenics import File

from solve_streamfunction import solve_problem
from postprocess import generate_all_outputs


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--a", type=float, default=1.0)
    parser.add_argument("--R", type=float, default=5.0)
    parser.add_argument("--u_inf", type=float, default=1.0)
    parser.add_argument("--p", type=int, default=2)
    parser.add_argument("--outdir", type=str, default="results/base_case")

    args = parser.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    mesh, facets, psi_h, psi_exact, err_L2, err_H1 = solve_problem(
        a=args.a,
        R=args.R,
        u_inf=args.u_inf,
        p=args.p,
    )

    # Экспорт для ParaView
    File(str(outdir / "psi_h.pvd")) << psi_h
    File(str(outdir / "psi_exact.pvd")) << psi_exact

    generate_all_outputs(
        outdir=outdir,
        mesh=mesh,
        facet_markers=facets,
        psi_h=psi_h,
        psi_exact=psi_exact,
        err_L2=err_L2,
        err_H1=err_H1,
        a=args.a,
        R=args.R,
        u_inf=args.u_inf,
        p=args.p,
    )

    print(f"Готово. Результаты сохранены в: {outdir}")


if __name__ == "__main__":
    main()