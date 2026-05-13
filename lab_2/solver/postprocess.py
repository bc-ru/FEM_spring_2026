from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.tri as mtri

from fenics import (
    FunctionSpace,
    SpatialCoordinate,
    Constant,
    conditional,
    gt,
    project,
    Point,
    facets,
)


PHYS_SPHERE = 1


def _make_triangulation(mesh):
    coords = mesh.coordinates()
    cells = mesh.cells()
    tri = mtri.Triangulation(coords[:, 0], coords[:, 1], cells)
    return coords, cells, tri


def _facet_length_2d(facet) -> float:
    """
    Длина 2D-грани как расстояние между её двумя вершинами.
    Работает для треугольной 2D-сетки в dolfin.
    """
    verts = facet.entities(0)
    mesh = facet.mesh()
    coords = mesh.coordinates()

    if len(verts) != 2:
        raise RuntimeError(
            f"Ожидалась 2D-грань с двумя вершинами, получено: {len(verts)}"
        )

    p0 = coords[verts[0]]
    p1 = coords[verts[1]]
    return float(np.linalg.norm(p1 - p0))


def _save_mesh_plot(mesh, outpath: Path):
    coords, cells, tri = _make_triangulation(mesh)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.triplot(tri, linewidth=0.45)
    ax.set_aspect("equal")
    ax.set_xlabel("z")
    ax.set_ylabel("r")
    ax.set_title("Расчётная сетка")
    ax.grid(True, alpha=0.2)
    fig.tight_layout()
    fig.savefig(outpath, dpi=180)
    plt.close(fig)


def _save_scalar_field_plot(mesh, field, title: str, outpath: Path):
    coords, cells, tri = _make_triangulation(mesh)
    values = field.compute_vertex_values(mesh)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    contour = ax.tricontourf(tri, values, levels=30)
    fig.colorbar(contour, ax=ax)
    ax.set_aspect("equal")
    ax.set_xlabel("z")
    ax.set_ylabel("r")
    ax.set_title(title)
    ax.grid(True, alpha=0.15)
    fig.tight_layout()
    fig.savefig(outpath, dpi=180)
    plt.close(fig)


def _save_error_plot(mesh, psi_h, psi_exact, outpath: Path):
    coords, cells, tri = _make_triangulation(mesh)
    vh = psi_h.compute_vertex_values(mesh)
    ve = psi_exact.compute_vertex_values(mesh)
    err = np.abs(vh - ve)

    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    contour = ax.tricontourf(tri, err, levels=30)
    fig.colorbar(contour, ax=ax)
    ax.set_aspect("equal")
    ax.set_xlabel("z")
    ax.set_ylabel("r")
    ax.set_title(r"Карта ошибки $|\psi_h - \psi_{\mathrm{exact}}|$")
    ax.grid(True, alpha=0.15)
    fig.tight_layout()
    fig.savefig(outpath, dpi=180)
    plt.close(fig)


def extract_tangential_velocity_on_sphere(
    mesh,
    facet_markers,
    psi_h,
    a: float,
    R: float,
    u_inf: float,
    degree: int,
) -> pd.DataFrame:
    """
    Извлечение касательной скорости на дискретной границе шара.

    Координаты в сетке:
        x[0] = z
        x[1] = r

    Компоненты скорости:
        u_r = (1/r) dpsi/dz
        u_z = -(1/r) dpsi/dr

    Для устойчивости при проектировании используется r_safe.
    """
    Q = FunctionSpace(mesh, "CG", max(1, degree))

    x = SpatialCoordinate(mesh)
    r_safe = conditional(gt(x[1], Constant(1e-10)), x[1], Constant(1e-10))

    u_r_h = project(psi_h.dx(0) / r_safe, Q)
    u_z_h = project(-psi_h.dx(1) / r_safe, Q)

    rows = []

    for facet in facets(mesh):
        if facet_markers[facet] != PHYS_SPHERE:
            continue

        mp = facet.midpoint()
        z = float(mp.x())
        r = float(mp.y())
        rho = float(np.hypot(z, r))
        theta = float(np.arctan2(r, z))  # [0, pi]

        # Касательный вектор к окружности в плоскости (z, r)
        tau_z = -r / rho
        tau_r = z / rho

        uz = float(u_z_h(Point(z, r)))
        ur = float(u_r_h(Point(z, r)))

        u_tau_h = tau_z * uz + tau_r * ur
        u_tau_exact = 3.0 * u_inf / (2.0 * (1.0 - a**3 / R**3)) * np.sin(theta)

        rows.append({
            "z": z,
            "r": r,
            "rho": rho,
            "theta": theta,
            "facet_length": _facet_length_2d(facet),
            "u_tau_h": u_tau_h,
            "u_tau_exact": u_tau_exact,
            "abs_error": abs(u_tau_h - u_tau_exact),
        })

    df = pd.DataFrame(rows).sort_values("theta").reset_index(drop=True)

    if len(df) == 0:
        raise RuntimeError("Не удалось извлечь данные на границе шара.")

    return df


