import streamlit as st
from dolfin import *
from PIL import Image
 
menu = st.sidebar.radio("***",
    ("Библиотеки Python", 
    "Текст программы", 
    "Результат работы",
    "Параметрические расчеты",    
    "streamlit - параметры",
    "streamlit - график",
    )
)
  
if menu == "Библиотеки Python":
    r"""
##### Библиотеки Python
* fenics - вычислительная платформа конечно-элементного анализа
* matplotlib - графика
* streamlit - интерактив

    """
      
if menu == "Текст программы":
    r"""
##### Текст программы

    """
    code = """
from dolfin import *
import matplotlib.pyplot as plt

# Параметры
n = 20
eps = Constant(0.01)

# Область и сетка
mesh = UnitSquareMesh(n, n)
plot(mesh, title="Сетка")
plt.savefig("gr1.png", format="png", dpi=300)
plt.clf()

# Функциональное пространство
V = FunctionSpace(mesh, "Lagrange", 2)

# Часть границы
class DirichletBoundary(SubDomain):
    def inside(self, x, on_boundary):
        return x[0] + x[1] > 1.0 - DOLFIN_EPS and on_boundary

# Краевые условия Дирихле
bc = DirichletBC(V, Constant(0.0), DirichletBoundary())

# Вариационная задача
u = TrialFunction(V)
v = TestFunction(V)
f = interpolate(Expression("x[0]", degree=2), V)
a = eps * inner(grad(u), grad(v)) * dx + u * v * dx
L = f * v * dx

# Численное решение
u_sol = Function(V)
solve(a == L, u_sol, bc,
      solver_parameters={'linear_solver': 'mumps'})
print("max|u(x)| = ", u_sol.vector().norm('linf'))

# График
plot(u_sol, title="Решение")
plt.savefig("gr2.png", format="png", dpi=300)
plt.clf()
"""
    st.code(code, language="python")  
          
if menu == "Результат работы":
    r"""
##### Результат работы

Параметры
* $n = 20$
* $\varepsilon = 0.01$

Консольный вывод
    """
    code = """
Solving linear variational problem.
max|u(x)| =  0.6696431966505915
    """
    st.code(code, language="bash")  
    
    r"""
Графики: gr1.png, gr2.png
    """
    c1, c2 = st.columns(2)
    image1 = Image.open("pages/figs/gr1.png")
    c1.image(image1)
    image2 = Image.open("pages/figs/gr2.png")
    c2.image(image2)
    
if menu == "Параметрические расчеты":

    import matplotlib.pyplot as plt
    import numpy as np

    r"""
##### Параметрические расчеты
* Равномерная сетка $n \times n$    
* Малый параметр $\varepsilon = 10^{-p}$
    """
        
    # Параметры
    c1, cc, c2, _ = st.columns([5,1,5,4])
    n = c1.selectbox("n", [10, 20, 40], index = 1)
    pa = range(1,10)
    p = c2.select_slider("p", options=pa, value=2)
    eps = Constant(10**(-p))

    # Область и сетка
    mesh = UnitSquareMesh(n, n)

    # Функциональное пространство
    V = FunctionSpace(mesh, "Lagrange", 2)

    # Часть границы
    class DirichletBoundary(SubDomain):
        def inside(self, x, on_boundary):
            return x[0] + x[1] > 1.0 - DOLFIN_EPS and on_boundary

    # Краевые условия Дирихле
    bc = DirichletBC(V, Constant(0.0), DirichletBoundary())

    # Вариационная задача
    u = TrialFunction(V)
    v = TestFunction(V)
    f = interpolate(Expression("x[0]", degree=2), V)
    a = eps * inner(grad(u), grad(v)) * dx + u * v * dx
    L = f * v * dx

    # Численное решение
    u_sol = Function(V)
    solve(a == L, u_sol, bc,
          solver_parameters={'linear_solver': 'mumps'})

    # График
    cc, _ = st.columns([5,3])
    plot(u_sol, title="Решение")
    with cc: st.pyplot(plt.gcf())
    plt.clf()

    # Амплитуда решения
    str = "max|u(x)| = " + str(u_sol.vector().norm('linf'))
    st.write(str)


if menu == "streamlit - параметры":
    r"""
##### streamlit - параметры
    """

    code = """
    # Параметры    
    c1, cc, c2 = st.columns([5,1,5])
    n = c1.selectbox("n", [10, 20, 40], index = 1)
    pa = range(1,10)
    p = c2.select_slider("p", options=pa, value=2)
    eps = Constant(10**(-p))
    """
    st.code(code, language="python")  
    
if menu == "streamlit - график":
    r"""
##### streamlit - график
    """

    code = """
    # График
    cc, _ = st.columns([5,3])
    plot(u_sol, title="Решение")
    with cc: st.pyplot(plt.gcf())
    plt.clf()

    # Амплитуда решения
    str = "max|u(x)| = " + str(u_sol.vector().norm('linf'))
    st.write(str)
    """
    st.code(code, language="python")  


    
    
       

