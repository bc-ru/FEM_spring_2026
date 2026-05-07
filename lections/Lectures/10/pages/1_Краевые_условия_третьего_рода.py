import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Постановка задачи", 
    "Интегральное тождество", 
    "Вариационная задача",
    "Тестовая задача",
    "Ключевые фрагменты кода (FEniCS)",
    "Матрица СЛАУ",
    "Влияние краевых условий",    
    )
)
  
if menu == "Постановка задачи":
    r"""
##### Постановка задачи

Уравнение

$\begin{aligned} 
 \mathcal{L} u \equiv -  \frac{d}{dx} \left (k(x) \frac{du}{dx} \right ) + q(x) u = f(x),
  \quad a < x < b
\end{aligned}$

с переменными коэффициентами

$\begin{aligned}
  k(x) \geq \kappa > 0,
  \quad q(x) \geq 0
\end{aligned}$

Граничные условия третьего рода

$\begin{aligned} -
  k(a) \frac{d u}{d x}(a) + \sigma_1 u(a) = \mu_1,
  \quad k(b) \frac{d u}{d x}(b) + \sigma_2 u(b) = \mu_2 
\end{aligned}$

с коэффициентами

$\begin{aligned}
  \sigma_1 \geq 0 \quad  \sigma_2 \geq 0
\end{aligned}$

    """    
    
if menu == "Интегральное тождество":
    r"""
##### Интегральное тождество


$V$ - пространство достаточно гладких функций

Для $u \in V$ и $v \in V$  
  
$\begin{aligned}
 (\mathcal{L} u, v) &= - \int_{a}^{b} \frac{d}{dx} \left (k(x) \frac{du}{dx} \right ) v(x) d x + \int_{a}^{b}  q(x) u(x) v(x) dx = \\
 & = - {\color {red} k(x) \frac{du}{dx}   v(x)} \Big |_a^b +  \int_{a}^{b} k(x) \frac{du}{dx} \frac{dv}{dx} d x + \int_{a}^{b}  q(x) u(x) v(x) dx
\end{aligned}$

С учетом граничных условий

$\begin{aligned}
 (\mathcal{L} u, v) & =  {\color {red} (\sigma_1 u(a) - \mu_1) v(a) + (\sigma_2 u(b) - \mu_2) v(b)} + \\
& +  \int_{a}^{b} k(x) \frac{du}{dx} \frac{dv}{dx} d x + \int_{a}^{b}  q(x) u(x) v(x) dx = \\
& = \int_{a}^{b} f(x) v(x) d x 
\end{aligned}$

    """  
    
if menu == "Вариационная задача":
    r"""
##### Вариационная задача

Билинейная форма 

$\begin{aligned}
 a(u,v) = \int_{a}^{b} k(x) \frac{du}{dx} \frac{dv}{dx} d x + \sigma_1 u(a) v(a) + \sigma_2 u(b) v(b) + \int_{a}^{b}  q(x) u(x) v(x) dx
\end{aligned}$

Линейная форма 

$\begin{aligned}
 l(v) = \int_{a}^{b} f(x) v(x) d x + \mu_1 v(a) + \mu_2 v(b)
\end{aligned}$

Вариационная задача: найти $u \in V$ 

$\begin{aligned}
 a(u,v) = l(v) \quad \forall v \in V
\end{aligned}$

Классы граничных условий 

* естественные: включены в вариационную формулировку (граничные условия третьего рода)

* главные: искомое решение из подпространства (условие Дирихле)

    """   
    
if menu == "Тестовая задача":
    r"""
##### Тестовая задача

Уравнение

$\begin{aligned} - 
 \frac{d}{dx} \left (k(x) \frac{du}{dx} \right ) = 1,
  \quad 0 < x < 1
\end{aligned}$

с переменным коэффициентом

$\begin{aligned}
 k(x) = \begin{cases}
  1 ,  &  0 \leq x < 0.5 \\
  \kappa ,  &  0.5 \leq x \leq 1 \\
\end{cases}
\end{aligned}$

Граничные условия 

$\begin{aligned} -
  k(a) \frac{d u}{d x}(a) + \sigma u(a) = 0,
  \quad k(b) \frac{d u}{d x}(b) + \sigma u(b) = 0
\end{aligned}$

    """ 

