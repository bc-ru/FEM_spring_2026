import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Постановка задачи", 
    "Интегральное тождество", 
    "Вариационная задача",
    "Тестовая задача",
    "Ключевые фрагменты кода (FEniCS)",
    "Матрица СЛАУ",
    "Влияние конвективного переноса",    
    )
)
  
if menu == "Постановка задачи":
    r"""
##### Постановка задачи

Уравнение конвекции-диффузии

$\begin{aligned} 
 \mathcal{L} u \equiv -  \frac{d}{dx} \left (k(x) \frac{du}{dx} \right ) + c(x)  \frac{du}{dx} = f(x),
  \quad a < x < b
\end{aligned}$

с переменными коэффициентами

$\begin{aligned}
  k(x) \geq \kappa > 0,
  \quad c(x) 
\end{aligned}$

Граничные условия Дирихле

$\begin{aligned} 
  u(a) = \mu_1,
  \quad u(b) = \mu_2 
\end{aligned}$

Уравнение в дивергентной форме

$\begin{aligned} -
 \frac{d}{dx} \left (k(x) \frac{du}{dx} \right ) + \frac{d}{dx} (c(x) u) = f(x)
\end{aligned}$

Уравнение в симметричной форме

$\begin{aligned} -
\frac{d}{dx} \left (k(x) \frac{du}{dx} \right ) + \frac{1}{2} \Big ( c(x)  \frac{du}{dx}  + \frac{d}{dx} (c(x) u) \Big ) = f(x)
\end{aligned}$
    """    
    
if menu == "Интегральное тождество":
    r"""
##### Интегральное тождество

Пространства

* $V$ - пространство достаточно гладких функций

* Подпространство $V_D = \{ v \ | \ v \in V, \quad v(a) = \mu_1,
  \quad u(b) = \mu_2 \}$ 
  
* Подпространство $V_0 = \{ v \ | \ v \in V, \quad v(a) = 0,
  \quad u(b) = 0 \}$  
  
Для $u \in V_D$ и $v \in V_0$  
  
$\begin{aligned}
 (\mathcal{L} u, v) &= - \int_{a}^{b} \frac{d}{dx} \left (k(x) \frac{du}{dx} \right ) v(x) d x + \int_{a}^{b}  c(x) \frac{du}{dx} v(x) dx = \\
 & = - {\color {red} k(x) \frac{du}{dx} v(x)} \Big |_a^b +  \int_{a}^{b} k(x) \frac{du}{dx} \frac{dv}{dx} d x + \int_{a}^{b}  c(x) \frac{du}{dx} v(x) dx
\end{aligned}$

Интегральное тождество

$\begin{aligned}
(\mathcal{L} u - f, v) = 0 , 
\quad u \in V_D, \ v \in V_0
\end{aligned}$

С учетом $v \in V_0$ 

$\begin{aligned}
 \int_{a}^{b} k(x) \frac{du}{dx} \frac{dv}{dx} d x + \int_{a}^{b}     c(x) \frac{du}{dx} v(x) dx = \int_{a}^{b} f(x) v(x) d x 
\end{aligned}$

    """  
    
if menu == "Вариационная задача":
    r"""
##### Вариационная задача


Билинейная форма 

$\begin{aligned}
 a(u,v) = \int_{a}^{b} k(x) \frac{du}{dx} \frac{dv}{dx} d x + \int_{a}^{b}  c(x) \frac{du}{dx} v(x) dx
\end{aligned}$

Линейная форма 

$\begin{aligned}
 l(v) = \int_{a}^{b} f(x) v(x) d x
\end{aligned}$

Вариационная задача: найти  $u \in V_D$ такую, что

$\begin{aligned}
 a(u,v) = l(v) ,
 \quad \forall v \in V_0
\end{aligned}$

    """   
    
