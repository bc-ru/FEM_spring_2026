import json
from pathlib import Path

import streamlit as st

st.title("7. Базовый вариант")

st.markdown(
    """
Рассматривается базовый вариант задачи:

- радиус шара: $(a = 1)$
- радиус внешней границы: $(R = 5)$

Ниже показаны результаты расчёта для выбранной сетки, а также
сравнение трёх последовательно сгущающихся сеток.
"""
)

st.latex(r"a = 1, \qquad R = 5")

mesh = st.selectbox(
    "Выбор сетки",
    ["coarse", "medium", "fine"],
    index=1,
)

base = Path(f"results/base/{mesh}/p2")
summary_path = base / "summary.json"

st.subheader("Параметры выбранного расчёта")

if summary_path.exists():
    with open(summary_path, "r", encoding="utf-8") as f:
        summary = json.load(f)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Сетка", mesh)
    c2.metric("Степень аппроксимации", summary.get("p", "—"))
    c3.metric("Число ячеек", summary.get("num_cells", "—"))
    c4.metric("Число узлов", summary.get("num_vertices", "—"))

    c5, c6 = st.columns(2)
    c5.metric(r"Ошибка $L_2(\psi)$", f"{summary.get('err_L2_psi', 0.0):.3e}")
    c6.metric(r"Ошибка $H^1(\psi)$", f"{summary.get('err_H1_psi', 0.0):.3e}")
else:
    st.warning(f"Файл не найден: {summary_path}")

st.caption(
    """
Для визуализации базового варианта используется аппроксимация полиномами степени \(p=2\).
Это позволяет сравнивать сетки при фиксированном порядке конечно-элементного пространства.
"""
)

tab1, tab2, tab3, tab4 = st.tabs([
    "Сетка",
    "Численное решение",
    "Точное решение",
    "Карта ошибки",
])

with tab1:
    img = base / "mesh.png"
    if img.exists():
        st.image(str(img), use_container_width=True)
    else:
        st.info(f"Файл не найден: {img}")

with tab2:
    img = base / "psi_h.png"
    if img.exists():
        st.image(str(img), use_container_width=True)
    else:
        st.info(f"Файл не найден: {img}")

with tab3:
    img = base / "psi_exact.png"
    if img.exists():
        st.image(str(img), use_container_width=True)
    else:
        st.info(f"Файл не найден: {img}")

with tab4:
    img = base / "psi_error.png"
    if img.exists():
        st.image(str(img), use_container_width=True)
    else:
        st.info(f"Файл не найден: {img}")

st.divider()

st.subheader("Сравнение расчётных сеток")

st.caption(
    """
Ниже показаны три последовательно сгущающиеся сетки для базового варианта.
Сравнение проводится для одного и того же случая $(a=1,\; R=5)$.
"""
)

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
        st.markdown(f"**{mesh_title}**")

        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        else:
            st.warning(f"Не найден файл:\n{img_path}")

        if summary_path.exists():
            with open(summary_path, "r", encoding="utf-8") as f:
                s = json.load(f)

            st.metric("Ячейки", s.get("num_cells", "—"))
            st.metric("Узлы", s.get("num_vertices", "—"))
        else:
            st.info("summary.json не найден")

st.caption(
    """
Обозначения:  
**coarse** — грубая сетка,  
**medium** — средняя сетка,  
**fine** — подробная сетка.
"""
)

st.divider()

st.subheader("Сравнение численного решения на трёх сетках")

st.caption(
    """
Ниже приведено поле функции тока $(\psi_h)$ для трёх сеток базового варианта.
Это позволяет визуально оценить влияние сгущения сетки на структуру решения.
"""
)

cols = st.columns(3)

for col, (mesh_key, mesh_title) in zip(cols, mesh_specs):
    img_path = Path(f"results/base/{mesh_key}/p2/psi_h.png")

    with col:
        st.markdown(f"**{mesh_title}**")
        if img_path.exists():
            st.image(str(img_path), use_container_width=True)
        else:
            st.warning(f"Не найден файл:\n{img_path}")