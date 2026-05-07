import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Базовая задача", 
    "Уравнение второго порядка", 
    "Многомерные нестационарные задачи",
    )
)

if menu == "Базовая задача":
    r"""
##### Базовая задача

Одномерное параболическое уравнение второго
порядка

$\begin{aligned} 
  \frac{\partial u}{\partial t}=
  \frac\partial{\partial x}\left(k(x)\frac{\partial u}{\partial
  x}\right) + f(x,t) ,
  \quad 0 < x < l,
  \quad 0 < t \le T 
\end{aligned}$

Граничные условия

$\begin{aligned} 
  u(0,t)=0,
  \quad u(l,t)=0,
  \quad 0 < t \le T
\end{aligned}$

Начальное условие

$\begin{aligned} 
u(x,0)=u^0(x), \quad 0 \le x \le l
\end{aligned}$
    """  
  
if menu == "Уравнение второго порядка":
    r"""
##### Уравнение второго порядка

Гиперболическое уравнение 

$\begin{aligned} 
  \frac{\partial^2 u}{\partial t^2}=
  \frac\partial{\partial x}\left(k(x)\frac{\partial u}{\partial
  x}\right) + f(x,t) ,
  \quad 0 < x < l,
  \quad 0 < t \le T 
\end{aligned}$

Граничные условия

$\begin{aligned} 
  u(0,t)=0,
  \quad u(l,t)=0,
  \quad 0 < t \le T
\end{aligned}$

Два начальных условия

$\begin{aligned} 
  u(x,0)=u^0(x),
  \quad \frac{\partial u}{\partial t}(0,t) = v_0(x),
  \quad 0 \le x \le l 
\end{aligned}$

    """    
    
if menu == "Многомерные нестационарные задачи":
    r"""
##### Многомерные нестационарные задачи

Прямоугольник

$\begin{aligned} 
\Omega = \{ \bm x \ | \ \bm x  = (x_1,x_2), \ 0 < x_\alpha <
l_\alpha, \ \alpha = 1,2 \}
\end{aligned}$

Двумерное параболическое уравнение

$\begin{aligned} 
& \frac{\partial u}{\partial t} =
  \sum_{\alpha =1}^{2}
  \frac{\partial }{x_\alpha} \left ( k(\bm x)
  \frac{\partial u}{x_\alpha} \right ) - q(\bm x,t) u + f(\bm x,t) \\
 & \bm x \in \Omega ,
  \quad 0\le t\le T
\end{aligned}$

Граничные условия

$\begin{aligned} 
  u(\bm x,t) = 0,
  \quad \bm x \in \partial \Omega
\end{aligned}$

Начальное условие

$\begin{aligned} 
  u(\bm x,0)=u^0(\bm x),
  \quad \quad \bm x \in \Omega 
\end{aligned}$

    """  

