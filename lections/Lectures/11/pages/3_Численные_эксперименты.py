import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Тестовая задача", 
    "Ключевые фрагменты кода (FEniCS)", 
    "Параметрические расчеты", 
    )
)

if menu == "Тестовая задача":
    r"""
##### Тестовая задача

**Область**

$\Omega = \{ \bm x \ | \ \bm x = (x_1, x_2), \ 0 < x_1 < 1, \ 0 < x_2 < 1\} ~-~$ единичный квадрат

**Уравнение**

$\begin{aligned} - 
 \operatorname{div} \operatorname{grad} u + c(\bm x) u = 1 ,
 \quad x \in \Omega
\end{aligned}$

с переменным коэффициентом ($c(\bm x) \ge 0$)

$\begin{aligned}
 c(\bm x) = \begin{cases}
  0 ,  &  x_1 < 0.5 \ \operatorname{or} \ x_2 < 0.5\\
  c ,  &  x_1 > 0.5 \ \operatorname{and} \ x_2 > 0.5 \\
\end{cases}
\end{aligned}$

**Части границы**

* $\Gamma_D = \{ \bm x \ | \ \bm x \in \partial \Omega, \ x_1 = 0 \ \operatorname{or} \ x_2 = 0 \}$
* $\Gamma_N = \{ \bm x \ | \ \bm x \in \partial \Omega, \ x_1 > 0 \ \operatorname{and} \ x_2 > 0 \}$

**Граничные условия**

$\begin{aligned}
  u(\bm x) = 0, 
  \quad \bm x \in \Gamma_D
\end{aligned}$

$\begin{aligned}
  \frac{\partial u}{\partial n} = 0,
  \quad \bm x \in \Gamma_N
\end{aligned}$

    """     
if menu == "Ключевые фрагменты кода (FEniCS)":
    r"""
##### Ключевые фрагменты кода (FEniCS)

**Сетка**
    """    
    code = """  
mesh = UnitSquareMesh(m, m)
    """ 
    st.code(code, language="python")  
    r"""    
**Части границы**
    """    
    code = """  
boundary_markers = MeshFunction('size_t', mesh, mesh.topology().dim()-1)
tol = 1E-14
b0 = CompiledSubDomain("on_boundary && near(x[0], 0, tol)", tol=tol)
b1 = CompiledSubDomain("on_boundary && near(x[1], 0, tol)", tol=tol)
b0.mark(boundary_markers, 0)
b1.mark(boundary_markers, 1)
ds = Measure("ds", domain=mesh, subdomain_data=boundary_markers)
    """ 
    st.code(code, language="python")    
    r"""        
**Граничные условия Дирихле**
    """    
    code = """  
def boundary(x, on_boundary):u_D = Expression("0", degree=p+2)
bcs = [DirichletBC(V, u_D, b0), DirichletBC(V, u_D, b1)]
    """ 
    st.code(code, language="python")   
    r"""    
**Вариационная формулировка задачи**
    """    
    code = """  
f = Expression("1", degree=p+2)
cc = Expression("x[0] > 0.5 and x[1] > 0.5 ? c : 0", c = c, degree=p+2)
a = dot(grad(u), grad(v))*dx + cc*u*v*dx
L = f*v*dx 
    """ 
    st.code(code, language="python")    
    r"""        
**Решение задачи**
    """    
    code = """  
w = Function(V)
solve(a == L, w, bcs)    
    """ 
    st.code(code, language="python")       
         
                   
if menu == "Параметрические расчеты":
    r"""
##### Параметрические расчеты

    """

    import matplotlib.pyplot as plt
    import numpy as np 
    from fenics import *
    from scipy.sparse import csr_matrix
    
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Число ячеек $m$")        
    m = c2.slider("", 4, 20, 10)
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Порядок полинома $p$")        
    p = c2.slider("", 1, 3, 1)  
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Коэффициент $c$")        
    c = c2.slider("", 0, 1000, 100, 10)     
      
    mesh = UnitSquareMesh(m, m)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    V = FunctionSpace(mesh, "CG", p)
    n = V.dim()-1
    
    u = TrialFunction(V)
    v = TestFunction(V)
    
    boundary_markers = MeshFunction('size_t', mesh, mesh.topology().dim()-1)
    tol = 1E-14
    b0 = CompiledSubDomain("on_boundary && near(x[0], 0, tol)", tol=tol)
    b1 = CompiledSubDomain("on_boundary && near(x[1], 0, tol)", tol=tol)
    b0.mark(boundary_markers, 0)
    b1.mark(boundary_markers, 1)
    ds = Measure("ds", domain=mesh, subdomain_data=boundary_markers)
    
    u_D = Expression("0", degree=p+2)
    bcs = [DirichletBC(V, u_D, b0), DirichletBC(V, u_D, b1)]
    
    
    f = Expression("1", degree=p+2)
    cc = Expression("x[0] > 0.5 and x[1] > 0.5 ? c : 0", c = c, degree=p+2)
    a = dot(grad(u), grad(v))*dx + cc*u*v*dx
    L = f*v*dx 
    
    A, b = assemble_system(a, L, bcs)

    mat = as_backend_type(A).mat()
    csr = csr_matrix(mat.getValuesCSR()[::-1], shape=mat.size)
    Ad = csr.toarray()
    
    tab1, tab2 = st.tabs([" **Портрет матрицы** ", " **Решение** "])

    with tab1:
        fig1 = plt.figure(1)
        plt.spy(csr, marker='o', markersize=75/n, color='blue')

        c1, c2, = st.columns([3,1])
        c1.pyplot(fig1)

        w = Function(V)
        solve(a == L, w, bcs)

    with tab2:
        N = 200
        x = np.linspace(0,1,N)
        y = np.linspace(0,1,N)
        yy  = np.zeros((N,N))
        ye  = np.zeros((N,N))
        tk = np.linspace(0,1,m+1)

        for i in range(0, N):
            for j in range(0, N):
                pp = Point(x[i],y[j])
                yy[j,i] = w(pp)

        fig2 = plt.figure(2)
        ss = "$m = $" + str(m) + "$, \ p = $" + str(p) + "$, \ c = $" + str(c)
        plt.title(ss)
        plt.contourf(x,y,yy)
        plt.gca().set_aspect("equal")
        plt.colorbar()
        plt.grid(True)
        plt.xticks(ticks=tk)
        plt.yticks(ticks=tk)

        c1, c2, = st.columns([3,1])
        c1.pyplot(fig2)
 
    
