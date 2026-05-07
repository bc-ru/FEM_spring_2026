import streamlit as st
 
menu = st.sidebar.radio('***',
    ("Краевая задача", 
    "Малый параметр", 
    "Параметрические расчеты"
    )
)
  
if menu == "Краевая задача":
    r"""
##### Краевая задача
**Расчетная область**

Единичный квадрат

$\begin{aligned}
\Omega = \{\bm x \ | \ \bm x = (x_1, x_2), \quad 0 < x_1 < 1, \quad 0 < x_2 < 1 \}
\end{aligned}$

**Уравнение**

$\begin{aligned}
-\varepsilon \Delta u + u = f(\bm x), \quad \bm x \in \Omega
\end{aligned}$

Оператор Лапласа

$\begin{aligned}
\Delta = \mathrm{div \, grad} = \frac{\partial^2 } {\partial x_1^2} + \frac{\partial^2 } {\partial x_2^2}
\end{aligned}$

**Граничные условия**

Однородные условия первого рода (Дирихле)

$\begin{aligned}
u(\bm x) = 0, \quad x_1 = 1, \quad x_2 = 1
\end{aligned}$

Однородные условия второго рода (Неймана)

$\begin{aligned}
\frac{\partial u}{\partial \nu} (\bm x) = 0, \quad x_1 = 0, \quad x_2 = 0
\end{aligned}$

$\bm \nu$ - нормаль к границе

    """
    
if menu == "Малый параметр":
    r"""
##### Малый параметр
**Вырожденная задача**

Параметр $\varepsilon = 0$

$\begin{aligned}
u_0(\bm x) = f(\bm x), \quad \bm x \in  \Omega
\end{aligned}$

Основная особенность: $u_0(\bm x) \ne 0, \quad \bm x \in \partial \Omega$

**Сингулярно возмущенная задача**

При $\varepsilon \to 0$

 * $u(\bm x) \to u_0(\bm x)$ в части области ($ D \subset \Omega$)

 * $u(\bm x) \not\to u_0(\bm x)$ вблизи границы области
 
   """
    
if menu == "Параметрические расчеты":
    r"""
##### Параметрические расчеты
**Правая часть**

$\begin{aligned}
f(\bm x) = x_1 , \quad \bm x \in  \Omega
\end{aligned}$

**Расчетные сетки**

$\begin{aligned}
n \times n, \quad n = 10, 20, 40
\end{aligned}$

$n+1$ - число узлов по одному направлению

**Малый параметр**

Значение параметра $\ 0 < \varepsilon < 1$

    """
    
    
    
    
    
