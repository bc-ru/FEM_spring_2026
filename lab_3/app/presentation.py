from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

import pandas as pd
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
MESHES = ROOT / "meshes"

st.set_page_config(page_title="ЛР3: вихре-потенциальное течение", layout="wide")

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.0rem; padding-bottom: 2rem; max-width: 1280px;}
    div[data-testid="stDataFrame"] {font-size: 0.80rem;}
    div[data-testid="stMetricValue"] {font-size: 1.15rem;}
    .src {font-size: 0.82rem; color: #555; border-left: 3px solid #bbb; padding-left: 0.75rem; margin: 0.4rem 0 0.8rem 0;}
    .tight {margin-bottom: 0.1rem;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Physical IDs used in geo/step_channel.geo.tpl and solver/problem.py.
WALL_LOWER = 11
WALL_TOP = 12
INLET = 13
OUTLET = 14
STEP = 15
DOMAIN = 1

SOURCE_MODEL = "Постановка задания: разделы «Геометрическая модель», «Математическая модель», «Задачи исследования»."
SOURCE_CODE = (
    "Реализация: geo/step_channel.geo.tpl, solver/solve_stream.py, experiments/*.py."
)


def source(text: str) -> None:
    st.markdown(f'<div class="src">Источник: {text}</div>', unsafe_allow_html=True)


def _try_import_matplotlib():
    try:
        import matplotlib.pyplot as plt
        from matplotlib.patches import Polygon

        return plt, Polygon
    except Exception as exc:  # pragma: no cover - UI fallback
        st.error(f"Matplotlib недоступен: {exc}")
        return None, None


def draw_geometry(L: float = 4.0, H: float = 1.0, l: float = 1.0, h: float = 1.0):
    """Draw the backward-facing-step geometry used by geo/step_channel.geo.tpl."""
    plt, Polygon = _try_import_matplotlib()
    if plt is None:
        return None

    pts = [(-l, 0.0), (0.0, 0.0), (0.0, -h), (L, -h), (L, H), (-l, H)]
    fig, ax = plt.subplots(figsize=(8.4, 3.7))
    patch = Polygon(pts, closed=True, fill=False, linewidth=2.1)
    ax.add_patch(patch)

    xs, ys = zip(*(pts + [pts[0]]))
    ax.plot(xs, ys, linewidth=1.4)
    ax.scatter(xs[:-1], ys[:-1], s=16)

    ax.text(-l / 2, H + 0.06 * (H + h), r"$\Gamma_3$ вход", ha="center", va="bottom")
    ax.text(
        L + 0.03 * (L + l), (H - h) / 2, r"$\Gamma_4$ выход", ha="left", va="center"
    )
    ax.text((L - l) / 2, H + 0.16 * (H + h), r"$\Gamma_2: \psi=H$", ha="center")
    ax.text((L) / 2, -h - 0.12 * (H + h), r"$\Gamma_1: \psi=0$", ha="center")
    ax.text(0.06 * (L + l), -h / 2, "уступ", ha="left", va="center")

    ax.set_aspect("equal", adjustable="box")
    pad_x = 0.08 * (L + l)
    pad_y = 0.18 * (H + h)
    ax.set_xlim(-l - pad_x, L + pad_x)
    ax.set_ylim(-h - pad_y, H + pad_y)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.22)
    ax.set_title("Расчётная область")
    fig.tight_layout()
    return fig


def plot_msh(path: Path, max_triangles: int = 28_000):
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
    if len(tri_cells) > max_triangles:
        step = max(1, len(tri_cells) // max_triangles)
        tri_preview = tri_cells[::step]
        suffix = f"; показан каждый {step}-й элемент"
    else:
        tri_preview = tri_cells
        suffix = ""

    triang = mtri.Triangulation(points[:, 0], points[:, 1], tri_preview)
    fig, ax = plt.subplots(figsize=(8.4, 3.7))
    ax.triplot(triang, linewidth=0.32)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True, alpha=0.18)
    ax.set_title(f"{path.name}: {len(tri_cells)} треугольников{suffix}")
    fig.tight_layout()
    return fig


def load_metrics() -> pd.DataFrame:
    metric_files = sorted(RESULTS.glob("**/metrics.csv"))
    frames: list[pd.DataFrame] = []
    for f in metric_files:
        try:
            df = pd.read_csv(f)
        except Exception:
            continue
        df.insert(0, "case", str(f.parent.relative_to(RESULTS)))
        frames.append(df)
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    for col in [
        "L",
        "H",
        "l",
        "h",
        "Gamma",
        "degree",
        "alpha",
        "num_cells",
        "dofs",
        "iterations",
        "omega",
        "vortex_area",
        "circulation_error_abs",
        "psi_min",
        "psi_max",
        "wall_time_sec",
    ]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def short_table(df: pd.DataFrame, cols: list[str]) -> pd.DataFrame:
    present = [c for c in cols if c in df.columns]
    out = df[present].copy()
    for c in [
        "omega",
        "vortex_area",
        "circulation_error_abs",
        "psi_min",
        "psi_max",
        "wall_time_sec",
        "err_psi_last",
        "err_omega_last",
    ]:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce").map(
                lambda x: f"{x:.5g}" if pd.notna(x) else ""
            )
    if "converged" in out.columns:
        out["converged"] = out["converged"].map(lambda x: "да" if int(x) else "нет")
    return out


def case_mask(df: pd.DataFrame, keys: Iterable[str]) -> pd.Series:
    if df.empty or "case" not in df:
        return pd.Series([], dtype=bool)
    mask = pd.Series(False, index=df.index)
    for key in keys:
        mask |= df["case"].astype(str).str.contains(key, case=False, regex=False)
    return mask


