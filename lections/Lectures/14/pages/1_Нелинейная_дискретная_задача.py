import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Краевая задача", 
    "Конечно-элементное решение",    
    "Вариационная задача", 
    "Дискретная задача",    
    )
)
  
if menu == "Краевая задача":
    r"""
##### Краевая задача

**Уравнение**

$\begin{aligned} - 
 \operatorname{div} (k(u) \operatorname{grad} u ) = f(u,\bm x),
 \quad \bm x \in \Omega
\end{aligned}$

**Граничные условия**

$\begin{aligned}
  u(\bm x) = 0,
  \quad \bm x \in \partial\Omega
\end{aligned}$

**Нелинейность**

* коэффициент $k(u)$
* правая часть $f(u,\bm x)$

    """    
if menu == "Конечно-элементное решение":
    r"""
##### Конечно-элементное решение

Пространства

* конечно-элементное пространство $V$ (кусочно-гладкие фенкции)

* подпространство $V_0 = \{ v \ | \ v \in V, \ v(\bm x) = 0,
  \ \bm x \in \partial\Omega \}$ 

Базисные функции в $V_0$ 

$\varphi_i(\bm x) , \quad i = 1,2, \ldots, n$

$\begin{aligned}
 \varphi_i(\bm x_j) = \begin{cases}
  1 ,  &  i = j \\
  0 ,  &  i \neq j \\
\end{cases}
\end{aligned}$

Приближенное решение

$\begin{aligned}
   u(\bm x) \approx y(\bm x) = \sum_{i=1}^{n} y_i \varphi_i(\bm x) ,
   \quad y_i = y(\bm x_i),
   \quad i = 1,2, \ldots, n
\end{aligned}$

    """
    
if menu == "Вариационная задача":
    r"""
##### Вариационная задача

**Интегральное следствие**

$\begin{aligned}
 \int_{\Omega} k(y)  \operatorname{grad} y \operatorname{grad} v \, d x = 
 \int_{\Omega} f(y,\bm x) v(\bm x) \, d x
\end{aligned}$

для $y, v \in V_0$

**Вариационная постановка**

Найти  $y \in V_0$ такую, что

$\begin{aligned}
 (k(y)  \operatorname{grad} y,  \operatorname{grad} v) = 
 (f(y,\bm x), v) ,
 \quad \forall v \in V_0
\end{aligned}$

Скалярное произведение

$\begin{aligned}
 (y,v) = \int_{\Omega} y(\bm x) v(\bm x) \, d x
\end{aligned}$
    """
    
if menu == "Дискретная задача":
    r"""
##### Дискретная задача

Конечно-элементное решение

$\begin{aligned}
   y(\bm x) = \sum_{i=1}^{n} y_i \varphi_i(\bm x) ,
   \quad i = 1,2, \ldots, n
\end{aligned}$

Задача для коэффициентов

$\begin{aligned}
 & \Big (k \big (\sum_{j=1}^{n} y_j \varphi_j \big ) \sum_{j=1}^{n} y_j \operatorname{grad} \varphi_j  \operatorname{grad} \varphi_i \Big ) = 
 \Big (f \big (\sum_{j=1}^{n} y_j \varphi_j, \bm x \big ), \varphi_i \Big ) \\
& i = 1,2, \ldots, n
\end{aligned}$



Для вектора коэффициентов $y=\{y_i\}$

$\quad$ система нелинейных уравнений

$\begin{aligned}
 F(y) = 0 
\end{aligned}$

    """
    



























