import streamlit as st
from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt
 
menu = st.sidebar.radio('***',
    (
    "Непрерывные и разрывные элементы", 
    "Разрывные квадратичные элементы", 
    "FEniCS: лагранжевые конечные элементы",
    "1D базисные функции",
    "2D базисные функции",
    "1D задачи интерполяции и приближения",           
    )
)
  
if menu == "Непрерывные и разрывные элементы":
    r"""
##### Непрерывные и разрывные элементы

**Непрерывные лагранжевые элементы**

* узлы аппроксимации на гранях ячейки являются общими
* непрерывность аппроксимирующей функции на гранях ячейки

**Разрывные лагранжевые элементы**

* узлы аппроксимации относятся только к одной ячейке
* разрывность аппроксимирующей функции на гранях ячейки

    """    
    
if menu == "Разрывные квадратичные элементы":
    r"""
##### Разрывные квадратичные элементы

$~$
    """

    c1,c2 = st.columns([4,2])
    image = Image.open("pages/figs/6.png")
    c1.image(image) 
    
if menu == "FEniCS: лагранжевые конечные элементы":
    r"""
##### FEniCS: лагранжевые конечные элементы

$p$ - степень полинома

**Непрерывные лагранжевые элементы**

    """

    c1,cc1,c2,cc2,c3,cc3 = st.columns([2,1,2,1,2,1])
    
    c1.write(r""" $p = 1$""")
    c2.write(r""" $p = 2$""")    
    c3.write(r""" $p = 3$""")       
    image = Image.open("pages/figs/7.png")
    c1.image(image)  
    image = Image.open("pages/figs/8.png")
    c2.image(image)  
    image = Image.open("pages/figs/9.png")
    c3.image(image)      

    r""" 
 $~$
 
**Разрывные лагранжевые элементы**

    """

    c1,cc1,c2,cc2,c3,cc3 = st.columns([2,1,2,1,2,1])
    
    c1.write(r""" $p = 0$""")
    c2.write(r""" $p = 1$""")    
    c3.write(r""" $p = 2$""")       
    image = Image.open("pages/figs/10.png")
    c1.image(image)  
    image = Image.open("pages/figs/11.png")
    c2.image(image)  
    image = Image.open("pages/figs/12.png")
    c3.image(image) 
    
if menu == "1D базисные функции":
    r"""
##### 1D базисные функции

$~$
    """   
    fem = st.selectbox(
    "Тип конечных элементов",
    ("непрерывные", "разрывные"))
    if fem == "разрывные":
        sfem = "DG"
    else:
        sfem = "CG"
        
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Число ячеек")        
    m = c2.slider("m", 2, 20, 5)
    c1.write("$~~$")
    c1.write("Порядок полинома")  
    
    if fem == "разрывные":                
        p = c2.slider("p", 0, 5, 0)   
    else:
        p = c2.slider("p", 1, 5, 1)   
        
    from fenics import *
    
    a = 0.
    b = 1.
    
    mesh = IntervalMesh(m, a, b)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    V = FunctionSpace(mesh, sfem, p)
    n = V.dim()-1
    
    c1.write("Базисная функция")
    k = c2.slider("k", 0, n, 0)  
    
    u = Function(V)
    u.vector()[k] = 1
    
    xn = V.tabulate_dof_coordinates()
    yn = np.zeros((len(xn)), "float")   
    
    N = 500
    xx = np.linspace(a, b, N) 
    yy = np.linspace(a, b, N)  
    
    for i in range(0, N): 
        yy[i]  = u(Point(xx[i]))
              
    fig1 = plt.figure(1)
    ss = sfem + ": $m = $" + str(m) + "$,  p = $" + str(p)
    plt.title(ss)
    
    plt.scatter(xn, yn)  
    plt.scatter(xm, ym)  
    plt.plot(xx, yy)  
        
    plt.xlabel('$x$') 
    plt.grid(True) 
    
    c1, c2, = st.columns([3,1]) 
    c1.pyplot(fig1)
    plt.clf()          
    
