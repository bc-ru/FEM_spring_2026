import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np 
import scipy.interpolate as interpolate 
 
menu = st.sidebar.radio('***',
    (
    "Ключевые элементы технологии", 
    "Аппроксимация расчетной области", 
    "Аппроксимация функций на ячейке",
    "Конечно-элементный базис",    
    "Задачи интерполяции",
    "Задачи приближения функций",    
    )
)
  
if menu == "Ключевые элементы технологии":
    r"""
##### Ключевые элементы технологии

* Аппроксимация расчетной области
* Аппроксимация функций на ячейке сетки
* Конечно-элементный базис (базисные функции)
* Задача (приближение функций)
* Приближенное решение (метод Галеркина)

    """  
       
if menu == "Аппроксимация расчетной области":
    r"""
##### Аппроксимация расчетной области

Разбиение расчетной области на ячейки

$\begin{aligned}
 \Omega = \bigcup_{\alpha=1}^{m} \Omega_\alpha  
\end{aligned}$

Приближение области

$\begin{aligned}
 \Omega \approx  \bigcup_{\alpha=1}^{m} \Omega_\alpha  
\end{aligned}$

1D

* Область: $\quad \Omega = \{ x \ | \ a \leq x \leq b \}$ 
* Сетка: $\quad x = \bar{x}_\alpha, \quad a =  \bar{x}_0 < \bar{x}_1 < \ldots <  \bar{x}_m = b $
* Ячейки: $\quad \Omega_\alpha = \{ x \ | \ \bar{x}_{\alpha -1} \leq x \leq \bar{x}_\alpha\}, \ \alpha = 1, 2, \ldots , m $ 

2D

* треугольники
* четырехугольники

    """ 
    
if menu == "Аппроксимация функций на ячейке":
    r"""
##### Аппроксимация функций на ячейке

**Аппроксимация полиномами малой степени**

1D

* Конечный элемент: $\\ \Omega_\alpha = \{ x \ | \ \bar{x}_{\alpha -1} \leq x \leq \bar{x}_\alpha\}, \ \alpha = 1, 2, \ldots , m$

* Линейная функция (полином первой степени): $\\ y(x) = a_0 + a_1 x$ - два узла аппроксимации

* Квадратичная функция (полином второй степени): $\\ y(x) = a_0 + a_1 x + a_2 x^2$ - три узла аппроксимации $\\$ (два на границах ячейки, один внутри)

2D  

* $\bm x = (x^{(1)}, x^{(2)})$ 
* Полином первой степени:  $\\ y(\bm x) = a_0 + a_1 x^{(1)} + a_2 x^{(2)}$ - три узла аппроксимации $\\$ (узлы треугольной ячейки)

    """  
    
if menu == "Конечно-элементный базис":
    r"""
##### Конечно-элементный базис

Линейно независимые базисные функции

$\varphi_k(x), \ k = 0,1, \ldots, n$  

Аппроксимирующая функция

$\begin{aligned}
 \varphi(\bm x) = \sum_{k=0}^{n} c_k \varphi_k(\bm x),
 \quad \bm x \in \Omega = \bigcup_{\alpha=1}^{m} \Omega_\alpha  
\end{aligned}$

Финитные базисные функции (носитель - часть ячеек)

$(\varphi_k, \varphi_l) \neq 0, \ k = 0, 1, \ldots, n$  для небольшого набора $\ l = 0, 1, \ldots, n$

Узлы аппроксимации

* точки $\bm x_i, \ i = 0,1, \ldots, n$ в области $\Omega$ и на ее границе 

* $\varphi_k(\bm x)$ сопоставляется с узлом аппроксимации $\bm x_k$

В узлах аппроксимации 

$\begin{aligned}
 \varphi_k(\bm x_i) = \begin{cases}
  1 ,  &  k = i \\
  0 ,  &  k \neq i \\
\end{cases}
\end{aligned}$

    """ 
    
if menu == "Задачи интерполяции":
    r"""
##### Задачи интерполяции

В узлах интерполирования $\bm x_i, \ i = 0,1, \ldots, n$
$\\ \quad$ заданы значения функции $f(\bm x_i), \ i = 0,1,\ldots,n$

Интерполирующая функция $\varphi(\bm x)$ 

$\begin{aligned}
  \varphi(\bm x_i) = f(\bm x_i),
  \quad i = 0,1,\ldots,n .
\end{aligned}$

**Решение**

Явное представление

$\begin{aligned}
\varphi(\bm x) = \sum_{k=0}^{n} f(\bm x_k) \varphi_k(\bm x),
\end{aligned}$

так как

$\begin{aligned}
 \varphi_k(\bm x_i) = \begin{cases}
  1 ,  &  k = i \\
  0 ,  &  k \neq i \\
\end{cases}
\end{aligned}$

    """
if menu == "Задачи приближения функций":
    r"""
##### Задачи приближения функций

Приближение на всей области $\Omega]$

$\begin{aligned}
 \varphi(\bm x) \approx f(\bm x),
 \quad  \bm x \in \Omega
\end{aligned}$

Аппроксимирующая функция 

$\begin{aligned}
   \varphi(\bm x) = \sum_{k=0}^{n} c_k \varphi_k(\bm x) 
\end{aligned}$

**Решение**

Метод Галеркина

$\begin{aligned}
  \sum_{k=0}^{n} c_k (\varphi_k,\varphi_l) = (f,\varphi_l),
  \quad l = 0,1,\ldots,n 
\end{aligned}$

Система уравнений с разреженной матрицей

$(\varphi_k, \varphi_l) \neq 0, \ k = 0, 1, \ldots, n$  для небольшого набора $\ l = 0, 1, \ldots, n$

    """
