import streamlit as st
from PIL import Image
 
menu = st.sidebar.radio('***',
    (
    "2D сетка", 
    "Функциональная трансформация",     
    "Примеры алгебраической трансформации",         
    "Краевая задача для узлов сетки", 
    "Блочные сетки",
    )
)
  
if menu == "2D сетка":
    r"""
##### 2D сетка
    """

    c1, c2, = st.columns(2)
    c1.write("""
**Индексное пространство**

$~$
    """)
     
    image = Image.open("pages/figs/6.png")
    c1.image(image)  
    
    c2.write("""
$~~~~~~~~~~$ **Прямоугольная сетка**
    """)
    image = Image.open("pages/figs/gr1.png")
    c2.image(image)  
 
if menu == "Функциональная трансформация":
    r"""
##### Функциональная трансформация
    """
    c1, c2, = st.columns(2)
    c1.write(r"""
**Исходная сетка**

$x_1 = \theta_1, \quad x_2 = \theta_2$

$\theta = (\theta_1,\theta_2)$

$\theta_1 \in [0,1], \quad \theta_2 \in [0,1]$
    """)
 
    image = Image.open("pages/figs/gr1.png")
    c1.image(image) 

    c2.write(r"""
**Трансформированная сетка**

$x = (x_1, x_2)$

$x_1 = x_1(\theta_1,\theta_2), \quad x_2 = x_2(\theta_1,\theta_2)$

На рисунке: $\quad x_1 = 2 \theta_1^2, \quad x_2 = \theta_2$
    """)
    
    image = Image.open("pages/figs/gr2.png")
    c2.image(image) 
      
    
if menu == "Примеры алгебраической трансформации":
    r"""
##### Примеры алгебраической трансформации
    """
    
    c1, c2, = st.columns(2)
    c1.write(r"""
**Четверть кольца**

В цилиндрических координатах

$\varrho = 1 + \theta_1 \in [1,2]$

$\varphi = 0.5 \theta_2 \in [0,0.5 \pi]$

$x_1 = \varrho \cos(\varphi), \quad x_2 = \varrho \sin(\varphi)$


    """)
   
    image = Image.open("pages/figs/gr3.png")
    c1.image(image) 

    c2.write(r"""    
**Трансформация по одному направлению**

Криволинейная верхняя граница

$x_2 = 1 - 0.5 \cos(0.5 \pi x_1), \quad x_1 \in [0,2]$

$x_1 = 2 \theta_1$  
 
$x_2 =  1 - 0.5 \cos(\pi \theta_1)$


    """)

    image = Image.open("pages/figs/gr4.png")
    c2.image(image) 
    
                    
if menu == "Краевая задача для узлов сетки":
    r"""
##### Краевая задача для узлов сетки
**Трансформация**

$x_1 = x_1(\theta_1,\theta_2), \quad x_2 = x_2(\theta_1,\theta_2)$

$\theta_1 \in [0,1], \quad \theta_2 \in [0,1]$

$~$
    """
    st.write("")      
    image = Image.open("pages/figs/7.png")
    st.image(image)
    
    r"""    
**Границы**

$\Gamma_1: \quad \theta_1 = 0$

$\Gamma_2: \quad \theta_2 = 1$ 

$\Gamma_3: \quad \theta_1 = 1$

$\Gamma_4: \quad \theta_2 = 0$  

**Система уравнений**

$\begin{aligned}
\frac{\partial^2 x_1}{\partial \theta_1^2} + \frac{\partial^2 x_1}{\partial \theta_2^2} = 0
\end{aligned}$

$\begin{aligned}
\frac{\partial^2 x_2}{\partial \theta_1^2} + \frac{\partial^2 x_2}{\partial \theta_2^2} = 0
\end{aligned}$

**Краевые условия**

Заданная параметризация на $\Gamma_1, \Gamma_2, \Gamma_3, \Gamma_4$

Условия Дирихле
    """
    
if menu == "Блочные сетки":

    r"""
##### Блочные сетки
**Расчетная область**
    """
    
    st.write("")      
    image = Image.open("pages/figs/8.png")
    st.image(image)
    
    r"""
$~$

**Блочная структурированная сетка**

В каждой подобласти $\Omega_1, \Omega_2$ строится своя структурированная сетка

Проблема: качество сеток на интерфейсной границе $\gamma = \Omega_1 \cup \Omega_2$  
    """

    
    
