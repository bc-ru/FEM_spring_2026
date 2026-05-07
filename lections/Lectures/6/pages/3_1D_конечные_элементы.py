import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np 
import scipy.interpolate as interpolate 
 
menu = st.sidebar.radio('***',
    (
    "Аппроксимация расчетной области", 
    "Аппроксимация функций на ячейке",
    "Конечно-элементный базис",    
    "Кусочно-квадратичные элементы",
    "Базисные функции",
    )
)
  
if menu == "Аппроксимация расчетной области":
    r"""
##### Аппроксимация расчетной области

Расчетная область $\Omega = [a,b]$ 

Сетка $\overline{\omega}$  

$\begin{aligned}
   \overline{\omega} = \{x~ |~ x = \bar{x}_\alpha , \ \alpha  = 0,1,\ldots,m, \ a = \bar{x}_0  < \bar{x}_1 < \cdots < \bar{x}_m = b \}
\end{aligned}$

* $\omega$ - множество внутренних узлов ($\bar{x}_\alpha, \ \alpha  = 1,2,\ldots,m-1$) 
* $\partial\omega$ - множество граничных узлов ($\bar{x}_0, \bar{x}_m$)

Ячейки

$\begin{aligned}
 \Omega = \bigcup_{\alpha=1}^{m} \Omega_\alpha  
\end{aligned}$
 
$\begin{aligned}
 \Omega_\alpha = \{ x \ | \ \bar{x}_{\alpha -1} \leq x \leq \bar{x}_\alpha\}, \ \alpha = 1, 2, \ldots , m 
\end{aligned}$

    """  
       
if menu == "Аппроксимация функций на ячейке":
    r"""
##### Аппроксимация функций на ячейке

Линейная функция (полином первой степени): 
$\\ \quad y(x) = a_0 + a_1 x$ - два узла аппроксимации

Узлы аппроксимации $x_{i-1} = \bar{x}_{\alpha -1}, \ x_i = \bar{x}_\alpha$  на элементе

$\begin{aligned}
 \Omega_\alpha = \{ x \ | \ \bar{x}_{\alpha -1} \leq x \leq \bar{x}_\alpha\} 
\end{aligned}$

    """

    c1, c2 = st.columns([2,1])
    c1.write("$~$")
    image = Image.open("pages/figs/1.png")    
    c1.image(image)   
       
if menu == "Конечно-элементный базис":
    r"""
##### Конечно-элементный базис

Кусочно-линейные базисные функции

$\begin{aligned}
 \varphi_i(x),
 \quad i = 0,1, \ldots, n 
\end{aligned}$

$\begin{aligned}
 \varphi_i(x_j) = \begin{cases}
  1 ,  &  i = j \\
  0 ,  &  i \neq j \\
\end{cases}
\end{aligned}$

    """

    c1, c2 = st.columns([2,1])
    c1.write("Внутренние узлы")
    image = Image.open("pages/figs/2.png")    
    c1.image(image)  
    c1.write("Граничные узлы")
    image = Image.open("pages/figs/3.png")    
    c1.image(image)      
    
       
if menu == "Кусочно-квадратичные элементы":
    r"""
##### Кусочно-квадратичные элементы

Квадратичная функция (полином второй степени): 

$y(x) = a_0 + a_1 x + a_2 x^2$  - три узла аппроксимации

На ячейке 

$\begin{aligned}
 \Omega_\alpha = \{ x \ | \ \bar{x}_{\alpha -1} \leq x \leq \bar{x}_\alpha\} 
\end{aligned}$

узлы аппроксимации 

$\begin{aligned}
 x_{i-1} = \bar{x}_{\alpha -1}, 
 \quad x_{i} = \frac 12 (\bar{x}_{\alpha -1} +  \bar{x}_\alpha), 
 \quad x_{i+1} = \bar{x}_\alpha
\end{aligned}$

    """

    c1, c2 = st.columns([2,1])
    c1.write("$~$")
    image = Image.open("pages/figs/4.png")    
    c1.image(image)  
    
if menu == "Базисные функции":
    r"""
##### Базисные функции

    """

    c1, c2 = st.columns([2,1])
    c1.write("Внутренние узлы")
    image = Image.open("pages/figs/5.png")    
    c1.image(image)  
    c1.write("Граничные узлы")
    image = Image.open("pages/figs/6.png")    
    c1.image(image)   
