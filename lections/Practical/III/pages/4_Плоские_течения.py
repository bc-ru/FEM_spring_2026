import streamlit as st

menu = st.sidebar.radio('***',
    (
    "Функция тока",    
    "Вихрь скорости",  
    "Система уравнений",
    "Идеальная жидкость",       
    )
)
if menu == "Функция тока":

    r"""
    ##### Функция тока
    
    Скорость
    
    $\begin{aligned}
    \bm{v}(\bm x, t) = \{v_1, v_2, 0\},
    \end{aligned}$ 
    
    Условие неразрывности
    
    $\begin{aligned}
    \frac{\partial v_1}{\partial x_1} +  \frac{\partial v_2}{\partial x_2} = 0
    \end{aligned}$    
    
    будет выполнено при
    
    $\begin{aligned}
    v_1 = \frac{\partial \psi}{\partial x_2} ,
    \quad v_2 = - \frac{\partial \psi}{\partial x_1}
    \end{aligned}$    
    
    Линии $\psi = \operatorname{const} - $ линии тока 
    
    """   
    
if menu == "Вихрь скорости":

    r"""
    ##### Вихрь скорости
    
    Плоские течения
    
    $\begin{aligned}
    \nabla \times \bm{v}= \{0, 0, \omega\},
    \quad \omega = \frac{\partial v_2}{\partial x_1} - \frac{\partial v_1}{\partial x_2}
    \end{aligned}$   
    
    Расчет через функцию тока
    
    $\begin{aligned}
    \omega = - \nabla^2 \psi
    \end{aligned}$      
    
    """
    
if menu == "Система уравнений":

    r"""
    ##### Система уравнений 
    
    Уравнение для вихря скорости ($\bm f = 0$)
    
    $\begin{aligned}
    \frac{\partial \omega}{\partial t} + (\bm{v} \cdot \nabla) \omega - \nu \nabla^2 \omega = 0
    \end{aligned}$ 

    + $\nu = \mu / \varrho - $ кинематическая вязкость
    
    Уравнение для функции тока
    
    $\begin{aligned}
    {-} \nabla^2 \psi = \omega 
    \end{aligned}$  
    
    Краевые условия на твердой границе
    
    + $\psi = \operatorname{const} - $ условие непротекания
    + $\partial \psi / \partial n = 0 - $ условие прилипания 
  
    """    
    
if menu == "Идеальная жидкость":

    r"""
    ##### Идеальная жидкость

    Уравнение для вихря 
    
    $\begin{aligned}
    \frac{\partial \omega}{\partial t} + (\bm{v} \cdot \nabla) \omega = 0
    \end{aligned}$     
    
    Краевые условия на твердой границе
    
    + $\psi = \operatorname{const} - $ условие непротекания  
    
    Стационарные течения
    
    $\begin{aligned}
    {-} \nabla^2 \psi = \omega(\psi)
    \end{aligned}$     
   
    """    
    
