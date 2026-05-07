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

**Система уравнений**

$\begin{aligned} -
 & \operatorname{div} \operatorname{grad} u_1  + r (u_1-u_2) = f_1(\bm x)  \\ -
 & \varkappa \operatorname{div} \operatorname{grad} u_2 - r (u_1-u_2) = f_2(\bm x) 
\end{aligned}$

с постоянными коэффициентами $\varkappa >  0, \ r$

**Части границы**

* $\partial D_1 = \{ \bm x \ | \ \bm x \in \partial \Omega, \ (x_1 = 0, \ x_2 < 0.5 ) , \ x_1 = 1  \}$
* $\partial N_2 =  \partial \Omega $

**Граничные условия**

$\begin{aligned}
  u_1(\bm x) = x_1, 
  \quad \bm x \in \partial D_1, 
  \quad \frac{\partial u_1}{\partial n} = 0,
  \quad \bm x \in \partial N_1
\end{aligned}$

$\begin{aligned}
  \frac{\partial u_2}{\partial n} = 0,
  \quad \bm x \in \partial \Omega
\end{aligned}$

    """     
if menu == "Ключевые фрагменты кода (FEniCS)":

    r"""
##### Ключевые фрагменты кода (FEniCS)

**Конечно-элементное пространство**
    """    
    code = """  
V1 = FiniteElement("CG", mesh.ufl_cell(), p)
V2 = FiniteElement("CG", mesh.ufl_cell(), p)
V = FunctionSpace(mesh, V1*V2)

u = TrialFunction(V)
v = TestFunction(V)
    """ 
    st.code(code, language="python")  
 
    r"""        
**Граничные условия Дирихле**
    """    
    code = """  
def left(x, on_boundary):
    return near(x[0], 0) and x[1] < 0.5 and on_boundary
def right(x, on_boundary):
    return near(x[0], 1) and on_boundary

bc1 = DirichletBC(V.sub(0), Constant(0.), left)
bc2 = DirichletBC(V.sub(0), Constant(1.), right)
bcs = [bc1, bc2]
    """ 
    st.code(code, language="python")   
    r"""    
**Вариационная формулировка задачи**
    """    
    code = """  
F = dot(grad(u[0]), grad(v[0]))*dx + rr*(u[0]-u[1])*v[0]*dx 
  + kap*dot(grad(u[1]), grad(v[1]))*dx - rr*(u[0]-u[1])*v[1]*dx 
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
(u1, u2) = w.split(True) 
    """ 
    st.code(code, language="python")       
         
                   
if menu == "Параметрические расчеты":
    r"""
##### Параметрические расчеты

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
    p = c2.slider("", 1, 3, 1)  
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write(r"""Коэффициент $\varkappa$""")        
    kap = c2.slider("", 0.01, 0.2, 0.1, 0.01)
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Коэффициент $r$")        
    rr = c2.slider("", 0.01, 0.5, 0.25, 0.01)

    mesh = UnitSquareMesh(m, m)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    V1 = FiniteElement("CG", mesh.ufl_cell(), p)
    V2 = FiniteElement("CG", mesh.ufl_cell(), p)
    V = FunctionSpace(mesh, V1*V2)
    
    u = TrialFunction(V)
    v = TestFunction(V)
    
    def left(x, on_boundary):
        return near(x[0], 0) and x[1] < 0.5 and on_boundary
    def right(x, on_boundary):
        return near(x[0], 1) and on_boundary
    
    bc1 = DirichletBC(V.sub(0), Constant(0.), left)
    bc2 = DirichletBC(V.sub(0), Constant(1.), right)
    bcs = [bc1, bc2]
    
    F = dot(grad(u[0]), grad(v[0]))*dx + rr*(u[0]-u[1])*v[0]*dx \
      + kap*dot(grad(u[1]), grad(v[1]))*dx - rr*(u[0]-u[1])*v[1]*dx 
    a = lhs(F)
    L = rhs(F)
    
    w = Function(V)
    solve(a == L, w, bcs)
    (u1, u2) = w.split(True)
    
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
    plt.contourf(x,y,yy, levels=np.linspace(0,1, 11))
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
