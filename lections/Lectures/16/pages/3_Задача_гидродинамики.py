import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Ползущие течения", 
    "Интегральное тождество",
    "Конечно-элементная аппроксимация", 
    )
)

if menu == "Ползущие течения":
    r"""
##### Ползущие течения

**Приближение**

* несжимаемая жидкость
* вязкая жидкость
* без учета конвективного переноса
* стационарные течения

**Уравнения Стокса**

Уравнение неразрывности

$\begin{aligned}
  \operatorname{div} \bm u = 0
\end{aligned}$

Уравнение движения

$\begin{aligned} -
  \mu \operatorname{div} \operatorname{grad} \bm u + \operatorname{grad} p = 0
\end{aligned}$

В ограниченной области $\Omega$

* $\bm u - $ скорость
* $p - $ давление
* $\mu - $ вязкость

**Граничные условия**

$\begin{aligned}
  \bm u (\bm x) = \bm g (\bm x),
  \quad \bm x \in \partial \Omega
\end{aligned}$

    """
if menu == "Интегральное тождество":
    r"""
##### Интегральное тождество

**Пространства**

Для скорости

* $\bm V$ - пространство достаточно гладких векторных функций
* подпространство $\bm V_D = \{ \bm v \ | \ \bm v \in \bm V, \quad \bm v(\bm x) = \bm g(\bm x),
  \quad \bm x \in \partial \Omega \}$ 
* подпространство $\bm V_0 = \{ \bm v \ | \ \bm v \in \bm V, \quad \bm v(\bm x) = 0,
  \quad \bm x \in \partial \Omega \}$  
  
Для давлений

* $V$ - пространство достаточно гладких скалярных функций
    
**Система уравнений**

$\begin{aligned}
& - \mu \operatorname{div} \operatorname{grad} \bm u + \operatorname{grad} p = 0 \\
&  \operatorname{div} \bm u = 0,
\quad \bm x \in \Omega
\end{aligned}$

Домножим скалярно в $L_2(\Omega)$ первое уравнение на $\bm v (\bm x) \in \bm V_0$, 

$\quad$ второе - на $q(\bm x) \in V$

Получим

$\begin{aligned}
& \int_{\Omega} \mu \operatorname{grad} \bm u \operatorname{grad} \bm v \, d x - \int_{\Omega}  p \operatorname{div} \bm v \, dx = 0 \\
& \int_{\Omega} \operatorname{div} \bm u \, q \, d x = 0 
\end{aligned}$

для

$\begin{aligned} 
 \bm u (\bm x) \in \bm V_D, 
 \quad \bm v (\bm x) \in \bm V_0, 
  \quad p(\bm x), \, q(\bm x) \in V  
\end{aligned}$

    """   
    
if menu == "Конечно-элементная аппроксимация":
    r"""
##### Конечно-элементная аппроксимация

Для скалярных и векторных величин свои аппроксимации в $\Omega$ 

$\quad$ (сетка, конечные элементы)  

Базис (пробные функции) для давления

$\varphi^p_{i_p}(\bm x) , \quad i_p = 1,2, \ldots, n_p$

Базис для скорости (векторные конечные элементы)

$\bm \varphi^u_{i_u}(\bm x) , \quad i_u = 1,2, \ldots, n_u$

Приближенное решение

$\begin{aligned}
 &  p (\bm x) \approx s (\bm x) = \sum_{i_p=1}^{n_p} s_{i_p} \varphi_{i_p}^p(\bm x)  \\
 &  \bm u(\bm x) \approx \bm y(\bm x) = \sum_{i_u=1}^{n_u} y_{i_u} \bm \varphi_{i_u}^u(\bm x) 
\end{aligned}$

    """   
