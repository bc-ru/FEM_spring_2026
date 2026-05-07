import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Полудискретизация", 
    "Аппроксимация по пространству", 
    "Разностный оператор",
    "Задача для эволюционного уравнения",
    "Априорная оценка",
    )
)

if menu == "Полудискретизация":
    r"""
##### Полудискретизация

Дифференциальная задача

$\begin{aligned} 
  \frac{\partial u}{\partial t}=
  \frac\partial{\partial x}\left(k(x)\frac{\partial u}{\partial
  x}\right) + f(x,t) ,
  \quad 0 < x < l,
  \quad 0 < t \le T 
\end{aligned}$

$\begin{aligned} 
  u(0,t)=0,
  \quad u(l,t)=0,
  \quad 0 < t \le T
\end{aligned}$

$\begin{aligned} 
u(x,0)=u^0(x), \quad 0 \le x \le l
\end{aligned}$

Метод прямых

* сеточная аппроксимация по пространству
* задача Коши для дифференциально-разностного уравнения

    """  
  
if menu == "Аппроксимация по пространству":
    r"""
##### Аппроксимация по пространству

Равномерная сетка $\bar{\omega}_h = \omega_h \cup \partial\omega_h$

$\begin{aligned} 
   \bar{\omega}_h = \{x~ |~ x = x_i  = ih,
   \quad i = 0,1,\ldots,N,  \quad Nh = l\} 
\end{aligned}$

$\omega_h - $  множество внутренних узлов $(i=1,2,\ldots,N-1$)

$\partial\omega_h - $  множество граничных узлов

Сеточный оператор

$\begin{aligned} 
  A y = - (ay_{\overline{x}})_x,
  \quad x \in \omega_h
\end{aligned}$

для сеточных функций $y = 0, \ x \not\in \omega_h$

В индексных обозначениях

$\begin{aligned} 
(A y)_i = - \frac{1}{h} \Big (a_{i+1} \frac{y_{i+1} - y_i}{h}  - a_{i} \frac{y_{i} - y_{i-1}}{h} \Big ) , 
\quad x \in \omega_h 
\end{aligned}$

Коэффициенты 

$\begin{aligned} 
  & a_i=k(x_{i-1/2}),\quad x_{i-1/2}=x_i-\frac{h}2 \\
  & a_i=\frac12 (k(x_{i-1})+k(x_i))
\end{aligned}$
    """

if menu == "Разностный оператор":
    r"""
##### Разностный оператор

В $H = L_2(\omega_h)$ норма и скалярное произведение

$\begin{aligned} 
 (y,v)=\sum_{i=1}^{N-1}y_iv_ih,
 \quad \|y\|= (y,y)^{1/2} 
\end{aligned}$

Оператор $A$ 

$\begin{aligned} 
A^*=A>0 
\end{aligned}$

Оценки оператора $A$ снизу и сверху

$\begin{aligned} 
  \delta I \leq A \leq \Delta_h I
\end{aligned}$

с постоянными

$\begin{aligned} 
  & \delta = \frac{8}{l^2} \min_{0 \leq x \leq l} k(x) \\
  & \Delta_h = \frac{4}{h^2} \max_{0 \leq x \leq l} k(x)
\end{aligned}$

    """    
    
if menu == "Задача для эволюционного уравнения":
    r"""
##### Задача для эволюционного уравнения

После дискретизации по пространству

$\begin{aligned} 
  \frac{dv}{dt}+Av=\varphi(t)
\end{aligned}$

$\begin{aligned} 
  v(0)=u^0
\end{aligned}$

Оператор

$\begin{aligned} 
A^*=A \ge  \delta I
\end{aligned}$

    """  
    
if menu == "Априорная оценка":
    r"""
##### Априорная оценка

Домножим скалярно на $u(t)$ 

$\begin{aligned} 
 \left ( \frac{d u}{d t}, u \right ) + (Au,u) = (\varphi, u)  
\end{aligned}$

Имеем

$\begin{aligned} 
 \left ( \frac{d u}{d t}, u \right ) = \frac{1}{2} \frac{d}{d t} (u, u) = \frac{1}{2} \frac{d}{d t} \|u(t)\|^2
\end{aligned}$

$\begin{aligned} 
 (A u, u) \geq \delta \|u\|^2
\end{aligned}$

$\begin{aligned} 
 (\varphi, u) \leq \delta \|u\|^2 + \frac{1}{4 \delta } \|\varphi\|^2
\end{aligned}$

Получим

$\begin{aligned} 
 \frac{d}{d t} \|u(t)\|^2 \leq \frac{1}{2 \delta } \|\varphi\|^2
\end{aligned}$

$\begin{aligned} 
 \|u(t)\|^2 \leq \|u^0\|^2 + \frac{1}{2 \delta } \int_{0}^{t}\|\varphi(\theta)\|^2 d \theta 
\end{aligned}$

    """   
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
