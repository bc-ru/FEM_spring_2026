import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Пример", 
    "Интегральное тождество", 
    "Конечно-элементная аппроксимация",
    "Векторная запись",
    )
)

if menu == "Пример":
    r"""
##### Пример

$\Omega ~-~$ ограниченная область

$\bm x = (x_1, \ldots, x_d)$

**Система уравнений**

$\begin{aligned} -
 & \operatorname{div} \big (k_1(\bm x) \operatorname{grad} u_1 ) + r(\bm x) (u_1-u_2) = f_1(\bm x)  \\ -
 & \operatorname{div} \big (k_2(\bm x) \operatorname{grad} u_2 ) - r(\bm x) (u_1-u_2) = f_2(\bm x) ,  \quad \bm x \in \Omega
\end{aligned}$

**Части границ**

$\begin{aligned}
  \partial \Omega = \partial D_\alpha + \partial N_\alpha,
  \quad \alpha = 1,2 
\end{aligned}$

**Граничные условия**

Условия Дирихле (главные)

$\begin{aligned} 
 u_\alpha (\bm x) = g_\alpha(\bm x),
 \quad \bm x \in   \partial D_\alpha,
  \quad \alpha = 1,2  
\end{aligned}$

Условия Неймана (естественные)

$\begin{aligned} 
 k(\bm x)_\alpha \frac{\partial u_\alpha}{\partial n}(\bm x) = \mu_\alpha(\bm x),
 \quad \bm x \in   \partial N_\alpha,
  \quad \alpha = 1,2  
\end{aligned}$
    """  
  
if menu == "Интегральное тождество":
    r"""
##### Интегральное тождество

**Пространства**

Для $\alpha = 1,2$

* $V^\alpha$ - пространство достаточно гладких функций
* подпространство $V^\alpha_D = \{ v \ | \ v \in V^\alpha, \quad v(\bm x) = g_\alpha(\bm x),
  \quad \bm x \in \partial D_\alpha \}$ 
* подпространство $V^\alpha_0 = \{ v \ | \ v \in V^\alpha, \quad v(\bm x) = 0,
  \quad \bm x \in \partial D_\alpha \}$ 
  
  
**Система уравнений**

$\begin{aligned} -
 & \operatorname{div} \big (k_1(\bm x) \operatorname{grad} u_1 ) + r(\bm x) (u_1-u_2) = f_1(\bm x)  \\ -
 & \operatorname{div} \big (k_2(\bm x) \operatorname{grad} u_2 ) - r(\bm x) (u_1-u_2) = f_2(\bm x) ,  \quad \bm x \in \Omega
\end{aligned}$

Домножим скалярно в $L_2(\Omega)$ первое уравнение на $v_1(\bm x) \in V^1_0$, 

$\quad$ второе $-$ на $v_2(\bm x) \in V^2_0$

С учетом граничных условий

$\begin{aligned} 
 u_\alpha (\bm x) = g_\alpha(\bm x),
 \quad \bm x \in   \partial D_\alpha,
  \quad \alpha = 1,2  
\end{aligned}$

$\begin{aligned} 
 k(\bm x) \frac{\partial u_\alpha}{\partial n}(\bm x) = \mu_\alpha(\bm x),
 \quad \bm x \in   \partial N_\alpha,
  \quad \alpha = 1,2  
\end{aligned}$

получим

$\begin{aligned}
& \int_{\Omega} k_1(\bm x) \operatorname{grad} u_1 \operatorname{grad} v_1 \, d x + \int_{\Omega}  r(\bm x) (u_1-u_2) \, v_1 \, dx = \int_{\Omega} f_1(\bm x) v_1 \, d x + \int_{\partial N_1} \mu_1(\bm x) v_1 \, dx \\
& \int_{\Omega} k_2(\bm x) \operatorname{grad} u_2 \operatorname{grad} v_2 \, d x - \int_{\Omega}  r(\bm x) (u_1-u_2) \, v_2 \, dx = \int_{\Omega} f_2(\bm x) v_2 \, d x + \int_{\partial N_2} \mu_2(\bm x) v_2 \, dx \\
\end{aligned}$

для

$\begin{aligned} 
 u_\alpha (\bm x) \in V^\alpha_D, 
 \quad v_\alpha (\bm x) \in V^\alpha_0, 
  \quad \alpha = 1,2  
\end{aligned}$

    """    
    