def show_numeric_line(df: pd.DataFrame, x: str, y: str) -> None:
    if df.empty or x not in df.columns or y not in df.columns:
        return
    plot_df = df[[x, y]].dropna().sort_values(x)
    if len(plot_df) >= 2:
        st.line_chart(plot_df, x=x, y=y, height=260)


def metric_cards(row: pd.Series) -> None:
    items = [
        ("Сходимость", "да" if int(row.get("converged", 0)) else "нет"),
        ("Итерации", row.get("iterations", "—")),
        ("ω", row.get("omega", "—")),
        ("|Ωᵥ|", row.get("vortex_area", "—")),
        ("DOF", row.get("dofs", "—")),
    ]
    cols = st.columns(len(items))
    for col, (name, value) in zip(cols, items):
        if isinstance(value, float):
            value = f"{value:.5g}"
        col.metric(name, value)


def image_files_for_case(case: str) -> list[Path]:
    case_dir = RESULTS / case
    if not case_dir.exists():
        return []
    imgs = []
    imgs.extend(sorted(case_dir.glob("*.png")))
    imgs.extend(sorted((case_dir / "figs").glob("*.png")))
    preferred = ["mesh", "psi", "indicator", "omega", "velocity_magnitude"]
    return sorted(
        imgs,
        key=lambda p: (preferred.index(p.stem) if p.stem in preferred else 99, p.name),
    )


def show_images_grid(paths: Iterable[Path], columns: int = 2) -> None:
    paths = list(paths)
    if not paths:
        return
    cols = st.columns(columns)
    for i, path in enumerate(paths):
        with cols[i % columns]:
            st.image(
                str(path), caption=str(path.relative_to(ROOT)), use_container_width=True
            )


def experiment_status_table() -> pd.DataFrame:
    return pd.DataFrame([
        {
            "Требование": "три сетки Gmsh для базового варианта",
            "Реализация": "experiments/run_base_meshes.py",
            "Параметры": "lc = 0.10, 0.05, 0.025; p=1; Γ=-2",
        },
        {
            "Требование": "подробная сетка для других вариантов",
            "Реализация": "run_poly_degree.py, run_gamma_sweep.py, run_height_sweep.py",
            "Параметры": "lc = 0.05",
        },
        {
            "Требование": "верификация по значениям завихренности",
            "Реализация": "results/base_*/**/metrics.csv",
            "Параметры": "сравнение ω на последовательности сеток",
        },
        {
            "Требование": "p = 1, 2, 3",
            "Реализация": "experiments/run_poly_degree.py",
            "Параметры": "degree = 1, 2, 3",
        },
        {
            "Требование": "три значения Γ",
            "Реализация": "experiments/run_gamma_sweep.py",
            "Параметры": "Γ = -1, -2, -3",
        },
        {
            "Требование": "три значения h",
            "Реализация": "experiments/run_height_sweep.py",
            "Параметры": "h = 0.50, 0.75, 1.00",
        },
    ])


def safe_case_id(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9а-яё_.-]+", "_", text, flags=re.IGNORECASE)
    text = re.sub(r"_+", "_", text).strip("_.-")
    return text or "interactive_case"


def run_cmd(cmd: list[str], timeout: int = 180) -> tuple[bool, str, str, str]:
    env = os.environ.copy()
    env.setdefault("HDF5_USE_FILE_LOCKING", "FALSE")
    try:
        proc = subprocess.run(
            cmd,
            cwd=str(ROOT),
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
        )
        return proc.returncode == 0, " ".join(cmd), proc.stdout, proc.stderr
    except subprocess.TimeoutExpired as exc:
        return (
            False,
            " ".join(cmd),
            exc.stdout or "",
            f"Timeout after {timeout} s\n{exc.stderr or ''}",
        )
    except Exception as exc:
        return False, " ".join(cmd), "", repr(exc)


def show_cmd_result(ok: bool, cmd_str: str, stdout: str, stderr: str) -> None:
    status = "OK" if ok else "ERROR"
    with st.expander(f"{status}: {cmd_str}", expanded=not ok):
        if stdout.strip():
            st.caption("stdout")
            st.code(stdout[-6000:], language="text")
        if stderr.strip():
            st.caption("stderr")
            st.code(stderr[-6000:], language="text")


def read_case_metrics(result_dir: Path) -> pd.DataFrame:
    path = result_dir / "metrics.csv"
    if not path.exists():
        return pd.DataFrame()
    try:
        return pd.read_csv(path)
    except Exception:
        return pd.DataFrame()


def load_ns_reference() -> pd.DataFrame:
    candidates = [
        ROOT / "data" / "ns_reference.csv",
        RESULTS / "ns_reference.csv",
        RESULTS / "navier_stokes_reference.csv",
    ]
    frames: list[pd.DataFrame] = []
    for path in candidates:
        if path.exists():
            try:
                df = pd.read_csv(path)
            except Exception:
                continue
            df.insert(0, "source_file", str(path.relative_to(ROOT)))
            frames.append(df)
    if not frames:
        return pd.DataFrame()
    out = pd.concat(frames, ignore_index=True)
    for col in [
        "Re",
        "vortex_area",
        "vortex_centroid_x",
        "vortex_centroid_y",
        "vortex_bbox_xmin",
        "vortex_bbox_xmax",
        "vortex_bbox_ymin",
        "vortex_bbox_ymax",
        "psi_min",
    ]:
        if col in out.columns:
            out[col] = pd.to_numeric(out[col], errors="coerce")
    return out