if menu == "Тестовая задача":
    r"""
##### Тестовая задача

Уравнение

$\begin{aligned} - 
 \frac{d^2 u}{dx^2} +   c \frac{du}{dx} = 0,
  \quad 0 < x < 1
\end{aligned}$

с коэффициентом $c(x) = c = \mathrm{const}$

Граничные условия 

$\begin{aligned} 
  u(a) = 0,
  \quad u(b) = 1
\end{aligned}$

Особые случаи

+ $|c| \ll 1 ~~- ~$ преобладание диффузии
+ $|c| \gg 1 ~~- ~$ преобладание конвекции

    """ 

if menu == "Ключевые фрагменты кода (FEniCS)":
    r"""
##### Ключевые фрагменты кода (FEniCS)
     
**Граничные условия Дирихле**
    """    
    code = """  
def boundary(x, on_boundary):
    return on_boundary
bc = DirichletBC(V, Expression("x[0]", degree=p+2), boundary)
    """ 
    st.code(code, language="python")   
    r"""    
**Вариационная формулировка задачи**
    """    
    code = """  
f = Expression("0.", degree=p+2)
a = u.dx(0)*v.dx(0)*dx + cc*u.dx(0)*v*dx
L = f*v*dx
    """ 
    st.code(code, language="python")    
    r"""        
**Решение задачи**
    """    
    code = """  
w = Function(V)
solve(a == L, w, bc)    
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
    c1.write("Коэффициент при конвективном слагаемом $c$")        
    c = c2.slider("", -10, 10, 1, 1)     
     
    mesh = IntervalMesh(m, 0, 1)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    V = FunctionSpace(mesh, "CG", p)
    n = V.dim()-1
    
    u = TrialFunction(V)
    v = TestFunction(V)
    
    def boundary(x, on_boundary):
        return on_boundary
    bc = DirichletBC(V, Expression("x[0]", degree=p+2), boundary)
    
    f = Expression("0.", degree=p+2)
    cc = Constant(c)
    a = u.dx(0)*v.dx(0)*dx + cc*u.dx(0)*v*dx
    L = f*v*dx
    
    A = assemble(a)
    b = assemble(L)
    bc.apply(A,b)
    A, b = assemble_system(a,L,bc)
    
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
         
if menu == "Влияние конвективного переноса":
    r"""
##### Влияние конвективного переноса

Коэффициент $c$ увеличивается в 10 и 100 раз

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
    c1.write("Коэффициент при конвективном слагаемом $c$")        
    c = c2.slider("", -10, 10, 1, 1)      
          
    fig1 = plt.figure(1)
    
    for kk in range(0, 3): 
    
        mesh = IntervalMesh(m, 0, 1)
        xm = mesh.coordinates()
        ym = np.zeros((m+1), "float") 
        
        V = FunctionSpace(mesh, "CG", p)
        n = V.dim()-1
        
        u = TrialFunction(V)
        v = TestFunction(V)
        
        def boundary(x, on_boundary):
            return on_boundary
        bc = DirichletBC(V, Expression("x[0]", degree=p+2), boundary)
        
        f = Expression("0.", degree=p+2)
        cc = Constant(c)
        a = u.dx(0)*v.dx(0)*dx + cc*u.dx(0)*v*dx
        L = f*v*dx
    
        w = Function(V)
        solve(a == L, w, bc)
        
        N = 500
        xx = np.linspace(0., 1., N) 
        yy = np.linspace(0., 1., N)  
        
        for i in range(0, N): 
            yy[i]  = w(Point(xx[i]))
        s = "$c = $" + str(c)
        plt.plot(xx, yy, label = s) 
        c = c*10 
    
    ss = "$m = $" + str(m) + "$, \ p = $" + str(p) 
    plt.title(ss)
    plt.xlabel('$x$') 
    plt.legend(loc=0)
    plt.grid(True)      
    
    c1, c2, = st.columns([3,1]) 
    c1.pyplot(fig1)  
 

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
