import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Тестовая задача", 
    "Ключевые фрагменты кода (FEniCS)", 
    "Численное решение", 
    )
)

if menu == "Тестовая задача":
    r"""
##### Тестовая задача

**Область**

$\Omega = \{ \bm x \ | \ \bm x = (x_1, x_2), \ 0 < x_1 < 1, \ 0 < x_2 < 1\} ~-~$ единичный квадрат

**Система уравнений**

$\begin{aligned}
& - \operatorname{div} \operatorname{grad} \bm u + \operatorname{grad} p = 0 \\
&  \operatorname{div} \bm u = 0,
\quad \bm x \in \Omega
\end{aligned}$

**Граничные условия**

$\begin{aligned}
 \bm g(\bm x) = \begin{cases}
  (1,0) ,  &  x_2 = 1 \\
  (0,0) ,  &   x_2 < 1 \\
\end{cases}
  \quad \bm x \in \partial \Omega
\end{aligned}$

    """     
if menu == "Ключевые фрагменты кода (FEniCS)":

    r"""
##### Ключевые фрагменты кода (FEniCS)

**Конечно-элементное пространство**

* векторные лагранжевые элементы степени $pp$ для скорости
* скалярные лагранжевые элементы степени $pp-1$ для давления

    """    
    code = """  
U = VectorElement("Lagrange", mesh.ufl_cell(), pp)
P = FiniteElement("Lagrange", mesh.ufl_cell(), pp-1)
V = FunctionSpace(mesh, U*P)

u, p = TrialFunctions(V)
v, q = TestFunctions(V)
    """ 
    st.code(code, language="python")  
 
    r"""        
**Граничные условия Дирихле**
    """    
    code = """  
def on_top(x, on_boundary):
    return near(x[1], 1) and on_boundary
def no_top(x, on_boundary):
    return on_boundary and not near(x[1], 1) 

bc1 = DirichletBC(V.sub(0), Constant((1,0)), on_top)
bc2 = DirichletBC(V.sub(0), Constant((0,0)), no_top)
bcs = [bc1, bc2]
    """ 
    st.code(code, language="python")   
    r"""    
**Вариационная формулировка задачи**
    """    
    code = """  
F = inner(grad(u), grad(v))*dx - div(v)*p*dx + q*div(u)*dx 
a = lhs(F)
L = rhs(F)
    """ 
    st.code(code, language="python")    
    r"""        
**Решение задачи**
    """    
    code = """  
w = Function(V)
solve(a == L, w, bcs)
us, ps = w.split(True)
u1, u2 = us.split(True)
    """ 
    st.code(code, language="python")       
         
                   
if menu == "Численное решение":
    r"""
##### Численное решение

    """

    import matplotlib.pyplot as plt
    import numpy as np 
    from fenics import *
    import pandas as pd
    
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Число ячеек $m$")        
    m = c2.slider("", 10, 50, 20, 1)
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Порядок полинома $p$")        
    pp = c2.slider("", 2, 4, 2)  
        
    mesh = UnitSquareMesh(m, m)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    U = VectorElement("Lagrange", mesh.ufl_cell(), pp)
    P = FiniteElement("Lagrange", mesh.ufl_cell(), pp-1)
    V = FunctionSpace(mesh, U*P)
    
    u, p = TrialFunctions(V)
    v, q = TestFunctions(V)
    
    def on_top(x, on_boundary):
        return near(x[1], 1) and on_boundary
    def no_top(x, on_boundary):
        return on_boundary and not near(x[1], 1) 
    
    bc1 = DirichletBC(V.sub(0), Constant((1,0)), on_top)
    bc2 = DirichletBC(V.sub(0), Constant((0,0)), no_top)
    bcs = [bc1, bc2]
    
    F = inner(grad(u), grad(v))*dx - div(v)*p*dx + q*div(u)*dx 
    a = lhs(F)
    L = rhs(F)
    
    w = Function(V)
    solve(a == L, w, bcs)
    us, ps = w.split(True)
    u1, u2 = us.split(True)
    
    N = 200
    x = np.linspace(0,1,N)
    y = np.linspace(0,1,N)
    yy  = np.zeros((N,N)) 
    ye  = np.zeros((N,N)) 
    tk = np.linspace(0,1,m+1)
    
    for i in range(0, N): 
        for j in range(0, N): 
            pp = Point(x[i],y[j])
            yy[j,i] = u1(pp)
              
    fig1 = plt.figure(1)
    plt.contourf(x,y,yy)
    plt.gca().set_aspect("equal")
    plt.colorbar()
    
    for i in range(0, N): 
        for j in range(0, N): 
            pp = Point(x[i],y[j])
            yy[j,i] = u2(pp)
              
    fig2 = plt.figure(2)
    plt.contourf(x,y,yy)
    plt.gca().set_aspect("equal")
    plt.colorbar()
    
    c1, cc, c2 = st.columns([5,1,5])  
    c1.write("$u_1(\\bm x)$")
    c2.write("$u_2(\\bm x)$")
    c1.pyplot(fig1)  
    c2.pyplot(fig2)  