def render_interactive_outputs(
    mesh_prefix: Path, msh_path: Path, result_dir: Path
) -> None:
    c1, c2 = st.columns([1.0, 1.0])
    with c1:
        st.subheader("Сетка")
        if msh_path.exists():
            fig = plot_msh(msh_path, max_triangles=20_000)
            if fig is not None:
                st.pyplot(fig, clear_figure=True)
        else:
            st.info("Файл .msh пока не создан.")
    with c2:
        st.subheader("Метрики")
        metrics = read_case_metrics(result_dir)
        if metrics.empty:
            st.info("metrics.csv пока не создан.")
        else:
            row = metrics.iloc[0]
            metric_cards(row)
            st.dataframe(
                short_table(
                    metrics.assign(case=str(result_dir.relative_to(RESULTS))),
                    [
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
                    ],
                ),
                hide_index=True,
                use_container_width=True,
                height=100,
            )

    imgs = []
    if result_dir.exists():
        imgs.extend(sorted(result_dir.glob("*.png")))
        imgs.extend(sorted((result_dir / "figs").glob("*.png")))
    if imgs:
        st.subheader("Решение")
        show_images_grid(imgs, columns=2)


all_metrics = load_metrics()

with st.sidebar:
    st.title("Численное исследование вихре-потенциального течения в канале с уступом")
    page = st.radio(
        "Раздел",
        [
            "1. Постановка",
            "2. Геометрия и сетки",
            "3. Математическая модель",
            "4. Вариационная постановка",
            "5. Алгоритм",
            "6. Реализация",
            "7. Фрагменты кода",
            "8. Верификация: сетки",
            "9. Аппроксимация p",
            "10. Влияние Γ",
            "11. Влияние h",
            "12. Решение",
            "13. Интерактивный расчёт",
            "14. Исследовательский трек",
        ],
    )

if page == "1. Постановка":
    st.title("Численное исследование вихре-потенциального течения в канале с уступом")
    # source(SOURCE_MODEL)

    st.markdown(
        r"""
        **Цель.** Найти вихре-потенциальное течение в канале с уступом методом конечных элементов.

        **Базовый вариант:**
        """
    )
    st.dataframe(
        pd.DataFrame([{"L": 4.0, "H": 1.0, "l": 1.0, "h": 1.0, "Γ": -2.0}]),
        hide_index=True,
        use_container_width=True,
        height=70,
    )

    st.subheader("Требования к расчётам")
    st.dataframe(
        experiment_status_table(), hide_index=True, use_container_width=True, height=260
    )

    st.markdown(
        r"""
        - расчётные сетки с использованием Gmsh: три последовательно сгущающиеся сетки для базового варианта;
        - верификация базового варианта по вычисленным значениям завихренности;
        - расчёты для $p=1,2,3$;
        - расчёты для трёх значений $\Gamma$;
        - расчёты для трёх высот уступа $h$.
        """
    )

elif page == "2. Геометрия и сетки":
    st.title("Геометрия и расчётные сетки")
    # source("Постановка: параметры области H, L, l, h и границы Γ₁–Γ₄; реализация: geo/step_channel.geo.tpl.")

    c1, c2 = st.columns([1.1, 1.0])
    with c1:
        fig = draw_geometry()
        if fig is not None:
            st.pyplot(fig, clear_figure=True)
    # c1.image("app/123.png")

    with c2:
        st.markdown(r"""
        + $ H, L - $ ширина канала, расчетная длина канала
        + $(l, h) - $ параметры уступа
        + $$ \Gamma_1, \Gamma_2 - $$ твердые стенки канала
        + $ \Gamma_3, \Gamma_4 - $ граница входа и выхода жидкости

        """)
        st.dataframe(
            pd.DataFrame([
                {
                    "ID": DOMAIN,
                    "Группа": "domain",
                    "Назначение": "треугольники области",
                },
                {
                    "ID": WALL_LOWER,
                    "Группа": "wall_lower",
                    "Назначение": "нижняя стенка и уступ",
                },
                {"ID": WALL_TOP, "Группа": "wall_top", "Назначение": "верхняя стенка"},
                {"ID": INLET, "Группа": "inlet", "Назначение": "вход"},
                {"ID": OUTLET, "Группа": "outlet", "Назначение": "выход"},
                {
                    "ID": STEP,
                    "Группа": "step",
                    "Назначение": "вертикальная грань уступа",
                },
            ]),
            hide_index=True,
            use_container_width=True,
            height=250,
        )

    st.subheader("Схема сгущения")
    st.dataframe(
        pd.DataFrame([
            {"Серия": "base_coarse", "lc": 0.100, "Отношение к coarse": "1"},
            {"Серия": "base_medium", "lc": 0.050, "Отношение к coarse": "≈4 элемента"},
            {"Серия": "base_fine", "lc": 0.025, "Отношение к coarse": "≈16 элементов"},
            {
                "Серия": "degree/gamma/height",
                "lc": 0.050,
                "Отношение к coarse": "подробная сетка",
            },
        ]),
        hide_index=True,
        use_container_width=True,
        height=180,
    )

    msh_files = sorted(MESHES.glob("**/*.msh"))
    if msh_files:
        selected = st.selectbox(
            "Сетка", msh_files, format_func=lambda p: str(p.relative_to(ROOT))
        )
        fig = plot_msh(selected)
        if fig is not None:
            st.pyplot(fig, clear_figure=True)

    st.code(
        r"""
// Parameters are substituted by geo/generate_geo.py

L = {L};      // downstream channel length
H = {H};      // upper channel height above y=0
l = {l};      // upstream inlet length
h = {h};      // step depth below y=0
lc = {lc};    // characteristic mesh size
lc_step = {lc_step};

Point(1) = {{-l, 0, 0, lc}};
Point(2) = {{ 0, 0, 0, lc_step}};
Point(3) = {{ 0,-h, 0, lc_step}};
Point(4) = {{ L,-h, 0, lc}};
Point(5) = {{ L, H, 0, lc}};
Point(6) = {{-l, H, 0, lc}};

Line(1) = {{1, 2}}; // lower upstream wall
Line(2) = {{2, 3}}; // vertical step wall
Line(3) = {{3, 4}}; // lower downstream wall
Line(4) = {{4, 5}}; // outlet
Line(5) = {{5, 6}}; // upper wall
Line(6) = {{6, 1}}; // inlet

Curve Loop(1) = {{1, 2, 3, 4, 5, 6}};
Plane Surface(1) = {{1}};

// Physical IDs used by FEniCS code.
// Keep these IDs synchronized with solver/problem.py.
Physical Surface("domain", 1) = {{1}};
Physical Curve("wall_lower", 11) = {{1, 2, 3}};
Physical Curve("wall_top",   12) = {{5}};
Physical Curve("inlet",      13) = {{6}};
Physical Curve("outlet",     14) = {{4}};
Physical Curve("step",       15) = {{2}};

Mesh.CharacteristicLengthMin = lc_step;
Mesh.CharacteristicLengthMax = lc;
Mesh.Algorithm = 6;
        
"""
    )

