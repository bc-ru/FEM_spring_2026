from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from ui_helpers import explain_table_columns, list_missing, plot_convergence, read_csv

st.title("8. Верификация и сравнение")

st.markdown(
    r"""
По заданию верификация должна включать:

- три последовательно сгущающиеся сетки для базового варианта;
- сравнение аппроксимаций степени $(p = 1,2,3)$;
- сравнение по касательной скорости на поверхности шара.
    """
)

conv_path = Path("results/convergence_table.csv")
if conv_path.exists():
    df = read_csv(conv_path)
    st.subheader("Таблица ошибок")
    st.dataframe(df, use_container_width=True)
    with st.expander("Пояснение к столбцам таблицы"):
        explain_table_columns()

    c1, c2 = st.columns(2)
    with c1:
        st.pyplot(plot_convergence(df, "L2(psi)", "L2(ψ)"), use_container_width=True)
    with c2:
        st.pyplot(plot_convergence(df, "Linf(u_tau)", r"L∞(uτ)"), use_container_width=True)
else:
    st.info(
        "Файл `results/convergence_table.csv` пока отсутствует. После batch-расчётов здесь "
        "появятся таблица сходимости и графики ошибок."
    )

st.divider()

st.subheader("Сравнение степеней аппроксимации p")
mesh_name = st.selectbox("Сетка", ["coarse", "medium", "fine"], index=2)
fig_p, ax_p = plt.subplots(figsize=(7.2, 4.2))
found_p = False
for p in [1, 2, 3]:
    path = Path(f"results/base/{mesh_name}/p{p}/tangential_velocity.csv")
    if path.exists():
        d = pd.read_csv(path)
        ax_p.plot(d["theta"], d["u_tau_h"], "o-", markersize=3, label=f"p={p}")
        if not found_p:
            ax_p.plot(d["theta"], d["u_tau_exact"], "--", linewidth=2, label="точное")
        found_p = True
if found_p:
    ax_p.set_xlabel(r"$\theta$")
    ax_p.set_ylabel(r"$u_\tau(\theta)$")
    ax_p.grid(True, alpha=0.3)
    ax_p.legend()
    fig_p.tight_layout()
    st.pyplot(fig_p, use_container_width=True)
    st.caption("На одной и той же сетке повышение порядка полинома должно улучшать совпадение с точным распределением.")
else:
    st.info("Сравнение по p пока недоступно: не найдены файлы `results/base/<mesh>/p*/tangential_velocity.csv`.")

st.divider()

st.subheader("Влияние радиуса внешней границы R")
fig_R, ax_R = plt.subplots(figsize=(7.2, 4.2))
found_R = False
for R in [3, 5, 10]:
    path = Path(f"results/R_study/R{R}/tangential_velocity.csv")
    if path.exists():
        d = pd.read_csv(path)
        ax_R.plot(d["theta"], d["u_tau_h"], "o-", markersize=3, label=f"R={R}")
        if not found_R:
            ax_R.plot(d["theta"], d["u_tau_exact"], "--", linewidth=2, label="точное")
        found_R = True
if found_R:
    ax_R.set_xlabel(r"$\theta$")
    ax_R.set_ylabel(r"$u_\tau(\theta)$")
    ax_R.grid(True, alpha=0.3)
    ax_R.legend()
    fig_R.tight_layout()
    st.pyplot(fig_R, use_container_width=True)
    st.caption("При увеличении R влияние искусственной внешней границы уменьшается, и решение приближается к модели внешней задачи.")
else:
    st.info("Сравнение по R пока недоступно: не найдены файлы `results/R_study/R*/tangential_velocity.csv`.")
