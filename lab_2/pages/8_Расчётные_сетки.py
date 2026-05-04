import json
from pathlib import Path

import streamlit as st

st.title("8. Расчётные сетки")

st.markdown(
    """
Для базового варианта используются три последовательно сгущающиеся сетки:
грубая, средняя и подробная. Эти сетки применяются для верификации
численного решения на последовательности разбиений.
"""
)

st.latex(r"a = 1, \qquad R = 5")

mesh_specs = [
    ("coarse", "Грубая сетка"),
    ("medium", "Средняя сетка"),
    ("fine", "Подробная сетка"),
]

cols = st.columns(3)

for col, (mesh_key, mesh_title) in zip(cols, mesh_specs):
    img_path = Path(f"results/base/{mesh_key}/p2/mesh.png")
    summary_path = Path(f"results/base/{mesh_key}/p2/summary.json")

    with col:
        st.subheader(mesh_title)

        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        else:
            st.warning(f"Не найден файл:\n{img_path}")

        if summary_path.exists():
            with open(summary_path, "r", encoding="utf-8") as f:
                summary = json.load(f)

            st.metric("Число ячеек", summary.get("num_cells", "—"))
            st.metric("Число узлов", summary.get("num_vertices", "—"))
        else:
            st.info("Файл summary.json пока не найден.")