elif page == "3. Математическая модель":
    st.title("Математическая модель")
    # source(SOURCE_MODEL)

    left, right = st.columns(2)
    with left:
        st.markdown(
            r"""
            **Завихренность**
            $$
            \nabla\times\mathbf v=\{0,0,\omega\},\qquad
            \omega=\frac{\partial v_2}{\partial x_1}-\frac{\partial v_1}{\partial x_2}.
            $$

            **Функция тока**
            $$
            -\Delta\psi=\omega(\psi),\qquad \mathbf x\in\Omega.
            $$

            **Области течения**
            $$
            \psi>0:\ \omega=0,\qquad
            \psi<0:\ \omega=\mathrm{const}<0.
            $$
            """
        )
    with right:
        st.markdown(
            r"""
            **Граничные условия**
            $$
            \psi=Hx_2\quad \text{на }\Gamma_3,
            $$
            $$
            \frac{\partial\psi}{\partial n}=0\quad \text{на }\Gamma_4,
            $$
            $$
            \psi=0\quad \text{на }\Gamma_1,
            \qquad
            \psi=H\quad \text{на }\Gamma_2.
            $$

            **Циркуляция**
            $$
            \int_{\psi<0}\omega(\psi)\,d\mathbf x=\Gamma.
            $$
            """
        )

elif page == "4. Вариационная постановка":
    st.title("Вариационная постановка")
    # source(
    #     "Постановка: уравнение для функции тока и граничные условия; преобразование — формула Грина для задачи Пуассона."
    # )

    st.markdown(
        r"""
        Для фиксированной правой части $f$:
        $$
        -\Delta\psi=f.
        $$
        Умножение на тестовую функцию $\varphi$ и интегрирование по частям дают
        $$
        \int_\Omega \nabla\psi\cdot\nabla\varphi\,dx
        =
        \int_\Omega f\varphi\,dx
        +
        \int_{\partial\Omega}\frac{\partial\psi}{\partial n}\varphi\,ds.
        $$
        На границах Дирихле $\varphi=0$; на выходе задано $\partial\psi/\partial n=0$.
        Поэтому
        $$
        \boxed{
        \int_\Omega \nabla\psi\cdot\nabla\varphi\,dx
        =
        \int_\Omega f\varphi\,dx
        }.
        $$
        На итерации $k$:
        $$
        f^k=\omega^k I_{\{\psi^k<0\}}.
        $$
        """
    )

elif page == "5. Алгоритм":
    st.title("Итерационный алгоритм")
    # source(
    # "Постановка: метод последовательных приближений для нелинейной правой части; реализация: solver/solve_stream.py."
    # )

    st.markdown(
        r"""
        По текущему приближению определяется вихревая область
        $$
        \Omega_v^k=\{\mathbf x\in\Omega:\psi^k(\mathbf x)<0\}.
        $$
        Для модели постоянной завихренности
        $$
        \omega^k=\frac{\Gamma}{\int_{\psi^k<0}d\mathbf x}.
        $$
        Следующее приближение находится из линейной задачи
        $$
        -\Delta\psi^{k+1}=\omega^k I_{\{\psi^k<0\}}.
        $$
        """
    )

    st.code(
        """psi_old = initial_guess()
for k in range(max_iter):
    indicator = I(psi_old < 0)        # DG0, по ячейкам
    vortex_area = assemble(indicator * dx)
    omega = Gamma / vortex_area

    solve(inner(grad(psi_new), grad(v))*dx == omega*indicator*v*dx)

    psi_old = (1 - alpha)*psi_old + alpha*psi_new
    stop if err_psi < tol_psi and err_omega < tol_omega""",
        language="python",
    )

    st.markdown(
        r"""
        В коде используется релаксация с параметром $\alpha$.
        При $\alpha=1$ схема совпадает с последовательными приближениями из постановки.
        """
    )