if menu == "Конечно-элементная аппроксимация":
    r"""
##### Конечно-элементная аппроксимация

Для каждой искомой величины $ u_\alpha (\bm x), \ \alpha = 1,2$ своя аппроксимация в $\Omega$ 

$\quad$ (сетка, конечные элементы)  

Для $V_h^\alpha \ (V^\alpha_h \subset V^\alpha)), \ \alpha = 1,2$ 

Базисы функции

$\varphi^\alpha_{i_\alpha}(\bm x) , \quad i_\alpha = 1,2, \ldots, n_\alpha$

$\begin{aligned}
 \varphi^\alpha_{i_\alpha}(\bm x_{j_\alpha}) = \begin{cases}
  1 ,  &  i_\alpha = j_\alpha \\
  0 ,  &   i_\alpha \ne j_\alpha \\
\end{cases}
  \quad \alpha = 1,2  
\end{aligned}$

Приближенное решение

$\begin{aligned}
 &   u^\alpha(\bm x) \approx y^\alpha(\bm x) = \sum_{i_\alpha=1}^{n_\alpha} y^\alpha_{i_\alpha} \varphi_{i_\alpha}^\alpha(\bm x) \\
 & y^\alpha_{i_\alpha} = y^\alpha(\bm x_{i_\alpha}),
   \quad i_\alpha = 1,2, \ldots, n_\alpha, 
  \quad \alpha = 1,2     
\end{aligned}$

    """  
    
if menu == "Векторная запись":
    r"""
##### Векторная запись

Вектор решений $\bm u(\bm x) = \{u_1(\bm x), u_2(\bm x)\}$

Определим пространство $\bm V$ векторных функций $\bm u$ 

$\quad$ на прямой сумме пространств $V^1$ и  $V^2$ 

Скалярное произведение и норма в $\bm V$ 

$\begin{aligned} 
 (\bm u, \bm v) = (u_1, v_1) + (u_2, v_2),
 \quad \|\bm u\| = (\bm u, \bm u)^{1/2}
\end{aligned}$

Систему уравнений 

$\begin{aligned} -
 & \operatorname{div} \big (k_1(\bm x) \operatorname{grad} u_1 ) + r(\bm x) (u_1-u_2) = f_1(\bm x)  \\ -
 & \operatorname{div} \big (k_2(\bm x) \operatorname{grad} u_2 ) - r(\bm x) (u_1-u_2) = f_2(x) 
\end{aligned}$

запишем в виде

$\begin{aligned} 
 \bm {\mathcal{A}}  \bm u = \bm f
\end{aligned}$

Операторные матрицы

$\begin{aligned}
& \bm {\mathcal{A}} = 
\begin{pmatrix}
{-} \operatorname{div} k_1(\bm x) \operatorname{grad} + r(\bm x) & - r(\bm x) \\
{-} r(\bm x) & - \operatorname{div} k_2(\bm x) \operatorname{grad} + r(\bm x) 
\end{pmatrix} \\
& \bm f(\bm x) = \{f_1(\bm x), f_2(\bm x) \}
\end{aligned}$	

Вариационная задача

$\begin{aligned} 
 a (\bm u,  \bm v)  = l(\bm v)
\end{aligned}$

в которой

$\begin{aligned}
& a (\bm u,  \bm v)   = (k_1(\bm x) \operatorname{grad} u_1, \operatorname{grad} v_1) + (r(\bm x) u_1, v_1) - (r(\bm x) u_2, v_1)  \\
&~ \qquad \quad + 
(k_2(\bm x) \operatorname{grad} u_2, \operatorname{grad} v_2) - (r(\bm x) u_1, v_2) + (r(\bm x) u_2, v_2) \\
& l(\bm v) = (f_1(\bm x), v_1) + (\mu_1(\bm x) v_1)_{\partial N_1} +
(f_2(\bm x), v_2) + (\mu_2(\bm x) v_2)_{\partial N_2}
\end{aligned}$	



    """   
    

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
