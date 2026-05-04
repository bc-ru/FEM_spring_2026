import streamlit as st

st.title("3. Математическая модель")

st.subheader("**Осесимметричное приближение**")
st.markdown("""Шар радиуса $(a)$ находится в потоке идеальной несжимаемой жидкости.""")
st.markdown(r"""Поток набегает вдоль оси $(z)$ со скоростью $(u_\infty)$.""")
st.markdown("Цилиндрические координаты $(r,  \Theta, z)$. Нет зависимости от угла $(\Theta)$")

st.subheader("**Уравнение для потенциала скорости**")
st.markdown("""
Потенциал скорости $(\phi(r, z))$ удовлетворяет уравнению Лапласа 
в цилиндрических координатах:""")
st.latex(r"""\frac{1}{r} \frac{\partial}{\partial r} \left( r \frac{\partial \varphi}{\partial r} \right) + 
\frac{\partial^2 \varphi}{\partial z^2} = 0, \quad (r, z) \in \Omega""")

st.subheader("**Уравнение для функции тока**")
st.markdown("""Функция тока $(\psi(r, z))$ определяет компоненты скорости""")
st.latex(r"u_r = \frac{1}{r}\frac{\partial \psi}{\partial z}")
st.latex(r"u_z = -\frac{1}{r}\frac{\partial \psi}{\partial r}")

st.markdown("""Уравнение""")
st.latex(r"r\frac{\partial}{\partial r}\left(\frac{1}{r}\frac{\partial \psi}{\partial r}\right) + \frac{\partial^2 \psi}{\partial z^2} = 0, \qquad (r,z)\in\Omega")

st.subheader("**Краевые условия**")

st.markdown(r"Равномерный поток (скорость $\mathbf{u} = \{0, u_\infty\}$) на удаленной границе")
st.latex(r"\psi(r,z)=\frac{1}{2}u_\infty r^2, \quad (r,z)\in\Gamma")
st.markdown("На границе шара")
st.latex(r"\psi(r,z)=0, \quad (r,z)\in\gamma")
st.markdown("Условие симметрии")
st.latex(r"\psi(r,z)=0, \quad (r,z)\in\Gamma_1\cup\Gamma_2")