elif page == "6. Реализация":
    st.title("Программная реализация")
    # source(SOURCE_CODE)

    st.dataframe(
        pd.DataFrame([
            {
                "Компонент": "геометрия",
                "Файл": "geo/step_channel.geo.tpl",
                "Роль": "Physical Surface/Curve, параметры L,H,l,h,lc",
            },
            {
                "Компонент": "генерация .geo",
                "Файл": "geo/generate_geo.py",
                "Роль": "подстановка параметров",
            },
            {
                "Компонент": "конвертация",
                "Файл": "solver/mesh_convert.py",
                "Роль": ".msh → XDMF mesh/facets",
            },
            {
                "Компонент": "параметры",
                "Файл": "solver/problem.py",
                "Роль": "ID границ, параметры задачи",
            },
            {
                "Компонент": "солвер",
                "Файл": "solver/solve_stream.py",
                "Роль": "итерации, МКЭ, метрики, XDMF/PNG",
            },
            {
                "Компонент": "запуск",
                "Файл": "solver/run_case.py",
                "Роль": "один расчёт",
            },
            {
                "Компонент": "серии",
                "Файл": "experiments/*.py",
                "Роль": "сетки, p, Γ, h",
            },
        ]),
        hide_index=True,
        use_container_width=True,
        height=300,
    )

    st.subheader("Проверка покрытия требований")
    st.dataframe(
        experiment_status_table(), hide_index=True, use_container_width=True, height=260
    )


elif page == "7. Фрагменты кода":
    st.title("Фрагменты исходного кода солвера")

    st.markdown(
        r"""
        Ниже приведены фрагменты `solver/solve_stream.py`, относящиеся непосредственно к решению задачи.
        Полный файл содержит также экспорт XDMF/PNG и запись метрик.
        """
    )

    st.subheader("1. Загрузка сетки и меток границ")
    st.code(
        """def read_mesh(prefix: str | Path) -> Tuple[Mesh, MeshFunction]:
    prefix = Path(prefix)
    mesh = Mesh()
    with XDMFFile(str(prefix.with_name(prefix.name + "_mesh.xdmf"))) as infile:
        infile.read(mesh)

    mvc = MeshValueCollection("size_t", mesh, mesh.topology().dim() - 1)
    with XDMFFile(str(prefix.with_name(prefix.name + "_facets.xdmf"))) as infile:
        infile.read(mvc, "name_to_read")
    facets = MeshFunction("size_t", mesh, mvc)
    return mesh, facets""",
        language="python",
    )
    st.markdown(
        r"""
        `*_mesh.xdmf` содержит треугольную сетку области. `*_facets.xdmf` содержит
        физические метки граничных участков, экспортированные из Gmsh.
        """
    )

    st.subheader("2. Граничные условия")
    st.code(
        """def make_boundary_conditions(V: FunctionSpace, facets: MeshFunction, params: CaseParameters):
    inlet_value = Expression(
        "inlet_scale*x[1]",
        inlet_scale=params.inlet_scale,
        degree=max(1, params.degree + 1),
    )
    bc_inlet = DirichletBC(V, inlet_value, facets, INLET)
    bc_lower = DirichletBC(V, Constant(0.0), facets, WALL_LOWER)
    bc_top = DirichletBC(V, Constant(params.H), facets, WALL_TOP)
    return [bc_inlet, bc_lower, bc_top]""",
        language="python",
    )
    st.markdown(
        r"""
        На входе задаётся $\psi=H x_2$ с масштабом входного потока. На нижней стенке и уступе
        задаётся $\psi=0$, на верхней стенке — $\psi=H$. На выходе условие
        $\partial\psi/\partial n=0$ является естественным условием Неймана и не задаётся через `DirichletBC`.
        """
    )

    st.subheader("3. Начальное потенциальное решение")
    st.code(
        """def solve_potential(V: FunctionSpace, bcs) -> Function:
    u = TrialFunction(V)
    v = TestFunction(V)
    psi = Function(V, name="psi_potential")
    solve(inner(grad(u), grad(v)) * dx == Constant(0.0) * v * dx, psi, bcs)
    return psi""",
        language="python",
    )
    st.markdown(
        r"""
        Первое приближение строится из задачи Лапласа $-\Delta\psi^0=0$ с теми же граничными условиями.
        В реализации к нему может добавляться малое отрицательное возмущение за уступом, чтобы запустить
        итерации со свободной вихревой областью.
        """
    )

    st.subheader("4. Индикатор вихревой области")
    st.code(
        """def build_indicator(psi: Function, Q: FunctionSpace) -> Function:
    mesh = Q.mesh()
    indicator = Function(Q, name="vortex_indicator")
    values = indicator.vector().get_local()
    dofmap = Q.dofmap()
    for cell in cells(mesh):
        dof = dofmap.cell_dofs(cell.index())[0]
        values[dof] = 1.0 if psi(cell.midpoint()) < 0.0 else 0.0
    indicator.vector().set_local(values)
    indicator.vector().apply("insert")
    return indicator""",
        language="python",
    )
    st.markdown(
        r"""
        Индикатор хранится в пространстве `DG0`: одно постоянное значение на треугольник.
        Значение равно $1$ в ячейках, где $\psi<0$, и $0$ вне вихревой зоны.
        """
    )

    st.subheader("5. Основная итерация")
    st.code(
        """u = TrialFunction(V)
v = TestFunction(V)
a = inner(grad(u), grad(v)) * dx

for k in range(1, params.max_iter + 1):
    indicator = build_indicator(psi_old, Q)
    vortex_area = float(assemble(indicator * dx))

    if vortex_area <= DOLFIN_EPS_AREA:
        raise RuntimeError("Vortex area is zero.")

    omega = float(params.Gamma / vortex_area)
    rhs = omega * indicator * v * dx

    psi_new = Function(V, name="psi_new")
    solve(a == rhs, psi_new, bcs)""",
        language="python",
    )
    st.markdown(
        r"""
        На каждой итерации фиксируется область $\{\psi^k<0\}$ и вычисляется
        $\omega^k=\Gamma/|\Omega_v^k|$. Затем решается линейная задача Пуассона
        $$
        \int_\Omega 
            \nabla\psi^{k+1}\cdot
            \nabla\varphi\,dx
        =
        \int_\Omega \omega^k I_{\{\psi^k<0\}}\varphi\,dx.
        $$
        """
    )

    st.subheader("6. Релаксация и критерий остановки")
    st.code(
        """psi_relaxed = Function(V, name="psi")
psi_relaxed.vector()[:] = (
    psi_old.vector() * (1.0 - params.alpha)
    + psi_new.vector() * params.alpha
)
psi_relaxed.vector().apply("insert")

diff = Function(V, name="psi_diff")
diff.vector()[:] = psi_relaxed.vector() - psi_old.vector()
diff.vector().apply("insert")

denom = max(l2_norm(psi_relaxed), 1.0e-30)
err_psi = l2_norm(diff) / denom
err_omega = abs(omega - omega_prev) / max(1.0, abs(omega))

psi_old.assign(psi_relaxed)
omega_prev = omega

if err_psi < params.tol_psi and err_omega < params.tol_omega:
    converged = True
    break""",
        language="python",
    )
    st.markdown(
        r"""
        При $\alpha=1$ используется исходная схема последовательных приближений. Значения
        $0<\alpha<1$ демпфируют изменение свободной границы $\{\psi=0\}$.
        """
    )

    st.subheader("7. Скорость, завихренность и контрольные метрики")
    st.code(
        """omega_field = project(Constant(omega) * indicator, Q)
omega_field.rename("omega", "omega")

W = VectorFunctionSpace(mesh, "CG", max(1, params.degree - 1))
velocity = project(as_vector((psi.dx(1), -psi.dx(0))), W)
velocity.rename("velocity", "velocity")

metrics = {
    "converged": int(converged),
    "iterations": iterations,
    "omega": omega,
    "vortex_area": vortex_area,
    "circulation_check": omega * vortex_area,
    "circulation_error_abs": abs(omega * vortex_area - params.Gamma),
    "psi_min": float(psi_values.min()),
    "psi_max": float(psi_values.max()),
}""",
        language="python",
    )

