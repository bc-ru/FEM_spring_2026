from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


RESULTS_DIR = Path("results")


def read_json(path: str | Path):
    p = Path(path)
    if not p.exists():
        return None
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def read_csv(path: str | Path):
    p = Path(path)
    if not p.exists():
        return None
    return pd.read_csv(p)


def show_image_if_exists(path: str | Path, caption: str | None = None):
    p = Path(path)
    if p.exists():
        st.image(str(p), caption=caption, use_container_width=True)
        return True
    st.info(f"Файл `{p}` пока не найден.")
    return False


def code_block(title: str, code: str, language: str = "python"):
    st.markdown(f"**{title}**")
    st.code(code.strip("\n"), language=language)


def metric_row_from_summary(summary: dict | None):
    if not summary:
        st.info("Сводка расчёта ещё не найдена.")
        return
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Число ячеек", summary.get("num_cells", "—"))
    c2.metric("Число узлов", summary.get("num_vertices", "—"))
    c3.metric("L2(ψ)", f"{summary.get('err_L2_psi', float('nan')):.3e}")
    c4.metric("H1(ψ)", f"{summary.get('err_H1_psi', float('nan')):.3e}")


def draw_geometry(a: float = 1.0, R: float = 5.0):
    theta = np.linspace(0.0, np.pi, 400)
    z_outer = R * np.cos(theta)
    r_outer = R * np.sin(theta)
    z_inner = a * np.cos(theta)
    r_inner = a * np.sin(theta)

    fig, ax = plt.subplots(figsize=(8.5, 4.8))
    ax.plot(z_outer, r_outer, linewidth=2.2)
    ax.plot(z_inner, r_inner, linewidth=2.2)
    ax.plot([-R, -a], [0, 0], linewidth=2.2)
    ax.plot([a, R], [0, 0], linewidth=2.2)

    ax.text(0.0, 0.58 * R, r"$\Gamma$", fontsize=14)
    ax.text(0.0, 0.58 * a, r"$\gamma$", fontsize=14)
    ax.text(-0.55 * (R + a), 0.09 * R, r"$\Gamma_1$", fontsize=13)
    ax.text(0.25 * (R + a), 0.09 * R, r"$\Gamma_2$", fontsize=13)
    ax.text(0.0, 0.35 * (R + a) / 2.0, r"$\Omega$", fontsize=14)

    ax.set_aspect("equal")
    ax.set_xlim(-1.1 * R, 1.1 * R)
    ax.set_ylim(-0.12 * R, 1.08 * R)
    ax.set_xlabel("z")
    ax.set_ylabel("r")
    ax.grid(True, alpha=0.25)
    fig.tight_layout()
    return fig


def explain_table_columns():
    df = pd.DataFrame(
        {
            "Столбец": ["mesh", "p", "cells", "L2(psi)", "H1(psi)", "Linf(u_tau)"],
            "Смысл": [
                "имя сетки: coarse, medium, fine",
                "степень лагранжевого элемента",
                "число треугольников в сетке",
                "ошибка функции тока в норме L2",
                "ошибка функции тока в норме H1",
                "максимальная ошибка касательной скорости на сфере",
            ],
        }
    )
    st.table(df)


def plot_convergence(df: pd.DataFrame, column: str, ylabel: str):
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    for p in sorted(df["p"].unique()):
        sub = df[df["p"] == p].copy()
        sub = sub.sort_values("cells")
        ax.plot(sub["cells"], sub[column], "o-", label=f"p={p}")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("Число ячеек")
    ax.set_ylabel(ylabel)
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()
    return fig


def list_missing(paths: Iterable[str | Path]):
    missing = [str(Path(p)) for p in paths if not Path(p).exists()]
    if missing:
        st.warning("Не найдены файлы:\n\n- " + "\n- ".join(missing))
        return False
    return True
