import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np 
import scipy.interpolate as interpolate 
 
menu = st.sidebar.radio('***',
    (
    "Аппроксимация расчетной области", 
    "Линейные конечные элементы", 
    "Квадратичные конечные элементы",     
    "Конечно-элементный базис",
    )
)
  
if menu == "Аппроксимация расчетной области":
    r"""
##### Аппроксимация расчетной области

Двумерная область

$\bm x = (x^{(1)}, x^{(2)})$

$\begin{aligned}
 \Omega = \bigcup_{\alpha=1}^{m} \Omega_\alpha  
\end{aligned}$

Ячейки - треугольники (триангуляция)
    """ 
    
    c1, c2 = st.columns([1,1])
    c1.write("$~$")
    image = Image.open("pages/figs/1.png")    
    c1.image(image)   

if menu == "Линейные конечные элементы":
    r"""
##### Линейные конечные элементы

Кусочно линейная аппроксимация

$y(\bm x) = a_0 + a_1 x^{(1)} + a_2 x^{(2)}$ - три узла аппроксимации

Узлы аппроксимации $\bm x_{i}$ совпадают с узлами сетки $\bar{x}_{\alpha}$  

    """ 
    
    c1, c2 = st.columns([1,1])
    c1.write("$~$")
    image = Image.open("pages/figs/2.png")    
    c1.image(image)   
    
if menu == "Квадратичные конечные элементы":
    r"""
##### Квадратичные конечные элементы

**Аппроксимация полиномом второго порядка**

Шесть коэффициентов

$y(\bm x) = a_0 + a_1 x^{(1)} + a_2 x^{(2)} + a_3 x^{(1)} x^{(1)} + a_4 x^{(1)} x^{(2)} + a_5 x^{(2)} x^{(2)}$ 

Узлы аппроксимации
 
 * три узла сетки
 * три узла на серединах ребер ячейки

    """ 
    
    c1, c2 = st.columns([1,1])
    c1.write("$~$")
    image = Image.open("pages/figs/3.png")    
    c1.image(image)  
        
if menu == "Конечно-элементный базис":
    r"""
##### Конечно-элементный базис

Базисные функции

$\begin{aligned}
 \varphi_i(\bm x),
 \quad i = 1,2, \ldots, n 
\end{aligned}$

$\begin{aligned}
 \varphi_i(x_j) = \begin{cases}
  1 ,  &  i = j \\
  0 ,  &  i \neq j \\
\end{cases}
\end{aligned}$

**Визуализация (FEniCS)**
    """    
    import matplotlib.pyplot as plt
    import numpy as np 
    from fenics import *
    
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Число разбиений по одному направлению")        
    m = c2.slider("m", 2, 20, 3)
    c1.write("$~~$")
    c1.write("Порядок полинома")        
    p = c2.slider("p", 1, 5, 2)
    
    p1 = Point(0,0)
    p2 = Point(1,1)
    
    mesh = RectangleMesh(p1, p2, m, m)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    V = FunctionSpace(mesh, "CG", p)
    n = V.dim()-1

    c1.write("$~~$")
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
    ss = "$m = $" + str(m) + "$, \ p = $" + str(p)
    plt.title(ss)
    plt.contourf(x,y,yy,vv)
    plt.gca().set_aspect("equal")
    plt.grid(True) 
    plt.xticks(ticks=tk)
    plt.yticks(ticks=tk)
    
    c1, c2, = st.columns([3,1]) 
    c1.pyplot(fig1)


    
    

    
    
