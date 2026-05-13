#!/usr/bin/env python3
"""Convert a Gmsh .msh file to XDMF files readable by FEniCS legacy.

Outputs:
    <out-prefix>_mesh.xdmf    triangular cells
    <out-prefix>_facets.xdmf  line facets with physical tags
"""
from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List, Tuple

import meshio
import numpy as np


def _collect_cells(msh: meshio.Mesh, cell_type: str) -> Tuple[np.ndarray, np.ndarray]:
    cells: List[np.ndarray] = []
    tags: List[np.ndarray] = []

    for idx, block in enumerate(msh.cells):
        if block.type != cell_type:
            continue
        cells.append(block.data)

        physical = None
        if "gmsh:physical" in msh.cell_data:
            physical = msh.cell_data["gmsh:physical"][idx]
        if physical is None:
            physical = np.zeros(len(block.data), dtype=np.int64)
        tags.append(np.asarray(physical, dtype=np.int64))

    if not cells:
        raise RuntimeError(f"No cells of type {cell_type!r} found in mesh")

    return np.vstack(cells), np.concatenate(tags)


def convert(msh_path: Path, out_prefix: Path) -> None:
    msh = meshio.read(msh_path)
    points = np.asarray(msh.points[:, :2], dtype=float)

    triangles, triangle_tags = _collect_cells(msh, "triangle")
    lines, line_tags = _collect_cells(msh, "line")

    out_prefix.parent.mkdir(parents=True, exist_ok=True)

    meshio.write(
        out_prefix.with_name(out_prefix.name + "_mesh.xdmf"),
        meshio.Mesh(
            points=points,
            cells=[("triangle", triangles)],
            cell_data={"name_to_read": [triangle_tags]},
        ),
    )
    meshio.write(
        out_prefix.with_name(out_prefix.name + "_facets.xdmf"),
        meshio.Mesh(
            points=points,
            cells=[("line", lines)],
            cell_data={"name_to_read": [line_tags]},
        ),
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("msh", type=Path)
    parser.add_argument("out_prefix", type=Path)
    args = parser.parse_args()
    convert(args.msh, args.out_prefix)


if __name__ == "__main__":
    main()
