# solver/build_convergence_table.py

import json
import pandas as pd
from pathlib import Path


MESH_ORDER = ["coarse", "medium", "fine"]
P_VALUES = [1, 2, 3]


def load_summary(path):
    with open(path, "r") as f:
        return json.load(f)


def build_table():
    rows = []

    for mesh in MESH_ORDER:
        for p in P_VALUES:
            path = Path(f"results/base/{mesh}/p{p}/summary.json")

            if not path.exists():
                continue

            s = load_summary(path)

            rows.append({
                "mesh": mesh,
                "p": p,
                "cells": s["num_cells"],
                "L2(psi)": s["err_L2_psi"],
                "H1(psi)": s["err_H1_psi"],
                "Linf(u_tau)": s["tau_err_Linf"],
            })

    df = pd.DataFrame(rows)

    df = df.sort_values(["p", "mesh"])

    df.to_csv("results/convergence_table.csv", index=False)

    print(df)


if __name__ == "__main__":
    build_table()