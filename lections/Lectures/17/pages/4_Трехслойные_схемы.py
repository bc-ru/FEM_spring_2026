import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Общие условия устойчивости", 
    "Уравнение первого порядка", 
    "Уравнение второго порядка",     
    "Условия устойчивости",
    )
)

if menu == "Общие условия устойчивости":
    r"""
##### Общие условия устойчивости

Каноническая форма трехслойных схем

$\begin{aligned} 
  B \frac{y^{n+1}-y^{n-1}}{2 \tau} + R (y^{n+1}-2 y^n + y^{n-1}) + A y^n = 0
  \quad n = 1,2, \ldots
\end{aligned}$

$\begin{aligned} 
 y^0 = u^0,
 \quad y^1 = v^0
\end{aligned}$

$A, B, R - $ самосопряженные операторы

Условия устойчивости 

$\begin{aligned} 
 B \geq 0, 
 \quad  A > 0 , 
 \quad R \geq \frac{1 }{4} A
\end{aligned}$
    """  
  
if menu == "Уравнение первого порядка":
    r"""
##### Уравнение первого порядка

Задача Коши

$\begin{aligned} 
  \frac{dv}{dt}+Av=\varphi(t)
\end{aligned}$

$\begin{aligned} 
 v(0)=u^0
\end{aligned}$

Оператор

$\begin{aligned} 
A^*=A  \ge  \delta I,
 \quad \delta > 0
\end{aligned}$

Схема второго порядка точности

$\begin{aligned} 
  \frac{y^{n+1}-y^{n-1}}{2\tau} + A (\sigma y^{n+1} + (1-2\sigma)y^n + \sigma y^{n-1}) =
  \varphi^n ,
  \quad n = 1,2, \ldots
\end{aligned}$

$\begin{aligned} 
  y^0 = u^0 ,
  \quad  y^1 = v^0
\end{aligned}$

Начальное условие из

$\begin{aligned} 
  \frac{v^0-u^0}{\tau} + A \frac{v^0+u^0}{2} =
  \varphi^{1/2} 
\end{aligned}$

Безусловная устойчивость при 

$\begin{aligned} 
 \sigma \geq \frac{1}{4} 
\end{aligned}$
    """

if menu == "Уравнение второго порядка":
    r"""
##### Уравнение второго порядка

После аппроксимации задачи Коши для гиперболического  уравнения второго порядка

$\begin{aligned} 
  \frac{d^2v}{dt^2}+Av=0
\end{aligned}$

$\begin{aligned} 
  v(0)=u^0,
  \quad \frac{dv}{dt}(0) = u^1
\end{aligned}$

Разностная схема

$\begin{aligned} 
  \frac{y^{n+1}-2y^n + y^{n-1}}{\tau^2} + A (\sigma y^{n+1} + (1-2\sigma)y^n + \sigma y^{n-1}) = 0 ,
  \quad n = 1,2, \ldots
\end{aligned}$

$\begin{aligned} 
  y^0 = u^0 ,
  \quad  y^1 = v^0
\end{aligned}$

    """    
    
if menu == "Условия устойчивости":
    r"""
##### Условия устойчивости

В канонической форме

$\begin{aligned} 
  B = 0,
  \quad R = \frac{1}{\tau^2} I + \sigma A 
\end{aligned}$

Безусловно устойчивые схемы

$\begin{aligned} 
 \sigma \geq \frac{1}{4} 
\end{aligned}$

Условие устойчивости явной схемы

$\begin{aligned} 
 \tau \leq \frac{2}{\|A\|^{1/2}} , 
 \quad \tau \leq  \mathcal{O} (h)
\end{aligned}$

    """   
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
