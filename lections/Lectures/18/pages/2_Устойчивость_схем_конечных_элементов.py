import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Задача Коши", 
    "Аппроксимация по времени",    
    "Каноническая форма", 
    "Устойчивость по начальным данным",   
    "Условия устойчивости",      
    "Схема с весами",     
    )
)
  
if menu == "Задача Коши":
    r"""
##### Задача Коши

Параболическая задача

$\begin{aligned}
 \frac{\partial u}{\partial t} - \operatorname{div} (k(x) \operatorname{grad} u ) + d(x) u = f(x,t),
 \quad x \in \Omega, 
 \quad 0 < t \leq T  
\end{aligned}$

$\begin{aligned}
 u(x,t) = 0 , 
 \quad x \in \partial \Omega 
\end{aligned}$

$\begin{aligned}
 u(x,0) = u^0(x),
 \quad x \in \Omega  
\end{aligned}$


Для $u(t) \in V$

$\begin{aligned}
 \left( \frac{\partial u}{\partial t}, v \right ) + a(u,v) = (f, v), 
 \quad \forall  v \in V_0 ,
 \quad 0 < t \leq T 
\end{aligned}$

$\begin{aligned}
 (u(0),v) = (u^0, v), 
 \quad \forall  v \in V_0
\end{aligned}$

    """
    
if menu == "Аппроксимация по времени":
    r"""
##### Аппроксимация по времени

Схема с весами

$\begin{aligned} 
\left (\frac{y^{n+1} - y^{n}}{\tau},v \right ) + 
& a(\sigma y^{n+1} + (1-\sigma) y^n,v)=  
\big (f (\sigma t^{n+1} + (1-\sigma) t^n),v \big ) \\
& \forall v \in V_0, \quad n=0,1,\dots,N-1
\end{aligned}$

$\begin{aligned}
 (y^0,v) = (u^0, v), 
 \quad \forall  v \in V_0
\end{aligned}$

$\sigma - $ числовой параметр (вес)

* $\sigma = 0 - $ явная схема

* $\sigma = 1 - $ чисто неявная схема

* $\sigma = 0.5 - $ симметричная (Кранка-Николсон) схема
    """

if menu == "Каноническая форма":
    r"""
##### Каноническая форма

Двухслойная схема

$\begin{aligned} 
b_n\left (\frac{y^{n+1} - y^{n}}{\tau},v \right ) + 
& a_n(y^n,v) = (\chi^n, v) \\
& \forall v \in V_0, \quad n=0,1,\dots,N-1
\end{aligned}$

$\begin{aligned}
 (y^0,v) = (u^0, v), 
 \quad \forall  v \in V_0
\end{aligned}$

    """
    
if menu == "Устойчивость по начальным данным":
    r"""
##### Устойчивость по начальным данным

Схема с постоянными билинейными формами

$\begin{aligned} 
b\left (\frac{y^{n+1} - y^{n}}{\tau},v \right ) + 
& a(y^n,v) = 0 \\
& \forall v \in V_0, \quad n=0,1,\dots,N-1
\end{aligned}$

$\begin{aligned}
 (y^0,v) = (u^0, v), 
 \quad \forall  v \in V_0
\end{aligned}$

при $y^n \in V_0, \ n=0,1,\dots,N-1$

В гильбертовом пространстве $H_d$ 

$\begin{aligned}
(u,v)_d = d(u,v),
 \quad \|u\|_d = \big((u,u)_d \big )^{1/2} 
\end{aligned}$

для
 
$\begin{aligned}
d(u,v) = d(v,u) ,
 \quad d(u,u) \ge \delta \|u\|^2,
 \quad \delta > 0 
\end{aligned}$

Устойчивость в $H_d$ по начальным данным

$\begin{aligned}
 \|y^{n+1}\|_d \le \|y^{n}\|_d \le \dots \le \|y^{o}\|_d
\end{aligned}$

    """

if menu == "Условия устойчивости":
    r"""
##### Условия устойчивости

Двухслойная схема

$\begin{aligned} 
b\left (\frac{y^{n+1} - y^{n}}{\tau},v \right ) + 
& a(y^n,v) = 0 
\end{aligned}$

записывается в виде

$\begin{aligned} 
b \left(\frac{y^{n+1}-y^n}{\tau}, v \right ) - \frac{\tau }{2} a\left (\frac{y^{n+1}-y^n}{\tau}, v \right) +
\frac{1}{2} a(y^{n+1} +y^n, v) = 0.
\end{aligned}$

**Основной результатат**

Если билинейная форма $a(\cdot,\cdot)$ 
симметрична, положительно определена 

$\quad$ и выполнено неравенство

$\begin{aligned} 
b (v, v) \geq \frac{\tau }{2} a(v, v),
\quad \forall v \in V_0
\end{aligned}$

то имеет место априорная оценка

$\begin{aligned} 
a(y^{n+1},y^{n+1}) \leq a(y^n,y^n),	
\quad \forall v \in V_0 
\end{aligned}$

Априорная оценка устанавливается при выборе

$\begin{aligned} 
v =  y^{n+1} - y^{n}
\end{aligned}$

    """
if menu == "Схема с весами":
    r"""
##### Схема с весами

Двухслойная схема

$\begin{aligned} 
\left (\frac{y^{n+1} - y^{n}}{\tau},v \right ) + 
& a(\sigma y^{n+1} + (1-\sigma) y^n,v)= 0 
\end{aligned}$ 

записывается в канонической форме

$\begin{aligned} 
b\left (\frac{y^{n+1} - y^{n}}{\tau},v \right ) + 
& a(y^n,v) = 0 
\end{aligned}$

при 

$\begin{aligned} 
b(u,v) = (u,v) + \sigma \tau a(u,v)
\end{aligned}$

Условие устойчивости

$\begin{aligned} 
b (v, v) \geq \frac{\tau }{2} a(v, v),
\end{aligned}$

выполнено при $\sigma \ge 0.5$

    """

