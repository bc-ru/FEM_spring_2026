import streamlit as st

st.title("5. Точное решение и вариационная постановка")

t1, t2 = st.tabs(["Точное решение", "Вариационная постановка"])

# =========================
# Точное решение
# =========================
with t1:
    st.markdown("Для сферической области a < ρ < R точное решение имеет вид:")

    st.latex(r"""
    \psi(r,z)=\frac{1}{2}u_\infty r^2\frac{1-a^3/\rho^3}{1-a^3/R^3}, 
    \qquad \rho=\sqrt{r^2+z^2}
    """)

    st.markdown("Касательная скорость на поверхности шара:")

    st.latex(r"""
    u_\tau(\theta)=\frac{3u_\infty}{2(1-a^3/R^3)}\sin\theta
    """)

    st.caption("Источник: Лойцянский Л.Г. «Механика жидкости и газа», 2003")


# =========================
# Вариационная постановка
# =========================
with t2:
    st.header("Исходное уравнение для потенциала скорости")

    st.latex(r"""
    \frac{1}{r} \frac{\partial}{\partial r}
    \left( r \frac{\partial \varphi}{\partial r} \right)
    +
    \frac{\partial^2 \varphi}{\partial z^2}
    = 0, \quad (r, z) \in \Omega
    """)

    st.header("Умножение на тестовую функцию и интегрирование")

    st.markdown("Умножаем уравнение на тестовую функцию v и интегрируем по области с весом r:")

    st.latex(r"""
    \int_{\Omega}
    \left[
    \frac{\partial}{\partial r}
    \left( r \frac{\partial \varphi}{\partial r} \right)
    +
    r \frac{\partial^2 \varphi}{\partial z^2}
    \right]
    v \, dr dz = 0
    """)

    st.header("Интегрирование по частям")

    st.latex(r"""
    \int_{\Omega}
    \left(
    \frac{\partial \varphi}{\partial r}
    \frac{\partial v}{\partial r}
    +
    \frac{\partial \varphi}{\partial z}
    \frac{\partial v}{\partial z}
    \right)
    r \, dr dz = 0
    """)

    st.header("Граничные условия")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Внешняя граница Γ (Дирихле):**")
        st.latex(r"\varphi = u_\infty z")

        st.markdown("**Поверхность шара γ (Неймана):**")
        st.latex(r"\frac{\partial \varphi}{\partial n} = 0")

    with col2:
        st.markdown("**Ось симметрии Γ₁:**")
        st.latex(r"\frac{\partial \varphi}{\partial r} = 0")

        st.markdown("**Горизонтальная ось Γ₂:**")
        st.latex(r"\frac{\partial \varphi}{\partial z} = 0")

    st.header("Итоговая вариационная задача")

    st.markdown("Найти φ ∈ V такую, что:")

    st.latex(r"""
    \int_{\Omega} \nabla \varphi \cdot \nabla v \, r \, dr dz = 0,
    \quad \forall v \in V_0
    """)

    st.markdown("где V₀ — пространство тестовых функций, равных нулю на внешней границе.")

    # =========================
    # FEM
    # =========================
    st.header("Конечно-элементная аппроксимация")

    st.subheader("Дискретизация области")
    st.latex(r"\Omega \approx \Omega_h = \bigcup_{e=1}^{N_e} K_e")

    st.subheader("Функциональные пространства")
    st.latex(r"""
    V_h = \{ v_h \in C^0(\Omega_h) : v_h|_{K_e} \in P_p(K_e) \}
    """)

    col_a, col_b, col_c = st.columns(3)

    with col_a:
        st.markdown("**p = 1 (линейные)**")
        st.markdown("3 узла")

    with col_b:
        st.markdown("**p = 2 (квадратичные)**")
        st.markdown("6 узлов")

    with col_c:
        st.markdown("**p = 3 (кубические)**")
        st.markdown("10 узлов")

    st.subheader("Аппроксимация решения")

    st.latex(r"""
    \varphi_h(r,z) = \sum_{j=1}^{N} \varphi_j \phi_j(r,z)
    """)

    st.subheader("Дискретная задача")

    st.latex(r"""
    \int_{\Omega_h}
    \nabla \varphi_h \cdot \nabla v_h \, r \, dr dz = 0,
    \quad \forall v_h \in V_{0h}
    """)

    st.subheader("Система линейных уравнений")

    st.latex(r"A \boldsymbol{\varphi} = 0")

    st.latex(r"""
    A_{ij} =
    \int_{\Omega_h}
    \nabla \phi_i \cdot \nabla \phi_j \, r \, dr dz
    """)


# =========================
# Expander
# =========================
with st.expander("Обозначения функциональных пространств"):

    st.latex(r"V_g = \{v\in H^1(\Omega): v=g \text{ на } \partial\Omega\}")
    st.latex(r"V_0 = \{v\in H^1(\Omega): v=0 \text{ на } \partial\Omega\}")
    st.latex(r"V_h \subset H^1(\Omega)")

    st.markdown(r"""
    - $$ H^1 (Ω) $$ — пространство Соболева  
    - $$ V_g $$ — функции с условиями Дирихле  
    - $$ V_0 $$ — тестовые функции  
    - $$ V_h $$ — конечно-элементное подпространство
    """)