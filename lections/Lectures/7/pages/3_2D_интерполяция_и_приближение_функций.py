import streamlit as st
import matplotlib.pyplot as plt
import numpy as np 
 
menu = st.sidebar.radio('***',
    (
    "Аппроксимируемая функция", 
    "2D интерполяция", 
    "2D приближение",     
    )
)
  
if menu == "Аппроксимируемая функция":
    r"""
##### Аппроксимируемая функция

Двумерная область

$\begin{aligned}
 \Omega = \{ \bm x \ | \ \bm x = (x^{(1)}, x^{(2)}),
  \quad -3 < x^{(1)} < 3, \quad -3 < x^{(2)} < 3 \}
\end{aligned}$

Функция 

$\begin{aligned}
f(x^{(1)},x^{(2)}) = \Big (1 - \big(x^{(1)}\big)^2 - \big(x^{(2)}\big)^3 \Big) 
\exp\Big(-\frac12\big(\big(x^{(1)}\big)^2 + \big(x^{(2)}\big)^2 \big )\Big) .
\end{aligned}$

График
    """ 
   
    def f(x,y):
        return (1-x**2-y**3)*np.exp(-(x**2+y**2)/2)
        
    N = 200
    x = np.linspace(-3,3,N)
    y = np.linspace(-3,3,N)
    yy  = np.zeros((N,N)) 
    
    for i in range(0, N): 
        for j in range(0, N): 
            yy[j,i]  = f(x[i], y[j])
              
    fig1 = plt.figure(1)
    plt.contourf(x,y,yy)
    plt.gca().set_aspect("equal")
    plt.colorbar()

    c1, c2, = st.columns([3,1]) 
    c1.pyplot(fig1)
    plt.clf()
    
if menu == "2D интерполяция":
    r"""
##### 2D интерполяция

**Задача интерполяции**

Узлы двумерной конечно-элемнентной интерполяции 

$ \bm x_i \in \Omega \cup \partial \Omega,
\quad i = 0,1, \ldots, n, \quad  \bm x = (x^{(1)}, x^{(2)}) $

Интерполирующая функция

$ \varphi(\bm x_i) = f(\bm x_i), \quad i = 0,1, \ldots, n $

**Конечно-элементная интерполяция (FEniCS)**

$~$
    """
    
    from fenics import *

    c1, cc, c2, = st.columns([5,1,5])    
    c1.write("$~~$")
    c1.write("Число разбиений по одному направлению")        
    m = c2.slider("m", 2, 20, 4)
    c1.write("$~~$")
    c1.write("Порядок полинома")        
    p = c2.slider("p", 1, 5, 2)  
    
    def f(x,y):
        return (1-(x**2+y**3))*np.exp(-(x**2+y**2)/2)
    
    p1 = Point(-3,-3)
    p2 = Point(3,3)
    
    mesh = RectangleMesh(p1, p2, m, m)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    V = FunctionSpace(mesh, "CG", p)
    n = V.dim()-1
     
    fr = Expression("(1-x[0]*x[0]-x[1]*x[1]*x[1])*exp(-0.5*(x[0]*x[0]+x[1]*x[1]))", degree=p+2)
    u = interpolate(fr, V)
    w = project(fr, V)
    
    N = 200
    x = np.linspace(-3,3,N)
    y = np.linspace(-3,3,N)
    yy  = np.zeros((N,N)) 
    ye  = np.zeros((N,N)) 
    tk = np.linspace(-3,3,m+1)
    
    for i in range(0, N): 
        for j in range(0, N): 
            pp = Point(x[i],y[j])
            yy[j,i] = u(pp)
            ye[j,i] = f(x[i], y[j])
            
    c1, cc, c2, = st.columns([5,1,5])          
    c1.write(r"""Решение $\quad \varphi(\bm x)$ """)
    c2.write(r"""Погрешность $\quad \varphi(\bm x) - f(\bm x)$ """)
              
    fig1 = plt.figure(1)
    ss = "$m = $" + str(m) + "$, p = $" + str(p)
    plt.title(ss)
    plt.contourf(x,y,yy)
    plt.gca().set_aspect("equal")
    plt.colorbar()
    plt.grid(True) 
    plt.xticks(ticks=tk)
    plt.yticks(ticks=tk)
    
    c1.pyplot(fig1)
    plt.clf()   
    
    fig2 = plt.figure(2)
    ss = "$m = $" + str(m) + "$, p = $" + str(p)
    plt.title(ss)
    plt.contourf(x,y,yy-ye)
    plt.gca().set_aspect("equal")
    plt.colorbar()
    plt.grid(True) 
    plt.xticks(ticks=tk)
    plt.yticks(ticks=tk)
    
    c2.pyplot(fig2)
    plt.clf()  
    
if menu == "2D приближение":
    r"""
##### 2D приближение

**Задача приближения**

В $L_2(\Omega)$

$\begin{aligned}
 (u,v) = \int_{\Omega} u(\bm x) v(\bm x) d x,
 \quad \|u\| = (u,u)^{1/2}
\end{aligned}$

$ \bm x = (x^{(1)}, x^{(2)}) $

Апроксимирующая функция

$\begin{aligned}
 \|\varphi - f\|^2 \rightarrow \min 
\end{aligned}$

**Конечно-элементное приближение (FEniCS)**

$~$
    """

    from fenics import *
    
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Число разбиений по одному направлению")        
    m = c2.slider("m", 2, 20, 4)
    c1.write("$~~$")
    c1.write("Порядок полинома")        
    p = c2.slider("p", 1, 5, 2)  
    
    def f(x,y):
        return (1-(x**2+y**3))*np.exp(-(x**2+y**2)/2)
    
    p1 = Point(-3,-3)
    p2 = Point(3,3)
    
    mesh = RectangleMesh(p1, p2, m, m)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    V = FunctionSpace(mesh, "CG", p)
    n = V.dim()-1
     
    fr = Expression("(1-x[0]*x[0]-x[1]*x[1]*x[1])*exp(-0.5*(x[0]*x[0]+x[1]*x[1]))", degree=p+2)
    u = interpolate(fr, V)
    w = project(fr, V)
    
    N = 200
    x = np.linspace(-3,3,N)
    y = np.linspace(-3,3,N)
    yy  = np.zeros((N,N)) 
    ye  = np.zeros((N,N)) 
    tk = np.linspace(-3,3,m+1)
    
    for i in range(0, N): 
        for j in range(0, N): 
            pp = Point(x[i],y[j])
            yy[j,i] = w(pp)
            ye[j,i] = f(x[i], y[j])
            
    c1, cc, c2, = st.columns([5,1,5])                          
    c1.write(r"""Решение $\quad \varphi(\bm x)$ """)
    c2.write(r"""Погрешность $\quad \varphi(\bm x) - f(\bm x)$ """)
                  
    fig1 = plt.figure(1)
    ss = "$m = $" + str(m) + "$,  p = $" + str(p)
    plt.title(ss)
    plt.contourf(x,y,yy) 
    plt.gca().set_aspect("equal")
    plt.colorbar()
    plt.grid(True) 
    plt.xticks(ticks=tk)
    plt.yticks(ticks=tk)
    
    c1.pyplot(fig1)
    plt.clf()   
    
    fig2 = plt.figure(2)
    ss = "$m = $" + str(m) + "$,  p = $" + str(p)
    plt.title(ss)
    plt.contourf(x,y,yy-ye) 
    plt.gca().set_aspect("equal")
    plt.colorbar()
    plt.grid(True) 
    plt.xticks(ticks=tk)
    plt.yticks(ticks=tk)
    
    c2.pyplot(fig2)
    plt.clf() 