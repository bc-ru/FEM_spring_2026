import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Схема с весами", 
    "Оценка устойчивости", 
    "Условия устойчивости",
    "Общие условия устойчивости",
    )
)

if menu == "Схема с весами":
    r"""
##### Схема с весами

Равномерная сетка по переменной $t$ с шагом $\tau > 0$

$\begin{aligned} 
  \omega_{\tau} = \{ t_n = n \tau, \ n = 0,1,\dots \}
\end{aligned}$

$y^n - $ приближенное решение на момент времени $t = t_n$ 

Схема с весами

$\begin{aligned} 
  \frac{y^{n+1}-y^n}{\tau} + A (\sigma y^{n+1} + (1-\sigma)y^n) =
  \varphi^n ,
  \quad n = 0,1, \ldots
\end{aligned}$

$\begin{aligned} 
  y^0 = u^0 
\end{aligned}$

Выбор веса
* $\sigma = 0 - $  явная схема
* $\sigma = 1 - $  полностью неявная схема
* $\sigma = 1/2 - $  симметричная схема 
    """  
  
if menu == "Оценка устойчивости":
    r"""
##### Оценка устойчивости

Запишем схему в виде

$\begin{aligned} 
  \left ( I + \left ( \sigma - \frac{1}{2} \right ) \tau A  \right ) \frac{y^{n+1}-y^n}{\tau} + A \frac{y^{n+1}+y^n}{2} =
  \varphi^n 
\end{aligned}$

Домножим скалярно в $H$ на $v = (y^{n+1}+y^n)/2$ 

$\begin{aligned} 
 (B y^{n+1}, y^{n+1}) -  (B y^{n}, y^{n}) + (Av,v) = (\varphi^n , v)
\end{aligned}$

$\begin{aligned} 
 B = I + \left ( \sigma - \frac{1}{2} \right ) \tau A 
\end{aligned}$

При $B = B^* > 0$ 

$\begin{aligned} 
 \|y^{n+1}\|^2_B \leq \|y^{n}\|^2_B + \frac{\tau }{2\delta } \|\varphi^n\|^2 
\end{aligned}$

Априорная оценка

$\begin{aligned} 
  \|y^{n+1}\|^2_B \leq \|u^0\|^2_B + \frac{\tau }{2\delta } \sum_{k=0}^{n}\|\varphi^k\|^2 
\end{aligned}$
    """

if menu == "Условия устойчивости":
    r"""
##### Условия устойчивости

Оператор

$\begin{aligned} 
 B = B^* > 0 , 
 \quad B = I + \left ( \sigma - \frac{1}{2} \right ) \tau A 
\end{aligned}$

Безусловно устойчивые схемы

$\begin{aligned} 
 \sigma \geq \frac{1}{2} 
\end{aligned}$

$\begin{aligned} 
  \|y^{n+1}\|^2 \leq \|u^0\|^2 + \frac{\tau }{2\delta } \sum_{k=0}^{n}\|\varphi^k\|^2 
\end{aligned}$

Явная схема

$\begin{aligned} 
 B = I - \frac{\tau }{2} A > 0
\end{aligned}$

Условная устойчивость 

$\begin{aligned} 
 \tau < \frac{2}{\|A\|} ,
 \quad \|A\| = \mathcal{O}(h^{-2})  
\end{aligned}$

    """    
    
if menu == "Общие условия устойчивости":
    r"""
##### Общие условия устойчивости

Каноническая форма

$\begin{aligned} 
  B \frac{y^{n+1}-y^n}{\tau} + A y^n = 0
  \quad n = 0,1, \ldots
\end{aligned}$

$\begin{aligned} 
 y^0 = u^0
\end{aligned}$

Операторы

$\begin{aligned} 
 B = B^* > 0,
 \quad A = A^* > 0 
\end{aligned}$

Критерий устойчивости (А.А. Самарского) в $H_A, H_B$ 

$\begin{aligned} 
 B \geq \frac{\tau }{2} A
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
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
