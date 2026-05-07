import streamlit as st
from PIL import Image
 
menu = st.sidebar.radio('***',
    (
    "Лагранжевые конечные элементы", 
    "Базисные функции",
    "1D интерполяция",
    "1D приближение",
    )
)
  
if menu == "Лагранжевые конечные элементы":
    r"""
##### Лагранжевые конечные элементы

Область

$\begin{aligned}
 \Omega = \bigcup_{\alpha=1}^{m} \Omega_\alpha  
\end{aligned}$

Ячейки
 
$\begin{aligned}
 \Omega_\alpha = \{ x \ | \ \bar{x}_{\alpha -1} \leq x \leq \bar{x}_\alpha\}, \ \alpha = 1, 2, \ldots , m 
\end{aligned}$

**Аппроксимация на ячейке**

Полином степени $p$

$y(x) = a_0 + a_1 x + \cdots + a_p x^p$

Узлы аппроксимации

* два узла сетки
* $p-1$ внутренних узла (равномерное разбиение ячейки)

    """    
    
if menu == "Базисные функции":
    r"""
##### Базисные функции

$\begin{aligned}
 \varphi_i(x),
 \quad i = 1,2, \ldots, n 
\end{aligned}$

$\begin{aligned}
 \varphi_i(x_j) = \begin{cases}
  1 ,  &  i = j \\
  0 ,  &  i \neq j \\
\end{cases}
\end{aligned}$
    """
    tab1, tab2 = st.tabs([" **Визуализация (FEniCS)** ", " **1D  базисные функции МКЭ (код)** "])

    with tab1:
        import matplotlib.pyplot as plt
        import numpy as np
        from fenics import *

        c1, cc, c2 = st.columns([5,1,5])
        c1.write("$~~$")
        c1.write("Число ячеек")
        m = c2.slider("m", 2, 20, 5)
        c1.write("$~~$")
        c1.write("Порядок полинома")
        p = c2.slider("p", 1, 5, 2)

        a = 0.
        b = 1.

        mesh = IntervalMesh(m, a, b)
        xm = mesh.coordinates()
        ym = np.zeros((m+1), "float")

        V = FunctionSpace(mesh, "CG", p)
        n = V.dim()-1

        c1.write("$~~$")
        c1.write("Базисная функция")
        k = c2.slider("k", 0, n, 0)
        u = Function(V)
        u.vector()[k] = 1

        xn = np.linspace(a, b, n+1)
        yn = np.zeros((n+1), "float")

        N = 500
        xx = np.linspace(a, b, N)
        yy = np.linspace(a, b, N)

        for i in range(0, N):
            yy[i]  = u(Point(xx[i]))

        fig1 = plt.figure(1)
        ss = "$m = $" + str(m) + "$, \ p = $" + str(p)
        plt.title(ss)

        plt.scatter(xn, yn)
        plt.scatter(xm, ym)
        plt.plot(xx, yy)

        plt.xlabel('$x$')
        plt.grid(True)

        c1, c2, = st.columns([3,1])
        c1.pyplot(fig1)

    with tab2:
            code = """  
    import matplotlib.pyplot as plt
    import numpy as np
    from fenics import *
    
    a = 0; b = 1
    m = 3; p = 2
    
    mesh = IntervalMesh(m, a, b)
    V = FunctionSpace(mesh, "CG", p)
    N = 500
    xx = np.linspace(a, b, N)
    yy = np.linspace(a, b, N)
    
    k = 4
    u = Function(V)
    u.vector()[k] = 1
    for i in range(0, N):
        yy[i]  = u(Point(xx[i]))
    plt.plot(xx, yy, label=f"$k = ${k}")
    plt.show()
            """
            st.code(code, language="python")


