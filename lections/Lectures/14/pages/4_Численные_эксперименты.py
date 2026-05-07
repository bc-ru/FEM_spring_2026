import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Тестовая задача", 
    "Ключевые фрагменты кода (FEniCS)", 
    "Численные результаты", 
    )
)

if menu == "Тестовая задача":
    r"""
##### Тестовая задача

**Область**

$\Omega = \{ \bm x \ | \ \bm x = (x_1, x_2), \ 0 < x_1 < 1, \ 0 < x_2 < 1\} $

**Уравнение**

$\begin{aligned} - 
 \operatorname{div} (k(u) \operatorname{grad} u ) = 1 ,
 \quad \bm x \in \Omega
\end{aligned}$

Коэффициент

$\begin{aligned}
  k(u) = 1 + \alpha u^{\beta},
  \quad \alpha , \beta \ge 0
\end{aligned}$

**Граничные условия**

$\begin{aligned}
  u(\bm x) = 0,
  \quad \bm x \in \partial\Omega
\end{aligned}$

    """     
   
if menu == "Ключевые фрагменты кода (FEniCS)":
    r"""
##### Ключевые фрагменты кода (FEniCS)

**Коэффициент уравнения**
    """    
    code = """  
def k(u):
    return 1 + al*u**bet
def kp(u):
    return al*bet*u**(bet-1)
    """ 
    st.code(code, language="python")   
    r"""       
**Нелинейный реашатель FEniCS**
    """    
    code = """  
u = TrialFunction(V)
v = TestFunction(V)
w = Function(V)

f = Expression("1", degree=p+2) 
bc = DirichletBC(V,  Expression("0.", degree=p+2), "on_boundary")

F = (k(w) * dot(grad(w), grad(v)) - f * v) * dx
solve(F == 0, w, bc)
    """ 
    st.code(code, language="python")   

    r"""        
**Простая линеаризация**
    """    
    code = """  
a1 = k(u1) * dot(grad(u), grad(v))*dx 
L1 = f*v*dx 
solve(a1 == L1, u1, bc)
    """ 
    st.code(code, language="python")  
        
    r"""        
**Метод Ньютона**
    """    
    code = """  
a2 = k(u2) * dot(grad(u), grad(v))*dx + dot(kp(u2)*u*grad(u2),grad(v))*dx
L2 = dot(kp(u2)*u2*grad(u2),grad(v))*dx + f*v*dx 
solve(a2 == L2, u2, bc)
    """ 
    st.code(code, language="python") 
             
    r"""           
**Погрешность на отдельной итерации**
    """    
    code = """  
er1 = assemble((u1-w) ** 2 * dx) ** 0.5
er2 = assemble((u2-w) ** 2 * dx) ** 0.5
    """ 
    st.code(code, language="python")  
         
if menu == "Численные результаты":
    r"""
##### Численные результаты

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
    c1.write(r"""Параметр $~\alpha$""")        
    al = c2.slider("", 0.1, 10., 5., 0.1)  
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write(r"""Параметр $~\beta$""")        
    bet = c2.slider("", 0.5, 5., 2., 0.1)     
      
    def k(u):
        return 1 + al*u**bet
    def kp(u):
        return al*bet*u**(bet-1)
    
    mesh = UnitSquareMesh(m, m)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    V = FunctionSpace(mesh, "CG", p)
    n = V.dim()-1
    
    u = TrialFunction(V)
    v = TestFunction(V)
    w = Function(V)
    
    f = Expression("1", degree=p+2) 
    bc = DirichletBC(V,  Expression("0.", degree=p+2), "on_boundary")
    
    F = (k(w) * dot(grad(w), grad(v)) - f * v) * dx
    solve(F == 0, w, bc)
    
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
              
    fig1 = plt.figure(1)
    plt.contourf(x,y,yy)
    plt.gca().set_aspect("equal")
    plt.colorbar()
    
    tab1, tab2 = st.tabs([" **Решение (нелинейный решатель FEniCS)** " , " **Погрешность на итерациях** "])

    with tab1:
        c1, c2, = st.columns([3,1])
        c1.pyplot(fig1)

        itMax = 9
        ii = []
        ei1 = []
        ei2 = []

        u_0 = Expression("0", degree=p+2)
        u1 = project(u_0, V)
        u2 = project(u_0, V)
        for it in range(0, itMax):

            a1 = k(u1) * dot(grad(u), grad(v))*dx
            L1 = f*v*dx
            solve(a1 == L1, u1, bc)
            er1 = assemble((u1-w) ** 2 * dx) ** 0.5

            a2 = k(u2) * dot(grad(u), grad(v))*dx + dot(kp(u2)*u*grad(u2),grad(v))*dx
            L2 = dot(kp(u2)*u2*grad(u2),grad(v))*dx + f*v*dx
            solve(a2 == L2, u2, bc)
            er2 = assemble((u2-w) ** 2 * dx) ** 0.5

            ii.append(it+1)
            ei1.append(er1)
            ei2.append(er2)

    with tab2:
        fig2 = plt.figure(2)
        st1 = "простая линеаризация"
        st2 = "метод Ньютона"
        plt.semilogy(ii,ei1,label=st1)
        plt.semilogy(ii,ei2,label=st2)
        plt.legend(loc=0)
        plt.xlabel('$k$')
        plt.ylabel('$\\varepsilon$')
        plt.grid(True)

        c1, c2, = st.columns([3,1])
        c1.pyplot(fig2)

    
 
    



