elif page == "8. Верификация: сетки":
    st.title("Верификация на последовательности сеток")
    # source(
    #     "Постановка: базовый вариант проверяется на трёх последовательно сгущающихся сетках по вычисленным значениям завихренности."
    # )

    if all_metrics.empty:
        st.warning("Файлы results/**/metrics.csv не найдены.")
    else:
        df = all_metrics[
            case_mask(all_metrics, ["base_coarse", "base_medium", "base_fine"])
        ].copy()
        if df.empty:
            st.warning("Не найдены результаты серии base_coarse/base_medium/base_fine.")
        else:
            df = df.sort_values("num_cells")
            df["rel_omega_change"] = df["omega"].pct_change().abs()
            st.dataframe(
                short_table(
                    df,
                    [
                        "case",
                        "num_cells",
                        "dofs",
                        "iterations",
                        "omega",
                        "rel_omega_change",
                        "vortex_area",
                        "circulation_error_abs",
                        "wall_time_sec",
                    ],
                ),
                hide_index=True,
                use_container_width=True,
                height=180,
            )
            show_numeric_line(df, "num_cells", "omega")

elif page == "9. Аппроксимация p":
    st.title("Аппроксимация полиномами степени p")
    # source(
    #     "Постановка: требуется решить задачу при p=1,2,3; реализация: experiments/run_poly_degree.py."
    # )

    if all_metrics.empty:
        st.warning("Файлы results/**/metrics.csv не найдены.")
    else:
        df = all_metrics[case_mask(all_metrics, ["degree_sweep"])].copy()
        if df.empty:
            st.warning("Не найдены результаты серии degree_sweep.")
        else:
            df = df.sort_values("degree")
            st.dataframe(
                short_table(
                    df,
                    [
                        "case",
                        "degree",
                        "num_cells",
                        "dofs",
                        "iterations",
                        "omega",
                        "vortex_area",
                        "circulation_error_abs",
                        "wall_time_sec",
                    ],
                ),
                hide_index=True,
                use_container_width=True,
                height=180,
            )
            show_numeric_line(df, "degree", "omega")

elif page == "10. Влияние Γ":
    st.title("Влияние заданной циркуляции Γ")
    # source(
    #     "Постановка: требуется решить задачу при трёх значениях Γ; реализация: experiments/run_gamma_sweep.py."
    # )

    if all_metrics.empty:
        st.warning("Файлы results/**/metrics.csv не найдены.")
    else:
        df = all_metrics[case_mask(all_metrics, ["gamma_sweep"])].copy()
        if df.empty:
            st.warning("Не найдены результаты серии gamma_sweep.")
        else:
            df = df.sort_values("Gamma")
            st.dataframe(
                short_table(
                    df,
                    [
                        "case",
                        "Gamma",
                        "num_cells",
                        "dofs",
                        "iterations",
                        "omega",
                        "vortex_area",
                        "circulation_error_abs",
                        "psi_min",
                    ],
                ),
                hide_index=True,
                use_container_width=True,
                height=180,
            )
            c1, c2 = st.columns(2)
            with c1:
                show_numeric_line(df, "Gamma", "omega")
            with c2:
                show_numeric_line(df, "Gamma", "vortex_area")