if menu == "1D интерполяция":
    r"""
##### 1D интерполяция
**Постановка задачи**

Интерполирование данных в равноотстоящих узлах для функции Рунге

$\begin{aligned}
 f(x) = \frac{1}{1 + 25 x^2}
\end{aligned}$

на интервале $[-1,1]$ при различном числе ячеек и степени полинома 

    """
    tab1, tab2 = st.tabs([" **FEniCS** ", " **Фрагмент кода** "])

    with tab1:
        import matplotlib.pyplot as plt
        import numpy as np
        from fenics import *

        def f(x):
            return 1./(1.+25*x**2)

        c1, cc, c2 = st.columns([5,1,5])
        c1.write("$~~$")
        c1.write("Число ячеек")
        m = c2.slider("m", 2, 20, 5)
        c1.write("$~~$")
        c1.write("Порядок полинома")
        p = c2.slider("p", 1, 5, 2)

        a = -1.
        b = 1.

        mesh = IntervalMesh(m, a, b)
        xm = mesh.coordinates()
        ym = np.zeros((m+1), "float")

        V = FunctionSpace(mesh, "CG", p)
        n = V.dim()-1

        fr = Expression("1/(1+25*x[0]*x[0])", degree=p)
        u = interpolate(fr, V)

        N = 500
        xx = np.linspace(a, b, N)
        yy = np.linspace(a, b, N)
        ye = f(xx)

        for i in range(0, N):
            yy[i]  = u(Point(xx[i]))

        fig1 = plt.figure(1)
        ss = "$m = $" + str(m) + "$, \ p = $" + str(p)
        plt.title(ss)

        plt.scatter(xm, ym)
        plt.plot(xx, ye)
        plt.plot(xx, yy)

        plt.xlabel('$x$')
        plt.grid(True)
    
        c1, c2, = st.columns([3,1])
        c1.pyplot(fig1)

    with tab2:
        code = """  
    mesh = IntervalMesh(m, a, b)
    V = FunctionSpace(mesh, "CG", p)
    
    fr = Expression("1/(1+25*x[0]*x[0])", degree=p+2)
    u = interpolate(fr, V)
            """
        st.code(code, language="python")
    
if menu == "1D приближение":
    r"""
##### 1D приближение

**Постановка задачи**

Выполнить конечно-элементную аппроксимацию функции Рунге

$\begin{aligned}
 f(x) = \frac{1}{1 + 25 x^2}
\end{aligned}$

на интервале $[-1,1]$ при различном числе ячеек и степени полинома 

    """
    tab1, tab2 = st.tabs([" **FEniCS** ", " **Фрагмент кода** "])

    with tab1:
        import matplotlib.pyplot as plt
        import numpy as np
        from fenics import *

        def f(x):
            return 1./(1.+25*x**2)

        c1, cc, c2 = st.columns([5,1,5])
        c1.write("$~~$")
        c1.write("Число ячеек")
        m = c2.slider("m", 2, 20, 4)
        c1.write("$~~$")
        c1.write("Порядок полинома")
        p = c2.slider("p", 1, 5, 2)

        a = -1.
        b = 1.

        mesh = IntervalMesh(m, a, b)
        xm = mesh.coordinates()
        ym = np.zeros((m+1), "float")

        V = FunctionSpace(mesh, "CG", p)
        n = V.dim()-1

        u = TrialFunction(V)
        v = TestFunction(V)
        fr = Expression("1/(1+25*x[0]*x[0])", degree=p+2)
        va = u*v*dx
        vL = fr*v*dx

        # Вычисление
        u = Function(V)
        solve(va == vL, u)

        N = 500
        xx = np.linspace(a, b, N)
        yy = np.linspace(a, b, N)
        ye = f(xx)

        for i in range(0, N):
            yy[i]  = u(Point(xx[i]))

        fig1 = plt.figure(1)
        ss = "$m = $" + str(m) + "$, \ p = $" + str(p)
        plt.title(ss)

        plt.scatter(xm, ym)
        plt.plot(xx, ye)
        plt.plot(xx, yy)

        plt.xlabel('$x$')
        plt.grid(True)

        c1, c2, = st.columns([3,1])
        c1.pyplot(fig1)

        with tab2:
            code = """  
        mesh = IntervalMesh(m, a, b)
        V = FunctionSpace(mesh, "CG", p)
        u = TrialFunction(V)
        v = TestFunction(V)
        
        fr = Expression("1/(1+25*x[0]*x[0])", degree=p+2)
        L = fr*v*dx
        
        u = Function(V)
        solve(a == L, u)
            """
            st.code(code, language="python")