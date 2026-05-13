from __future__ import annotations

import math
from pathlib import Path
from typing import Iterable

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
MESHES = ROOT / "meshes"
FIGS = RESULTS / "figs"

st.set_page_config(page_title="ЛР3: вихре-потенциальное течение", layout="wide")

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.2rem; padding-bottom: 2rem;}
    div[data-testid="stDataFrame"] {font-size: 0.82rem;}
    div[data-testid="stMetricValue"] {font-size: 1.25rem;}
    .small-note {font-size: 0.85rem; color: #666;}
    </style>
    """,
    unsafe_allow_html=True,
)


def _try_import_matplotlib():
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon

        return plt, Polygon
    except Exception as exc:  # pragma: no cover - UI fallback
        st.error(f"Matplotlib недоступен: {exc}")
        return None, None


def draw_geometry(L: float, H: float, l: float, h: float):
    """Draw the backward-facing-step geometry used by geo/step_channel.geo.tpl."""
    plt, Polygon = _try_import_matplotlib()
    if plt is None:
        return None

    pts = [(-l, 0.0), (0.0, 0.0), (0.0, -h), (L, -h), (L, H), (-l, H)]
    fig, ax = plt.subplots(figsize=(8, 3.6))
    patch = Polygon(pts, closed=True, fill=False, linewidth=2.2)
    ax.add_patch(patch)

    xs, ys = zip(*(pts + [pts[0]]))
    ax.plot(xs, ys, linewidth=1.5)
    ax.scatter(xs[:-1], ys[:-1], s=18)

    # Boundary labels. These correspond to Physical Curve IDs in problem.py.
    ax.text(-l / 2, H + 0.06 * (H + h), r"$\Gamma_3$: вход", ha="center", va="bottom")
    ax.text(
        L + 0.03 * (L + l), (H - h) / 2, r"$\Gamma_4$: выход", ha="left", va="center"
    )
    ax.text(
        (L - l) / 2,
        H + 0.16 * (H + h),
        r"$\Gamma_2$: верхняя стенка, $\boldsymbol{\psi}=H$",
        ha="center",
    )
    ax.text(
        L / 2,
        -h - 0.12 * (H + h),
        r"$\Gamma_1$: нижняя стенка, $\boldsymbol{\psi}=0$",
        ha="center",
    )
    ax.text(0.06 * (L + l), -h / 2, "уступ", ha="left", va="center")

    ax.set_aspect("equal", adjustable="box")
    pad_x = 0.08 * (L + l)
    pad_y = 0.18 * (H + h)
    ax.set_xlim(-l - pad_x, L + pad_x)
    ax.set_ylim(-h - pad_y, H + pad_y)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.25)
    ax.set_title("Геометрическая модель канала с уступом")
    fig.tight_layout()
    return fig


def plot_msh(path: Path, max_edges: int = 30_000):
    """Plot a 2D triangular Gmsh mesh from .msh using meshio."""
    try:
        import meshio
        import matplotlib.pyplot as plt
        import matplotlib.tri as mtri
    except Exception as exc:  # pragma: no cover - UI fallback
        st.error(f"Для просмотра .msh нужна связка meshio + matplotlib: {exc}")
        return None

    mesh = meshio.read(path)
    tri_cells = None
    for block in mesh.cells:
        if block.type == "triangle":
            tri_cells = block.data
            break
    if tri_cells is None:
        st.warning("В выбранном .msh не найдены треугольные элементы.")
        return None

    points = mesh.points[:, :2]
    if len(tri_cells) > max_edges:
        # Rendering a huge mesh in Streamlit is slow; decimate only for preview.
        step = max(1, len(tri_cells) // max_edges)
        tri_preview = tri_cells[::step]
        title_suffix = f"; показан каждый {step}-й элемент"
    else:
        tri_preview = tri_cells
        title_suffix = ""

    triang = mtri.Triangulation(points[:, 0], points[:, 1], tri_preview)
    fig, ax = plt.subplots(figsize=(8, 3.6))
    ax.triplot(triang, linewidth=0.35)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.2)
    ax.set_title(f"Сетка: {path.name} ({len(tri_cells)} треугольников{title_suffix})")
    fig.tight_layout()
    return fig


def load_metrics() -> pd.DataFrame:
    metric_files = sorted(RESULTS.glob("**/metrics.csv"))
    frames = []
    for f in metric_files:
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        df.insert(0, "case", str(f.parent.relative_to(RESULTS)))
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def compact_metrics(df: pd.DataFrame) -> pd.DataFrame:
    cols = [
        "case",
        "converged",
        "Gamma",
        "degree",
        "h",
        "num_cells",
        "dofs",
        "iterations",
        "omega",
        "vortex_area",
        "circulation_error_abs",
        "psi_min",
        "psi_max",
        "wall_time_sec",
    ]
    cols = [c for c in cols if c in df.columns]
    out = df[cols].copy()
    for c in [
        "omega",
        "vortex_area",
        "circulation_error_abs",
        "psi_min",
        "psi_max",
        "wall_time_sec",
    ]:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce").map(
                lambda x: f"{x:.4g}" if pd.notna(x) else ""
            )
    return out


def metric_cards(row: pd.Series):
    cols = st.columns(5)
    items = [
        ("Сходимость", "да" if int(row.get("converged", 0)) else "нет"),
        ("Итерации", row.get("iterations", "—")),
        ("ω", row.get("omega", "—")),
        ("Площадь ψ<0", row.get("vortex_area", "—")),
        ("DOF", row.get("dofs", "—")),
    ]
    for col, (name, value) in zip(cols, items):
        if isinstance(value, float):
            value = f"{value:.5g}"
        col.metric(name, value)


def image_files_for_case(case: str) -> list[Path]:
    case_dir = RESULTS / case
    imgs = []
    if case_dir.exists():
        imgs.extend(sorted(case_dir.glob("*.png")))
        imgs.extend(sorted((case_dir / "figs").glob("*.png")))
    return imgs


def show_images_grid(paths: Iterable[Path], columns: int = 2):
    paths = list(paths)
    if not paths:
        return
    cols = st.columns(columns)
    for i, path in enumerate(paths):
        with cols[i % columns]:
            st.image(
                str(path), caption=str(path.relative_to(ROOT)), use_container_width=True
            )


with st.sidebar:
    st.title("ЛР3")
    page = st.radio(
        "Раздел",
        [
            "1. Обзор",
            "2. Геометрия",
            "3. Сетка",
            "4. Математическая модель",
            "5. Алгоритм",
            "6. Результаты",
            "7. Файлы и запуск",
        ],
    )
    st.divider()
    st.caption("Проект: fenics-legacy + Gmsh + Streamlit")


if page == "1. Обзор":
    st.title("Численное исследование вихре-потенциального течения в канале с уступом")
    st.markdown(
        r"""
        Цель работы — построить конечно-элементный алгоритм для задачи со свободной
        вихревой областью, где знак функции тока определяет тип течения:

        $$
        \boldsymbol{\psi}>0 \Rightarrow \text{потенциальное течение},\qquad
        \boldsymbol{\psi}<0 \Rightarrow \text{вихревое течение}.
        $$
        """
    )

    c1, c2, c3 = st.columns(3)
    c1.info("**Геометрия**\n\nКанал с уступом, параметризованный `.geo` файлом Gmsh.")
    c2.info("**Модель**\n\nНелинейная задача для функции тока через область `ψ < 0`.")
    c3.info(
        "**Эксперименты**\n\nСетки, степени `p=1,2,3`, значения `Γ`, высоты уступа `h`."
    )

    st.subheader("Базовый вариант")
    base = pd.DataFrame([
        {"L": 4.0, "H": 1.0, "l": 1.0, "h": 1.0, "Gamma": -2.0, "p": "1, 2, 3"}
    ])
    st.dataframe(base, hide_index=True, use_container_width=True)

    st.subheader("Что показывать на защите")
    st.markdown(
        """
        - геометрическая область и физические группы границ;
        - вид сетки и сгущение около уступа;
        - постановка через функцию тока и граничные условия;
        - итерационный алгоритм для свободной вихревой области;
        - таблицы метрик: `omega`, `vortex_area`, `iterations`, `circulation_error_abs`;
        - поля `psi`, `indicator`, `omega`, `velocity` в ParaView или PNG-экспорте.
        """
    )

elif page == "2. Геометрия":
    st.title("Геометрическая модель")
    st.markdown(
        r"""
        Используется область типа backward-facing step. В текущем `.geo` шаблоне
        контур задаётся точками

        $$
        (-l,0)\to(0,0)\to(0,-h)\to(L,-h)\to(L,H)\to(-l,H).
        $$

        Поэтому полная высота выходного сечения равна $H+h$.
        """
    )

    left, right = st.columns([1, 2])
    with left:
        st.subheader("Параметры чертежа")
        L = st.number_input("L", min_value=0.5, max_value=20.0, value=4.0, step=0.25)
        H = st.number_input("H", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        l = st.number_input("l", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
        h = st.number_input("h", min_value=0.1, max_value=10.0, value=1.0, step=0.1)
    with right:
        fig = draw_geometry(L, H, l, h)
        if fig is not None:
            st.pyplot(fig, clear_figure=True)

    st.subheader("Граничные условия")
    bc = pd.DataFrame([
        {
            "Граница": "Γ₃ / inlet",
            "Physical ID": 13,
            "Условие": "ψ = x₂",
            "Тип": "Dirichlet",
        },
        {
            "Граница": "Γ₄ / outlet",
            "Physical ID": 14,
            "Условие": "∂ψ/∂n = 0",
            "Тип": "Neumann, естественное",
        },
        {
            "Граница": "нижняя стенка + уступ",
            "Physical ID": "11, 15",
            "Условие": "ψ = 0",
            "Тип": "Dirichlet",
        },
        {
            "Граница": "верхняя стенка",
            "Physical ID": 12,
            "Условие": "ψ = H",
            "Тип": "Dirichlet",
        },
    ])
    st.dataframe(bc, hide_index=True, use_container_width=True)

    with st.expander("Фрагмент генерации .geo"):
        geo_tpl = ROOT / "geo" / "step_channel.geo.tpl"
        if geo_tpl.exists():
            st.code(geo_tpl.read_text(encoding="utf-8"), language="geo")
        else:
            st.warning("Файл geo/step_channel.geo.tpl не найден.")

elif page == "3. Сетка":
    st.title("Расчётная сетка")
    st.markdown(
        """
        Сетка строится в Gmsh. На этой странице можно просмотреть готовые `.msh`
        файлы из каталога `meshes/`. Если `.msh` отсутствует, сначала выполните
        генерацию сетки из README.
        """
    )

    msh_files = sorted(MESHES.glob("**/*.msh"))
    png_meshes = sorted(MESHES.glob("**/*.png")) + sorted(FIGS.glob("*mesh*.png"))

    st.subheader("Доступные mesh-файлы")
    if not msh_files:
        st.warning("В каталоге meshes/ не найдено `.msh` файлов.")
        st.code(
            """python3 geo/generate_geo.py --L 4 --H 1 --l 1 --h 1 --lc 0.08 --out meshes/base/step_channel.geo
gmsh -2 meshes/base/step_channel.geo -format msh2 -o meshes/base/step_channel.msh""",
            language="bash",
        )
    else:
        selected = st.selectbox(
            "Выберите сетку", msh_files, format_func=lambda p: str(p.relative_to(ROOT))
        )
        fig = plot_msh(selected)
        if fig is not None:
            st.pyplot(fig, clear_figure=True)
        st.caption(
            "Для очень больших сеток предпросмотр может быть прорежен, но расчётная сетка не изменяется."
        )

    if png_meshes:
        st.subheader("Сохранённые изображения сеток")
        show_images_grid(png_meshes, columns=2)

    st.subheader("План сгущения")
    mesh_plan = pd.DataFrame([
        {"Сетка": "coarse", "lc": 0.08, "Ожидание": "начальный расчёт"},
        {"Сетка": "medium", "lc": 0.04, "Ожидание": "примерно ×4 элементов"},
        {
            "Сетка": "fine",
            "lc": 0.02,
            "Ожидание": "примерно ×16 элементов относительно coarse",
        },
    ])
    st.dataframe(mesh_plan, hide_index=True, use_container_width=True)

elif page == "4. Математическая модель":
    st.title("Математическая модель")
    st.markdown(
        r"""
        Основная неизвестная — функция тока $\boldsymbol{\psi}$. Скорость восстанавливается как

        $$
        \mathbf v = \left(\frac{\partial\boldsymbol{\psi}}{\partial y},
        -\frac{\partial\boldsymbol{\psi}}{\partial x}\right).
        $$

        Вихрь скорости:

        $$
        \boldsymbol{\omega} = \frac{\partial v_2}{\partial x} - \frac{\partial v_1}{\partial y}.
        $$

        Для выбранной модели решается задача

        $$
        -\Delta\boldsymbol{\psi}=\boldsymbol{\omega}(\boldsymbol{\psi}),\qquad x\in\Omega.
        $$

        Постоянная завихренность внутри вихревой зоны задаётся через циркуляцию:

        $$
        \boldsymbol{\omega}^k = \frac{\Gamma}{|\Omega_v^k|},\qquad
        |\Omega_v^k| = \int_\Omega I(\boldsymbol{\psi}^k<0)\,dx.
        $$
        """
    )

    st.subheader("Слабая форма")
    st.markdown(
        r"""
        Для тестовой функции $\boldsymbol{\varphi}$:

        $$
        \int_\Omega \nabla\boldsymbol{\psi}^{k+1}\cdot\nabla\boldsymbol{\varphi}\,dx
        = \int_\Omega \boldsymbol{\omega}^k I(\boldsymbol{\psi}^k<0)\boldsymbol{\varphi}\,dx.
        $$

        Условие на выходе $\partial\boldsymbol{\psi}/\partial n=0$ является естественным и не
        добавляет отдельного члена в правую часть.
        """
    )

elif page == "5. Алгоритм":
    st.title("Вычислительный алгоритм")
    st.markdown(
        r"""
        На каждой итерации решается линейная задача Пуассона с правой частью,
        вычисленной по предыдущему приближению.
        """
    )

    st.code(
        """psi_old = initial_guess()
for k in range(max_iter):
    indicator = 1 if psi_old < 0 else 0      # DG0, по ячейкам
    vortex_area = assemble(indicator * dx)
    omega = Gamma / vortex_area

    solve( inner(grad(psi_new), grad(v))*dx == omega*indicator*v*dx )

    psi_relaxed = (1 - alpha)*psi_old + alpha*psi_new
    check ||psi_relaxed - psi_old|| and |omega - omega_old|
    psi_old = psi_relaxed""",
        language="python",
    )

    st.subheader("Диагностические величины")
    diagnostics = pd.DataFrame([
        {
            "Величина": "vortex_area",
            "Формула": "∫ I(ψ<0) dx",
            "Назначение": "площадь вихревой зоны",
        },
        {
            "Величина": "omega",
            "Формула": "Γ / vortex_area",
            "Назначение": "постоянная завихренность",
        },
        {
            "Величина": "circulation_check",
            "Формула": "omega · vortex_area",
            "Назначение": "должно совпадать с Γ",
        },
        {
            "Величина": "err_psi_last",
            "Формула": "||ψᵏ⁺¹-ψᵏ|| / ||ψᵏ⁺¹||",
            "Назначение": "критерий остановки",
        },
    ])
    st.dataframe(diagnostics, hide_index=True, use_container_width=True)

elif page == "6. Результаты":
    st.title("Результаты расчётов")
    all_metrics = load_metrics()
    if all_metrics.empty:
        st.warning(
            "Пока нет файлов results/**/metrics.csv. Сначала запустите один расчёт или серию экспериментов."
        )
        st.code("python3 experiments/run_base_meshes.py", language="bash")
    else:
        with st.sidebar:
            st.divider()
            st.subheader("Фильтр результатов")
            cases = sorted(all_metrics["case"].unique())
            selected_cases = st.multiselect("cases", cases, default=cases)
            degrees = (
                sorted(all_metrics["degree"].dropna().unique())
                if "degree" in all_metrics
                else []
            )
            selected_degrees = st.multiselect("degree", degrees, default=degrees)

        df = all_metrics[all_metrics["case"].isin(selected_cases)].copy()
        if selected_degrees and "degree" in df:
            df = df[df["degree"].isin(selected_degrees)]

        tab_summary, tab_case, tab_plots, tab_images, tab_full = st.tabs([
            "Кратко",
            "Один расчёт",
            "Графики",
            "Изображения",
            "Полная таблица",
        ])

        with tab_summary:
            st.subheader("Компактная таблица")
            st.dataframe(
                compact_metrics(df),
                hide_index=True,
                use_container_width=True,
                height=360,
            )

            st.subheader("Агрегация по группам")
            group_cols = [c for c in ["degree", "Gamma", "h"] if c in df.columns]
            if group_cols:
                group_by = st.selectbox("Группировать по", group_cols)
                numeric_cols = [
                    c
                    for c in [
                        "omega",
                        "vortex_area",
                        "iterations",
                        "dofs",
                        "wall_time_sec",
                    ]
                    if c in df.columns
                ]
                agg = (
                    df
                    .groupby(group_by)[numeric_cols]
                    .mean(numeric_only=True)
                    .reset_index()
                )
                st.dataframe(agg, hide_index=True, use_container_width=True)

        with tab_case:
            case = st.selectbox("Выберите расчёт", sorted(df["case"].unique()))
            row = df[df["case"] == case].iloc[0]
            metric_cards(row)
            st.subheader("Параметры и метрики выбранного расчёта")
            one = (
                row
                .to_frame(name="value")
                .reset_index()
                .rename(columns={"index": "field"})
            )
            st.dataframe(one, hide_index=True, use_container_width=True, height=480)

        with tab_plots:
            numeric = df.select_dtypes(include="number")
            if numeric.empty:
                st.info("Нет числовых столбцов для графиков.")
            else:
                c1, c2 = st.columns(2)
                x_col = c1.selectbox("Ось x", ["case"] + list(numeric.columns), index=0)
                y_col = c2.selectbox(
                    "Ось y",
                    list(numeric.columns),
                    index=list(numeric.columns).index("omega")
                    if "omega" in numeric
                    else 0,
                )
                plot_df = (
                    df[[x_col, y_col]].copy()
                    if x_col != "case"
                    else df[["case", y_col]].copy()
                )
                plot_df = plot_df.sort_values(x_col) if x_col != "case" else plot_df
                st.line_chart(plot_df, x=x_col, y=y_col)

                st.markdown(
                    "**Рекомендуемые пары:** `num_cells → omega`, `degree → omega`, `Gamma → vortex_area`, `h → vortex_area`."
                )

        with tab_images:
            case = st.selectbox(
                "Изображения для расчёта", sorted(df["case"].unique()), key="image_case"
            )
            imgs = image_files_for_case(case)
            if imgs:
                show_images_grid(imgs, columns=2)
            else:
                st.warning(
                    "Для этого расчёта нет PNG-изображений. XDMF-файлы можно открыть в ParaView."
                )
                st.markdown(
                    "После обновления solver изображения будут автоматически сохраняться в `results/<case>/figs/`, если установлен `matplotlib`."
                )

        with tab_full:
            st.subheader("Полная таблица")
            st.dataframe(df, use_container_width=True, height=520)
            st.download_button(
                "Скачать отфильтрованные метрики CSV",
                df.to_csv(index=False).encode("utf-8"),
                file_name="filtered_metrics.csv",
                mime="text/csv",
            )

elif page == "7. Файлы и запуск":
    st.title("Файлы и запуск")
    st.subheader("Быстрый запуск")
    st.code(
        """python3 geo/generate_geo.py --L 4 --H 1 --l 1 --h 1 --lc 0.08 --out meshes/base/step_channel.geo
gmsh -2 meshes/base/step_channel.geo -format msh2 -o meshes/base/step_channel.msh
python3 solver/mesh_convert.py meshes/base/step_channel.msh meshes/base/step_channel
python3 solver/run_case.py \
  --mesh-prefix meshes/base/step_channel \
  --out results/base/p1_Gamma-2 \
  --L 4 --H 1 --l 1 --h 1 --Gamma -2 --degree 1 --alpha 0.5
streamlit run app/presentation.py""",
        language="bash",
    )

    st.subheader("Файлы результатов")
    files = sorted(RESULTS.glob("**/*"))
    files = [f for f in files if f.is_file()]
    if not files:
        st.info("Файлов результатов пока нет.")
    else:
        file_df = pd.DataFrame([
            {
                "file": str(f.relative_to(ROOT)),
                "size_kb": round(f.stat().st_size / 1024, 1),
            }
            for f in files
        ])
        st.dataframe(file_df, hide_index=True, use_container_width=True, height=480)
