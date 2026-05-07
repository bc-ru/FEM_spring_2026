import streamlit as st
from PIL import Image
 
menu = st.sidebar.radio('***',
    (
    "Задачи интерполяции", 
    "Полиномиальная  интерполяция", 
    "Экстраполяция, сглаживание",
    "Приближение функций",
    "Нелинейная аппроксимация",    
    )
)
  
if menu == "Задачи интерполяции":
    r"""
##### Задачи интерполяции


На отрезке $[a,b]$  в узлах интерполирования $x_0 < x_1 < \ldots < x_n$
$\\ \quad$ заданы значения функции $f(x_i), \ i = 0,1,\ldots,n$

Проблема: найти значения функции $f(x)$ в точках $x \ne x_i, \ i = 0,1,\ldots,n$

На отрезке
$[a,b]$  задана система функций
$\{\varphi_k(x)\}_{k=0}^{n}$ 

Определим интерполирующую функцию

$\begin{aligned}
  \varphi(x) = \sum_{k=0}^{n} c_k \varphi_k(x)
\end{aligned}$

$\\ \quad$ с действительными коэффициентами $c_k, \ k = 0,1,\ldots,n$

При интерполировании функции $f(x)$ для нахождения коэффициентов
условия

$\begin{aligned}
  \varphi(x_i) = f(x_i),
  \quad i = 0,1,\ldots,n .
\end{aligned}$

    """    
    
if menu == "Полиномиальная  интерполяция":
    r"""
##### Полиномиальная  интерполяция

Базисные функции

$\begin{aligned}
 \varphi_k(x) = x^k,
 \quad k = 0,1,\ldots,n
\end{aligned}$

**Интерполяция сплайнами**

Функция $f(x)$ приближается многочленами невысокой степени 
на частичных отрезках 
$\\$ (кусочно-полиномиальная  интерполяция)

$\begin{aligned}
[x_i,x_{i+1}], \quad i=0,1,\ldots,n-1
\end{aligned}$

    """
    
if menu == "Экстраполяция, сглаживание":

    r"""
##### Экстраполяция, сглаживание

Экстраполяция

$\begin{aligned}
  x_0 > a, 
 \quad x_n < b
\end{aligned}$

Сглаживание

$\begin{aligned}
  \varphi(x) = \sum_{k=0}^{m} c_k \varphi_k(x)
\end{aligned}$

$\quad$ при $m < n$: $\quad \varphi(x_i) \approx f(x_i), \ i = 0, 1, \ldots, n$

   """
    
if menu == "Приближение функций":
    r"""
##### Приближение функций

Построения функции $\varphi(x)$ 
$\\ \quad$ приближающую заданную функцию $f(x)$ на отрезке $[a,b]$ 

$\begin{aligned}
 \varphi(x) \approx f(x),
 \quad a \leq x \leq b 
\end{aligned}$

Проблема: коэффициенты $c_k, \ k = 0, 1, \ldots, n$ аппроксимирующей функции $\varphi(x)$

В линейном нормированном пространстве
$\\ \quad$ из условия минимальности нормы погрешности аппроксимации

$\begin{aligned}
  \|f(x) - \sum_{k=0}^{n} c_k \varphi_k(x)\| 
\end{aligned}$

Примеры

* пространство $L_\infty (a,b)$: $\quad {\displaystyle \| \varphi(x) \| = \max_{a \leq x \leq b} |\varphi(x)|}$   

* пространство $L_2(a,b)$: $\quad {\displaystyle \| \varphi(x) \| = \Big (\int_{a}^{b} \varphi^2(x) \, d x \Big )^{1/2}} $ 

    """
    
if menu == "Нелинейная аппроксимация":
    r"""
##### Нелинейная аппроксимация

Аппроксимирующая функция 

$\begin{aligned}
   \varphi(x) = \sum_{k=0}^{n} c_k \varphi_k(x) ,
  \quad \varphi_k(x) = \psi(x, d_k),
  \quad k = 0,1,\ldots,n
\end{aligned}$

Найти $c_k, d_k, \ k = 0,1,\ldots,n$

Пример 1: $\quad$ рациональная аппроксимация

$\begin{aligned}
 \psi(x, d_k) = \frac{1}{x + d_k} 
  \quad k = 0,1,\ldots,n
\end{aligned}$

Пример 2: $\quad$ аппроксимация суммой экспонент

$\begin{aligned}
 \psi(x, d_k) = \exp(- d_k x) 
  \quad k = 0,1,\ldots,n
\end{aligned}$

    """    
    
    
    