elif page == "11. Влияние h":
    st.title("Влияние высоты уступа h")
    # source(
    #     "Постановка: требуется решить задачу при трёх значениях h; реализация: experiments/run_height_sweep.py."
    # )

    if all_metrics.empty:
        st.warning("Файлы results/**/metrics.csv не найдены.")
    else:
        df = all_metrics[case_mask(all_metrics, ["height_sweep"])].copy()
        if df.empty:
            st.warning("Не найдены результаты серии height_sweep.")
        else:
            df = df.sort_values("h")
            st.dataframe(
                short_table(
                    df,
                    [
                        "case",
                        "h",
                        "num_cells",
                        "dofs",
                        "iterations",
                        "omega",
                        "vortex_area",
                        "circulation_error_abs",
                        "psi_min",
                    ],
                ),
                hide_index=True,
                use_container_width=True,
                height=180,
            )
            c1, c2 = st.columns(2)
            with c1:
                show_numeric_line(df, "h", "omega")
            with c2:
                show_numeric_line(df, "h", "vortex_area")

elif page == "12. Решение":
    st.title("Решения")
    # source(
    #     "Реализация: solver/solve_stream.py сохраняет ψ, velocity, omega, indicator в XDMF и PNG для презентации."
    # )

    if all_metrics.empty:
        st.warning("Файлы results/**/metrics.csv не найдены.")
    else:
        cases = sorted(all_metrics["case"].astype(str).unique())
        case = st.selectbox("Расчёт", cases)
        row = all_metrics[all_metrics["case"].astype(str) == case].iloc[0]
        metric_cards(row)
        imgs = image_files_for_case(case)
        if imgs:
            show_images_grid(imgs, columns=2)
        else:
            st.info(
                "PNG для выбранного расчёта не найдены. Основные поля сохранены в XDMF."
            )

elif page == "13. Интерактивный расчёт":
    st.title("Интерактивный расчёт")
    # source(
    #     "Демонстрационный pipeline: geo/generate_geo.py → gmsh → solver/mesh_convert.py → solver/run_case.py."
    # )

    st.markdown(
        r"""
        Страница запускает один расчёт с выбранными параметрами. Результаты сохраняются в
        `meshes/interactive/<case_id>/` и `results/interactive/<case_id>/`.
        """
    )

    with st.form("interactive_case_form"):
        st.subheader("Параметры")
        g1, g2, g3, g4, g5 = st.columns(5)
        L_val = g1.number_input(
            "L", min_value=1.0, max_value=10.0, value=4.0, step=0.25
        )
        H_val = g2.number_input(
            "H", min_value=0.25, max_value=4.0, value=1.0, step=0.10
        )
        l_val = g3.number_input(
            "l", min_value=0.10, max_value=4.0, value=1.0, step=0.10
        )
        h_val = g4.number_input(
            "h", min_value=0.10, max_value=4.0, value=1.0, step=0.10
        )
        lc_val = g5.number_input(
            "lc", min_value=0.015, max_value=0.30, value=0.08, step=0.005, format="%.3f"
        )

        n1, n2, n3, n4, n5 = st.columns(5)
        gamma_val = n1.number_input("Γ", value=-2.0, step=0.5)
        degree_val = n2.selectbox("p", [1, 2, 3], index=0)
        alpha_val = n3.number_input(
            "α", min_value=0.05, max_value=1.0, value=0.5, step=0.05
        )
        max_iter_val = n4.number_input(
            "max_iter", min_value=5, max_value=500, value=120, step=5
        )
        timeout_val = n5.number_input(
            "timeout, s", min_value=30, max_value=1200, value=240, step=30
        )

        a1, a2, a3 = st.columns([1.0, 1.0, 2.0])
        initial_eps_val = a1.number_input(
            "initial_eps", min_value=0.0, max_value=1.0, value=0.05, step=0.01
        )
        initial_x_val = a2.number_input(
            "initial_vortex_x", min_value=0.1, max_value=10.0, value=2.0, step=0.1
        )
        case_raw = a3.text_input(
            "case_id",
            value=f"L{L_val:g}_H{H_val:g}_l{l_val:g}_h{h_val:g}_G{gamma_val:g}_p{degree_val}_lc{lc_val:g}",
        )

        action = st.radio(
            "Действие",
            [
                "Полный pipeline",
                "Только .geo",
                "Только Gmsh",
                "Только конвертация",
                "Только solve",
            ],
            horizontal=True,
        )
        submitted = st.form_submit_button("Выполнить")

    fig = draw_geometry(L_val, H_val, l_val, h_val)
    if fig is not None:
        st.pyplot(fig, clear_figure=True)

    case_id = safe_case_id(case_raw)
    mesh_dir = MESHES / "interactive" / case_id
    result_dir = RESULTS / "interactive" / case_id
    geo_path = mesh_dir / "step_channel.geo"
    msh_path = mesh_dir / "step_channel.msh"
    mesh_prefix = mesh_dir / "step_channel"

    st.code(
        f"""case_id: {case_id}
geo: {geo_path.relative_to(ROOT)}
msh: {msh_path.relative_to(ROOT)}
mesh_prefix: {mesh_prefix.relative_to(ROOT)}
results: {result_dir.relative_to(ROOT)}""",
        language="text",
    )

    if submitted:
        mesh_dir.mkdir(parents=True, exist_ok=True)
        result_dir.mkdir(parents=True, exist_ok=True)
        cmds: list[list[str]] = []

        cmd_geo = [
            sys.executable,
            "geo/generate_geo.py",
            "--L",
            str(L_val),
            "--H",
            str(H_val),
            "--l",
            str(l_val),
            "--h",
            str(h_val),
            "--lc",
            str(lc_val),
            "--out",
            str(geo_path.relative_to(ROOT)),
        ]
        cmd_gmsh = [
            "gmsh",
            "-2",
            str(geo_path.relative_to(ROOT)),
            "-format",
            "msh2",
            "-o",
            str(msh_path.relative_to(ROOT)),
        ]
        cmd_convert = [
            sys.executable,
            "solver/mesh_convert.py",
            str(msh_path.relative_to(ROOT)),
            str(mesh_prefix.relative_to(ROOT)),
        ]
        cmd_solve = [
            sys.executable,
            "solver/run_case.py",
            "--mesh-prefix",
            str(mesh_prefix.relative_to(ROOT)),
            "--out",
            str(result_dir.relative_to(ROOT)),
            "--L",
            str(L_val),
            "--H",
            str(H_val),
            "--l",
            str(l_val),
            "--h",
            str(h_val),
            "--Gamma",
            str(gamma_val),
            "--degree",
            str(degree_val),
            "--alpha",
            str(alpha_val),
            "--max-iter",
            str(max_iter_val),
            "--initial-eps",
            str(initial_eps_val),
            "--initial-vortex-x",
            str(initial_x_val),
        ]

        if action == "Полный pipeline":
            cmds = [cmd_geo, cmd_gmsh, cmd_convert, cmd_solve]
        elif action == "Только .geo":
            cmds = [cmd_geo]
        elif action == "Только Gmsh":
            cmds = [cmd_gmsh]
        elif action == "Только конвертация":
            cmds = [cmd_convert]
        elif action == "Только solve":
            cmds = [cmd_solve]

        if (
            any(cmd and cmd[0] == "gmsh" for cmd in cmds)
            and shutil.which("gmsh") is None
        ):
            st.error("Команда `gmsh` не найдена в PATH контейнера/среды.")
        else:
            ok_all = True
            for cmd in cmds:
                ok, cmd_str, stdout, stderr = run_cmd(cmd, timeout=int(timeout_val))
                show_cmd_result(ok, cmd_str, stdout, stderr)
                ok_all = ok_all and ok
                if not ok:
                    break
            if ok_all:
                st.success("Pipeline завершён.")

    if geo_path.exists():
        st.subheader("Сгенерированный .geo")
        with st.expander(str(geo_path.relative_to(ROOT)), expanded=False):
            st.code(geo_path.read_text(encoding="utf-8"), language="geo")

    render_interactive_outputs(mesh_prefix, msh_path, result_dir)