if menu == "Ключевые фрагменты кода (FEniCS)":
    r"""
##### Ключевые фрагменты кода (FEniCS)

**Вариационная формулировка задачи**
    """    
    code = """  
f = Expression("1", degree=p+2)
kk = Expression("x[0] < 0.5 ? 1 : kap", kap = kap, degree=p+2)
a = kk*dot(grad(u), grad(v))*dx + sig*u*v*ds
L = f*v*dx
    """ 
    st.code(code, language="python")    
    r"""        
**Решение задачи**
    """    
    code = """  
w = Function(V)
solve(a == L, w)
    """ 
    st.code(code, language="python")   
    
if menu == "Матрица СЛАУ":
    r"""
##### Матрица СЛАУ

**Параметры задачи**

    """

    import matplotlib.pyplot as plt
    import numpy as np 
    from fenics import *
    from scipy.sparse import csr_matrix
    
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Число ячеек $m$")        
    m = c2.slider("", 10, 50, 20)
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Порядок полинома $p$")        
    p = c2.slider("", 1, 3, 1)  
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Коэффициент в уравнении $\kappa$")        
    kap = c2.slider("", 0.01, 10., 5., 0.1)     
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Коэффициент в граничном условии $\sigma$")        
    sig = c2.slider("", 10., 1000., 20., 1.)     

     
    mesh = IntervalMesh(m, 0, 1)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    V = FunctionSpace(mesh, "CG", p)
    n = V.dim()-1
    
    u = TrialFunction(V)
    v = TestFunction(V)
    
    f = Expression("1", degree=p+2)
    kk = Expression("x[0] < 0.5 ? 1 : kap", kap = kap, degree=p+2)
    a = kk*dot(grad(u), grad(v))*dx + sig*u*v*ds
    L = f*v*dx

    A = assemble(a)
    mat = as_backend_type(A).mat()
    csr = csr_matrix(mat.getValuesCSR()[::-1], shape=mat.size)
    Ad = csr.toarray()

    # Форматирование: убираем trailing zeros и точу для целых
    def format_element(val):
        if abs(val) < 1e-12:  # нулевые элементы
            return ''
        s = f"{val:g}"  # компактный формат без лишних нулей
        return s.rstrip('0').rstrip('.') if '.' in s else s

    # Создаем отформатированный массив строк
    Ad_formatted = np.vectorize(format_element)(Ad)

    tab1, tab2 = st.tabs([" **Портрет матрицы** ", " **Элементы матрицы** "])

    with tab1:
        fig1 = plt.figure(1)
        plt.spy(csr, marker='o', markersize=150/n, color='blue')
        c1, c2 = st.columns([3,1])
        c1.pyplot(fig1)

    with tab2:
        st.dataframe(Ad_formatted, use_container_width=True)

if menu == "Влияние краевых условий":
    r"""
##### Влияние краевых условий

Коэффициент $\sigma$ увеличивается в 10 и 100 раз

    """

    import matplotlib.pyplot as plt
    import numpy as np
    from fenics import *

    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Число ячеек $m$")
    m = c2.slider("", 10, 50, 20)
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Порядок полинома $p$")
    p = c2.slider("", 1, 3, 1)
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Коэффициент в уравнении $\kappa$")
    kap = c2.slider("", 0.01, 10., 5., 0.1)
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Коэффициент в граничном условии $\sigma$")
    sig = c2.slider("", 10., 1000., 20., 1.)

    fig1 = plt.figure(1)

    for kk in range(0, 3):

        mesh = IntervalMesh(m, 0, 1)
        xm = mesh.coordinates()
        ym = np.zeros((m+1), "float")

        V = FunctionSpace(mesh, "CG", p)
        n = V.dim()-1

        u = TrialFunction(V)
        v = TestFunction(V)

        f = Expression("1", degree=p+2)
        kk = Expression("x[0] < 0.5 ? 1 : kap", kap = kap, degree=p+2)  # qqq
        a = kk*dot(grad(u), grad(v))*dx + sig*u*v*ds
        L = f*v*dx

        w = Function(V)
        solve(a == L, w)

        N = 500
        xx = np.linspace(0., 1., N)
        yy = np.linspace(0., 1., N)

        for i in range(0, N):
            yy[i]  = w(Point(xx[i]))
        s = "$\\sigma = $" + str(sig)
        plt.plot(xx, yy, label = s)
        sig = sig*10

    ss = "$m = $" + str(m) + "$, \ p = $" + str(p) + "$, \ \kappa = $" + str(kap)
    plt.title(ss)
    plt.scatter(xm, ym)
    plt.xlabel('$x$')
    plt.legend(loc=0)
    plt.grid(True)

    c1, c2, = st.columns([3,1])
    c1.pyplot(fig1)
    
    
    
    
    
    
    