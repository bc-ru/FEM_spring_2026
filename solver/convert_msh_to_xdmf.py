from pathlib import Path
import numpy as np
import meshio


def collect_cells_and_data(mesh, cell_type: str, data_name: str = "gmsh:physical"):
    """
    Собирает все блоки ячеек заданного типа и соответствующие им cell_data,
    после чего склеивает их в один массив.

    Это корректно работает для .msh с несколькими блоками одного типа
    (типичная ситуация для Gmsh 4.x).
    """
    cells = []
    cell_data = []

    if data_name not in mesh.cell_data:
        raise RuntimeError(f"В mesh.cell_data отсутствует ключ '{data_name}'.")

    # mesh.cells и mesh.cell_data[data_name] согласованы по индексам блоков
    for cell_block, data_block in zip(mesh.cells, mesh.cell_data[data_name]):
        if cell_block.type == cell_type:
            cells.append(cell_block.data)
            cell_data.append(np.asarray(data_block, dtype=np.int32))

    if not cells:
        return None, None

    cells = np.vstack(cells)
    cell_data = np.concatenate(cell_data)

    if len(cells) != len(cell_data):
        raise RuntimeError(
            f"Несогласованные размеры для типа '{cell_type}': "
            f"{len(cells)} ячеек против {len(cell_data)} меток."
        )

    return cells, cell_data


def main():
    input_path = Path("meshes/sphere.msh")
    domain_path = Path("meshes/sphere_domain.xdmf")
    facets_path = Path("meshes/sphere_facets.xdmf")

    msh = meshio.read(input_path)

    triangle_cells, triangle_data = collect_cells_and_data(msh, "triangle")
    line_cells, line_data = collect_cells_and_data(msh, "line")

    if triangle_cells is None:
        raise RuntimeError("В .msh не найдены треугольные элементы.")
    if line_cells is None:
        raise RuntimeError("В .msh не найдены линейные граничные элементы.")

    points_2d = msh.points[:, :2]

    triangle_mesh = meshio.Mesh(
        points=points_2d,
        cells=[("triangle", triangle_cells)],
        cell_data={"name_to_read": [triangle_data]},
    )

    line_mesh = meshio.Mesh(
        points=points_2d,
        cells=[("line", line_cells)],
        cell_data={"name_to_read": [line_data]},
    )

    meshio.write(domain_path, triangle_mesh)
    meshio.write(facets_path, line_mesh)

    print(f"Сохранено: {domain_path}")
    print(f"Сохранено: {facets_path}")
    print(f"Triangles: {len(triangle_cells)}")
    print(f"Lines: {len(line_cells)}")


if __name__ == "__main__":
    main()