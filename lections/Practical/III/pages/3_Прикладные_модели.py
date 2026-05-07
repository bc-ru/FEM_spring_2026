import streamlit as st
from PIL import Image

menu = st.sidebar.radio('***',
    (
    "Базовая система уравнений",    
    "Краевые и начальные условия",  
    "Иерархия моделей",   
    )
)
if menu == "Базовая система уравнений":

    r"""
    ##### Базовая система уравнений
    
    **Уравнение Навье-Стокса**
    
    $\begin{aligned}
    \rho \left( \frac{\partial \bm{v}}{\partial t} + (\bm{v} \cdot \nabla) \bm{v} \right) + \nabla p - \mu \nabla^2 \bm{v} = \bm{f}
    \end{aligned}$ 

    **Уравнение неразрывности**
    
    $\begin{aligned}
    \nabla \cdot \bm{v} = 0
    \end{aligned}$ 
    
    """
    
if menu == "Краевые и начальные условия":

    r""" 
    ##### Краевые и начальные условия
    
    Уравнение второго порядка (условия для вектора скорости)
    
    **Твердая граница**
    
    Условия непротекания и прилипания
    
    $\begin{aligned}
    \bm{v}(\bm x, t) = \bm{v}_{wall}(\bm x, t), \quad \bm x \in \Gamma_{wall} \quad (= 0 - \text{неподвижная граница})  
    \end{aligned}$  
    
    **Условия на входе**
    
    Заданный профиль скорости
    
    $\begin{aligned}
    \bm{v}(\bm x, t) = \bm{v}_{inlet}(\bm x, t) , \quad \bm x \in \Gamma_{inlet} 
    \end{aligned}$  
        
     **Условия на выходе**
    
    Для скорости
    
    $\begin{aligned}
    \frac{\partial \bm{v}}{\partial n}(\bm x, 0) = 0, \quad \bm x \in \Gamma_{outlet} 
    \end{aligned}$ 
    
    Другие условия: симметрии, периодичности
    
    **Начальные условия**
    
    $\begin{aligned}
    \bm{v}(\bm x, 0) = \bm{v}^{0}(\bm x) 
    \end{aligned}$  
         
    """ 
if menu == "Иерархия моделей":

    r""" 
    ##### Иерархия моделей    
    
    **Турбулентные течения** ($\operatorname{Re} \gg 1$)
    
    + Вычислительная проблема - моделирование мелкомасштабных возмущений
    + Решение - гомогенизация, осреднение за счет дополнительных уравнений
    
    **Идеальная жидкость**
    
    Уравнение Эйлера
    
    $\begin{aligned}
    \rho \left( \frac{\partial \bm{v}}{\partial t} + (\bm{v} \cdot \nabla) \bm{v} \right) + \nabla p = \bm{f}
    \end{aligned}$ 
    
    Меньше граничных условий
     
    Например, на неподвижной твердой стенке (условие непротекания)
    
    $\begin{aligned}
    \bm{v}(\bm x, t) \cdot \bm n = 0
    \end{aligned}$  
    
    **Приближение Стокса** ($\operatorname{Re} \ll 1$)
    
    Вязкие силы играют основную роль, а инерционные силы пренебрежимо малы

    $\begin{aligned}
    \rho \frac{\partial \bm{v}}{\partial t} + \nabla p - \mu \nabla^2 \bm{v} = \bm{f}
    \end{aligned}$      
    
    **Безвихревые (потенциальные) течения** 
    
    Отсутствие завихренностей
    
    $\begin{aligned}
    \nabla \times \bm{v} = 0
    \end{aligned}$     
    
    Потенциал скорости
    
    $\begin{aligned}
    \bm{v} = \nabla \varphi
    \end{aligned}$   
    
    Для несжимаемых течений
    
    $\begin{aligned}
    \nabla^2 \varphi = 0 
    \end{aligned}$     
    
    """    
    
    
    
    