if menu == "2D базисные функции":
    r"""
##### 2D базисные функции

$~$
    """   
    fem = st.selectbox(
    "Тип конечных элементов",
    ("непрерывные", "разрывные"))
    if fem == "разрывные":
        sfem = "DG"
    else:
        sfem = "CG"
        
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Число ячеек")        
    m = c2.slider("m", 2, 10, 3)
    c1.write("$~~$")
    c1.write("Порядок полинома")  
    
    if fem == "разрывные":                
        p = c2.slider("p", 0, 5, 0)   
    else:
        p = c2.slider("p", 1, 5, 1)   
        
    from fenics import *
    
    p1 = Point(0,0)
    p2 = Point(1,1)
    
    mesh = RectangleMesh(p1, p2, m, m)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    V = FunctionSpace(mesh, sfem, p)
    n = V.dim()-1
    
    c1.write("Базисная функция")
    k = c2.slider("k", 0, n, 0) 
    
    u = Function(V)
    u.vector()[k] = 1
    plot(u)
    
    N = 200
    x = np.linspace(0,1,N)
    y = np.linspace(0,1,N)
    yy  = np.zeros((N,N)) 
    vv = np.linspace(-1,1,21)
    tk = np.linspace(0,1,m+1)
    
    for i in range(0, N): 
        for j in range(0, N): 
            pp = Point(x[i],y[j])
            yy[j,i]  = u(pp)
              
    fig1 = plt.figure(1)
    ss = "$m = $" + str(m) + "$,  p = $" + str(p)
    plt.title(ss)
    plt.contourf(x,y,yy,vv)
    plt.gca().set_aspect("equal")
    plt.grid(True) 
    plt.xticks(ticks=tk)
    plt.yticks(ticks=tk)
    
    c1, c2, = st.columns([3,1]) 
    c1.pyplot(fig1)
    plt.clf()    
 
if menu == "1D задачи интерполяции и приближения":
    r"""
##### 1D задачи интерполяции и приближения

**Постановка задачи**

Выполнить интерполяцию и приближение функции Рунге

$\begin{aligned}
 f(x) = \frac{1}{1 + 25 x^2}
\end{aligned}$

на интервале $[-1,1]$ при использовании непрерывных и разрывных лагранжевых конечных элементов

**Решение (FEniCS)**

$~$
    """   
    c1, cc, c2 = st.columns([5,1,5])
    
    spr = c1.selectbox(
    "Задача", ("интерполяции", "приближения"))
        
    fem = c2.selectbox(
    "Тип конечных элементов",
    ("непрерывные", "разрывные"))
    if fem == "разрывные":
        sfem = "DG"
    else:
        sfem = "CG"
               
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Число ячеек")        
    m = c2.slider("m", 2, 10, 3)
    c1.write("$~~$")
    c1.write("Порядок полинома")  
    
    if fem == "разрывные":                
        p = c2.slider("p", 0, 5, 0)   
    else:
        p = c2.slider("p", 1, 5, 1) 
        
    from fenics import *
    
    a = -1.
    b = 1.
        
    def f(x):
        return 1./(1.+25*x**2)  
    
    mesh = IntervalMesh(m, a, b)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    V = FunctionSpace(mesh, sfem, p)
    n = V.dim()-1
    
    fr = Expression("1/(1+25*x[0]*x[0])", degree=p+2)
    if spr == "интерполяции":
        u = interpolate(fr, V)
    else:
        u = project(fr, V)
    
    N = 500
    xx = np.linspace(a, b, N) 
    yy = np.linspace(a, b, N)  
    ye = f(xx)
    
    xn = V.tabulate_dof_coordinates()
    yn = np.zeros((len(xn)), "float")   
    
    for i in range(0, N): 
        yy[i]  = u(Point(xx[i]))
              
    fig1 = plt.figure(1)
    ss = "$m = $" + str(m) + "$,  p = $" + str(p)
    plt.title(ss)
    plt.scatter(xn, yn)  
    plt.scatter(xm, ym)  
    plt.plot(xx, ye)  
    plt.plot(xx, yy)  
        
    plt.xlabel('$x$') 
    plt.grid(True)   
           
    c1, c2, = st.columns([3,1]) 
    c1.pyplot(fig1)
    plt.clf()     
    
    
    
    