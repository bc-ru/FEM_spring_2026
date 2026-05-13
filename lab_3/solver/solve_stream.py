"""FEniCS legacy solver for vortex-potential flow in a stepped channel.

The nonlinear/free-boundary part is solved by Picard-type iterations:

    -Delta psi^{k+1} = omega^k * I(psi^k < 0),
    omega^k = Gamma / integral I(psi^k < 0) dx.

The zero-Neumann outlet condition is natural in the weak form.
"""
from __future__ import annotations

import csv
import json
import math
import time
from pathlib import Path
from typing import Dict, Tuple

from dolfin import *  # noqa: F403,F401 - conventional FEniCS legacy import

try:
    from .problem import CaseParameters, INLET, WALL_LOWER, WALL_TOP
except ImportError:  # direct script execution fallback
    from problem import CaseParameters, INLET, WALL_LOWER, WALL_TOP


DOLFIN_EPS_AREA = 1.0e-14


def read_mesh(prefix: str | Path) -> Tuple[Mesh, MeshFunction]:
    prefix = Path(prefix)
    mesh = Mesh()
    with XDMFFile(str(prefix.with_name(prefix.name + "_mesh.xdmf"))) as infile:
        infile.read(mesh)

    mvc = MeshValueCollection("size_t", mesh, mesh.topology().dim() - 1)
    with XDMFFile(str(prefix.with_name(prefix.name + "_facets.xdmf"))) as infile:
        infile.read(mvc, "name_to_read")
    facets = MeshFunction("size_t", mesh, mvc)
    return mesh, facets


def make_boundary_conditions(V: FunctionSpace, facets: MeshFunction, params: CaseParameters):
    inlet_value = Expression("inlet_scale*x[1]", inlet_scale=params.inlet_scale, degree=max(1, params.degree + 1))
    bc_inlet = DirichletBC(V, inlet_value, facets, INLET)
    bc_lower = DirichletBC(V, Constant(0.0), facets, WALL_LOWER)
    bc_top = DirichletBC(V, Constant(params.H), facets, WALL_TOP)
    return [bc_inlet, bc_lower, bc_top]


def solve_potential(V: FunctionSpace, bcs) -> Function:
    u = TrialFunction(V)
    v = TestFunction(V)
    psi = Function(V, name="psi_potential")
    solve(inner(grad(u), grad(v)) * dx == Constant(0.0) * v * dx, psi, bcs)
    return psi


def initial_guess(V: FunctionSpace, potential: Function, params: CaseParameters) -> Function:
    """Create an initial field with a small negative patch behind the step.

    This is only used to initialize the free-boundary iteration. The first PDE solve
    immediately reimposes the Dirichlet boundary conditions.
    """
    psi = Function(V, name="psi_initial")
    psi.assign(potential)
    if params.initial_eps <= 0:
        return psi

    perturb = interpolate(
        Expression(
            "(x[0] >= 0.0 && x[0] <= xv && x[1] <= 0.0) ? -eps : 0.0",
            xv=params.initial_vortex_x,
            eps=params.initial_eps,
            degree=1,
        ),
        V,
    )
    psi.vector().axpy(1.0, perturb.vector())
    psi.vector().apply("insert")
    return psi


def build_indicator(psi: Function, Q: FunctionSpace) -> Function:
    mesh = Q.mesh()
    indicator = Function(Q, name="vortex_indicator")
    values = indicator.vector().get_local()
    dofmap = Q.dofmap()
    for cell in cells(mesh):
        dof = dofmap.cell_dofs(cell.index())[0]
        values[dof] = 1.0 if psi(cell.midpoint()) < 0.0 else 0.0
    indicator.vector().set_local(values)
    indicator.vector().apply("insert")
    return indicator


def l2_norm(u: Function) -> float:
    return math.sqrt(max(0.0, assemble(u * u * dx)))