def save_tangential_velocity_plot(df: pd.DataFrame, outpath: Path):
    fig, ax = plt.subplots(figsize=(7.5, 4.5))
    ax.plot(df["theta"], df["u_tau_exact"], linewidth=2.2, label="Точное решение")
    ax.plot(
        df["theta"],
        df["u_tau_h"],
        "o-",
        markersize=3.5,
        linewidth=1.2,
        label="Численное решение",
    )
    ax.set_xlabel(r"$\theta$")
    ax.set_ylabel(r"$u_\tau(\theta)$")
    ax.set_title("Касательная скорость на поверхности шара")
    ax.grid(True, alpha=0.25)
    ax.legend()
    fig.tight_layout()
    fig.savefig(outpath, dpi=180)
    plt.close(fig)


def save_summary(
    outdir: Path,
    mesh,
    err_L2: float,
    err_H1: float,
    df_tau: pd.DataFrame,
    a: float,
    R: float,
    u_inf: float,
    p: int,
):
    weights = df_tau["facet_length"].to_numpy()
    errs = df_tau["abs_error"].to_numpy()

    tau_err_linf = float(np.max(errs))
    tau_err_l2 = float(np.sqrt(np.sum((errs**2) * weights) / np.sum(weights)))

    summary = {
        "a": a,
        "R": R,
        "u_inf": u_inf,
        "p": p,
        "num_cells": int(mesh.num_cells()),
        "num_vertices": int(mesh.num_vertices()),
        "err_L2_psi": float(err_L2),
        "err_H1_psi": float(err_H1),
        "tau_err_Linf": tau_err_linf,
        "tau_err_L2_boundary": tau_err_l2,
    }

    with open(outdir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)


def generate_all_outputs(
    outdir: Path,
    mesh,
    facet_markers,
    psi_h,
    psi_exact,
    err_L2: float,
    err_H1: float,
    a: float,
    R: float,
    u_inf: float,
    p: int,
):
    outdir.mkdir(parents=True, exist_ok=True)

    _save_mesh_plot(mesh, outdir / "mesh.png")
    _save_scalar_field_plot(
        mesh, psi_h, r"Численное решение $\psi_h$", outdir / "psi_h.png"
    )
    _save_scalar_field_plot(
        mesh,
        psi_exact,
        r"Точное решение $\psi_{\mathrm{exact}}$",
        outdir / "psi_exact.png",
    )
    _save_error_plot(mesh, psi_h, psi_exact, outdir / "psi_error.png")

    df_tau = extract_tangential_velocity_on_sphere(
        mesh=mesh,
        facet_markers=facet_markers,
        psi_h=psi_h,
        a=a,
        R=R,
        u_inf=u_inf,
        degree=p,
    )
    df_tau.to_csv(outdir / "tangential_velocity.csv", index=False)
    save_tangential_velocity_plot(df_tau, outdir / "tangential_velocity.png")

    save_summary(
        outdir=outdir,
        mesh=mesh,
        err_L2=err_L2,
        err_H1=err_H1,
        df_tau=df_tau,
        a=a,
        R=R,
        u_inf=u_inf,
        p=p,
    )
