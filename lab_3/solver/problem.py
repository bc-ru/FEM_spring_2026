"""Numerical constants and parameter containers for lab 3."""
from __future__ import annotations

from dataclasses import dataclass

# Boundary tags. Must match geo/step_channel.geo.tpl.
WALL_LOWER = 11
WALL_TOP = 12
INLET = 13
OUTLET = 14
STEP = 15


@dataclass(frozen=True)
class CaseParameters:
    L: float = 4.0
    H: float = 1.0
    l: float = 1.0
    h: float = 1.0
    Gamma: float = -2.0
    degree: int = 1
    alpha: float = 0.5
    tol_psi: float = 1.0e-8
    tol_omega: float = 1.0e-8
    max_iter: int = 200
    inlet_scale: float = 1.0
    initial_eps: float = 0.05
    initial_vortex_x: float = 2.0
    omega_model: str = "constant"
    omega_power: float = 0.0
