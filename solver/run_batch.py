# solver/run_batch.py

import subprocess
import json
from pathlib import Path

from geo_builder import generate_geo


A = 1.0
U_INF = 1.0

# сетки (примерно ×4 сгущение)
MESHES = {
    "coarse": 0.5,
    "medium": 0.25,
    "fine": 0.125,
}

P_VALUES = [1, 2, 3]
R_VALUES = [3.0, 5.0, 15.0]


def run_cmd(cmd):
    print(">>", " ".join(cmd))
    subprocess.run(cmd, check=True)


def run_base_case():
    print("=== BASE CASE (R=5) ===")

    for mesh_name, h in MESHES.items():
        print(f"\n--- mesh: {mesh_name}, h={h} ---")

        geo_path = Path("meshes/sphere.geo")
        generate_geo(A, 5.0, h, geo_path)

        run_cmd(["gmsh", "-2", str(geo_path), "-o", "meshes/sphere.msh"])

        run_cmd(["python3", "solver/convert_msh_to_xdmf.py"])

        for p in P_VALUES:
            outdir = f"results/base/{mesh_name}/p{p}"

            run_cmd(
                [
                    "python3",
                    "solver/run_case.py",
                    "--a",
                    str(A),
                    "--R",
                    "5.0",
                    "--u_inf",
                    str(U_INF),
                    "--p",
                    str(p),
                    "--outdir",
                    outdir,
                ]
            )


def run_R_study():
    print("\n=== R STUDY ===")

    h = 0.125  # фиксируем хорошую сетку

    for R in R_VALUES:
        print(f"\n--- R = {R} ---")

        geo_path = Path("meshes/sphere.geo")
        generate_geo(A, R, h, geo_path)

        run_cmd(["gmsh", "-2", str(geo_path), "-o", "meshes/sphere.msh"])
        run_cmd(["python3", "solver/convert_msh_to_xdmf.py"])

        outdir = f"results/R_study/R{int(R)}"

        run_cmd(
            [
                "python3",
                "solver/run_case.py",
                "--a",
                str(A),
                "--R",
                str(R),
                "--u_inf",
                str(U_INF),
                "--p",
                "2",
                "--outdir",
                outdir,
            ]
        )


def main():
    run_base_case()
    run_R_study()


if __name__ == "__main__":
    main()