elif page == "14. Исследовательский трек":
    st.title("Исследовательский трек: зависимость ω(ψ)")

    st.markdown(
        r"""
        В базовой модели завихренность постоянна в области $\psi<0$:
        $$
        \omega(\psi)=\lambda I_{\{\psi<0\}}.
        $$

        Рассмотрено расширение:
        $$
        \omega(\psi)=\lambda(-\psi)^q I_{\{\psi<0\}},
        \qquad q=0,1,2.
        $$

        Коэффициент $\lambda$ определяется из условия заданной циркуляции:
        $$
        \int_\Omega \omega(\psi)\,dx=\Gamma,
        \qquad
        \lambda=
        \frac{\Gamma}
        {\int_\Omega (-\psi)^q I_{\{\psi<0\}}\,dx}.
        $$

        При $q=0$ получается базовая модель постоянной завихренности.
        """
    )

    st.markdown(
        r"""
| Параметр | Модель | Смысл |
|:---:|---|---|
| $q=0$ | $\omega=\lambda I_{\{\psi<0\}}$ | постоянная завихренность |
| $q=1$ | $\omega=\lambda(-\psi)I_{\{\psi<0\}}$ | завихренность усиливается в глубине вихревой зоны |
| $q=2$ | $\omega=\lambda(-\psi)^2I_{\{\psi<0\}}$ | более локализованная завихренность |
"""
    )

    if all_metrics.empty:
        st.warning("Файлы results/**/metrics.csv не найдены.")
    else:
        df = all_metrics[case_mask(all_metrics, ["omega_model_sweep"])].copy()
        if df.empty:
            st.warning("Не найдены результаты серии omega_model_sweep.")
        else:
            df = df.sort_values("omega_power")
            st.dataframe(
                short_table(
                    df,
                    [
                        "case",
                        "omega_model",
                        "omega_power",
                        "num_cells",
                        "dofs",
                        "iterations",
                        "omega_scale",
                        "omega_mean",
                        "omega_min",
                        "omega_max",
                        "vortex_area",
                        "vortex_centroid_x",
                        "vortex_centroid_y",
                        "psi_min",
                        "circulation_error_abs",
                    ],
                ),
                hide_index=True,
                use_container_width=True,
                height=220,
            )

            c1, c2 = st.columns(2)
            with c1:
                show_numeric_line(df, "omega_power", "vortex_area")
            with c2:
                show_numeric_line(df, "omega_power", "psi_min")

            cases = sorted(df["case"].astype(str).unique())
            case = st.selectbox("Расчёт", cases)
            imgs = image_files_for_case(case)
            if imgs:
                show_images_grid(imgs, columns=2)