def write_function_xdmf(path: Path, function: Function) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with XDMFFile(str(path)) as f:
        f.parameters["flush_output"] = True
        f.parameters["functions_share_mesh"] = True
        f.write(function)




def _mesh_triangulation(mesh: Mesh):
    """Return vertex coordinates and triangular cells for matplotlib previews."""
    import matplotlib.tri as mtri

    coords = mesh.coordinates()
    cells_array = mesh.cells()
    return coords, cells_array, mtri.Triangulation(coords[:, 0], coords[:, 1], cells_array)


def _save_scalar_vertex_plot(path: Path, mesh: Mesh, values, title: str, label: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    coords, _, triang = _mesh_triangulation(mesh)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    field = ax.tricontourf(triang, values, levels=32)
    ax.tricontour(triang, values, levels=[0.0], linewidths=1.4)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    fig.colorbar(field, ax=ax, label=label)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _save_cell_plot(path: Path, mesh: Mesh, cell_values, title: str, label: str) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _, _, triang = _mesh_triangulation(mesh)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    field = ax.tripcolor(triang, facecolors=cell_values, edgecolors="none")
    ax.triplot(triang, linewidth=0.12, alpha=0.35)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(title)
    fig.colorbar(field, ax=ax, label=label)
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def _save_mesh_plot(path: Path, mesh: Mesh, title: str = "Расчётная сетка") -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    _, _, triang = _mesh_triangulation(mesh)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.triplot(triang, linewidth=0.25)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title(f"{title}: {mesh.num_cells()} элементов")
    fig.tight_layout()
    fig.savefig(path, dpi=180)
    plt.close(fig)


def export_preview_figures(output_dir: Path, mesh: Mesh, psi: Function, indicator: Function, omega_field: Function, velocity: Function) -> None:
    """Export compact PNG previews for the Streamlit presentation.

    XDMF remains the primary scientific output. These PNG files are presentation
    artifacts: mesh, psi, vortex indicator, omega, and velocity magnitude.
    If matplotlib is unavailable, the solver simply skips preview generation.
    """
    try:
        figs_dir = output_dir / "figs"
        figs_dir.mkdir(parents=True, exist_ok=True)

        _save_mesh_plot(figs_dir / "mesh.png", mesh)

        psi_values = psi.compute_vertex_values(mesh)
        _save_scalar_vertex_plot(figs_dir / "psi.png", mesh, psi_values, "Функция тока ψ", "ψ")

        indicator_values = indicator.vector().get_local()
        _save_cell_plot(figs_dir / "indicator.png", mesh, indicator_values, "Вихревая область I(ψ<0)", "indicator")

        omega_values = omega_field.vector().get_local()
        _save_cell_plot(figs_dir / "omega.png", mesh, omega_values, "Поле завихренности ω", "ω")

        vel_values = velocity.compute_vertex_values(mesh)
        n = mesh.num_vertices()
        dim = mesh.geometry().dim()
        if len(vel_values) >= dim * n:
            mag2 = None
            for i in range(dim):
                comp = vel_values[i * n : (i + 1) * n]
                mag2 = comp * comp if mag2 is None else mag2 + comp * comp
            vel_mag = mag2 ** 0.5
            _save_scalar_vertex_plot(figs_dir / "velocity_magnitude.png", mesh, vel_mag, "Модуль скорости |v|", "|v|")
    except Exception as exc:  # preview export must never break the numerical run
        print(f"Warning: failed to export preview figures: {exc}")

def save_metrics_csv(path: Path, metrics: Dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(metrics.keys()))
        writer.writeheader()
        writer.writerow(metrics)


def solve_case(mesh_prefix: str | Path, params: CaseParameters, output_dir: str | Path) -> Dict[str, object]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    set_log_level(LogLevel.WARNING)
    mesh, facets = read_mesh(mesh_prefix)
    V = FunctionSpace(mesh, "CG", params.degree)
    Q = FunctionSpace(mesh, "DG", 0)
    bcs = make_boundary_conditions(V, facets, params)

    start_time = time.time()
    psi_potential = solve_potential(V, bcs)
    psi_old = initial_guess(V, psi_potential, params)

    u = TrialFunction(V)
    v = TestFunction(V)
    a = inner(grad(u), grad(v)) * dx

    omega_prev = None
    converged = False
    final_indicator = None
    final_omega = float("nan")
    final_area = 0.0
    err_psi = float("inf")
    err_omega = float("inf")
    iterations = 0

    for k in range(1, params.max_iter + 1):
        iterations = k
        indicator = build_indicator(psi_old, Q)
        vortex_area = float(assemble(indicator * dx))

        if vortex_area <= DOLFIN_EPS_AREA:
            raise RuntimeError(
                "Vortex area is zero. Increase --initial-eps or --initial-vortex-x."
            )

        omega = float(params.Gamma / vortex_area)
        rhs = omega * indicator * v * dx

        psi_new = Function(V, name="psi_new")
        solve(a == rhs, psi_new, bcs)

        psi_relaxed = Function(V, name="psi")
        psi_relaxed.vector()[:] = psi_old.vector() * (1.0 - params.alpha) + psi_new.vector() * params.alpha
        psi_relaxed.vector().apply("insert")

        diff = Function(V, name="psi_diff")
        diff.vector()[:] = psi_relaxed.vector() - psi_old.vector()
        diff.vector().apply("insert")
        denom = max(l2_norm(psi_relaxed), 1.0e-30)
        err_psi = l2_norm(diff) / denom

        if omega_prev is None:
            err_omega = float("inf")
        else:
            err_omega = abs(omega - omega_prev) / max(1.0, abs(omega))

        psi_old.assign(psi_relaxed)
        omega_prev = omega
        final_indicator = indicator
        final_omega = omega
        final_area = vortex_area

        if err_psi < params.tol_psi and err_omega < params.tol_omega:
            converged = True
            break

    psi = Function(V, name="psi")
    psi.assign(psi_old)
    indicator = build_indicator(psi, Q)
    vortex_area = float(assemble(indicator * dx))
    omega = float(params.Gamma / vortex_area) if vortex_area > DOLFIN_EPS_AREA else float("nan")
    omega_field = project(Constant(omega) * indicator, Q)
    omega_field.rename("omega", "omega")

    W = VectorFunctionSpace(mesh, "CG", max(1, params.degree - 1))
    velocity = project(as_vector((psi.dx(1), -psi.dx(0))), W)
    velocity.rename("velocity", "velocity")

    psi.rename("psi", "psi")
    indicator.rename("vortex_indicator", "vortex_indicator")

    write_function_xdmf(output_dir / "psi.xdmf", psi)
    write_function_xdmf(output_dir / "velocity.xdmf", velocity)
    write_function_xdmf(output_dir / "omega.xdmf", omega_field)
    write_function_xdmf(output_dir / "indicator.xdmf", indicator)

    export_preview_figures(output_dir, mesh, psi, indicator, omega_field, velocity)

    psi_values = psi.vector().get_local()
    metrics: Dict[str, object] = {
        "L": params.L,
        "H": params.H,
        "l": params.l,
        "h": params.h,
        "Gamma": params.Gamma,
        "degree": params.degree,
        "alpha": params.alpha,
        "num_cells": mesh.num_cells(),
        "num_vertices": mesh.num_vertices(),
        "dofs": V.dim(),
        "converged": int(converged),
        "iterations": iterations,
        "omega": omega,
        "vortex_area": vortex_area,
        "circulation_check": omega * vortex_area,
        "circulation_error_abs": abs(omega * vortex_area - params.Gamma),
        "psi_min": float(psi_values.min()),
        "psi_max": float(psi_values.max()),
        "err_psi_last": err_psi,
        "err_omega_last": err_omega,
        "wall_time_sec": time.time() - start_time,
    }

    save_metrics_csv(output_dir / "metrics.csv", metrics)
    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return metrics
