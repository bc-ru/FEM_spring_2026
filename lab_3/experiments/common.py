from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]


def run(cmd: Iterable[str]) -> None:
    cmd = list(map(str, cmd))
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, cwd=str(ROOT))


def make_mesh(name: str, L: float, H: float, l: float, h: float, lc: float) -> Path:
    geo_path = Path("meshes") / name / "step_channel.geo"
    msh_path = Path("meshes") / name / "step_channel.msh"
    prefix = Path("meshes") / name / "step_channel"
    (ROOT / geo_path).parent.mkdir(parents=True, exist_ok=True)

    run([
        "python3", "geo/generate_geo.py",
        "--L", L, "--H", H, "--l", l, "--h", h,
        "--lc", lc,
        "--out", geo_path,
    ])
    run(["gmsh", "-2", geo_path, "-format", "msh2", "-o", msh_path])
    run(["python3", "solver/mesh_convert.py", msh_path, prefix])
    return ROOT / prefix
