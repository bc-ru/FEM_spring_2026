import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Спектральная задача", 
    "Эллиптический оператор",
    "Интегральное следствие",        
    "Вариационная задача", 
    "Конечно-элементное решение",    
    "Матричная задача",                       
    )
)
  
if menu == "Спектральная задача":
    r"""
##### Спектральная задача

В ограниченной области $\Omega$ определим дифференциальный оператор $\mathcal A$

Для достаточно гладких функций $u(\bm x), \ \bm x \in \Omega$, $\\ \quad $ удовлетворяющих однородным граничным условиям на $\partial \Omega$, $\\ \quad$ ищутся нетривиальные решения ($u(\bm x) \not \equiv 0, \ \bm x \in \Omega$) 

$\begin{aligned}
\mathcal A u = \lambda u
\end{aligned}$

Решение спектральной задачи

* $\lambda_k, \quad k = 1,2, \ldots - $ собственные значения
* $\phi_k(\bm x), \quad k = 1,2, \ldots - $ собственные функции

Более общие спектральные задачи

$\begin{aligned}
\mathcal A u = \lambda \mathcal B u
\end{aligned}$

$\mathcal A ,  \mathcal B - $ дифференциальные операторы

    """

if menu == "Эллиптический оператор":
    r"""
##### Эллиптический оператор

Оператор второго порядка

$\begin{aligned} 
 \mathcal A u = - \operatorname{div} \big (k(\bm x) \operatorname{grad} u + \bm a(\bm x) u \big ) +
 \bm b(\bm x) \cdot \operatorname{grad} u + c(\bm x) u ,
 \quad \bm x \in  \Omega 
\end{aligned}$

на множестве функций

$\begin{aligned} 
 k(\bm x) \frac{\partial u}{\partial n} + \sigma (\bm x) u = 0,
 \quad \bm x \in   \partial \Omega
\end{aligned}$

Коэффициенты $k(\bm x) > 0, \ c(\bm x) \geq 0, \ \sigma(\bm x) \geq 0$

Конвективный перенос

* $\bm a(\bm x) ~-~$ консервативный (дивергентный)
* $\bm b(\bm x) ~-~$ характеристический (недивергентный)
    """
    
if menu == "Интегральное следствие":
    r"""
##### Интегральное следствие

$V$ - пространство достаточно гладких функций

Для $u,v \in V$

$\begin{aligned}
(\mathcal{A} u - \lambda u, v) = 0 
\end{aligned}$  

С учетом граничных условий

$\begin{aligned}
& \int_{\Omega} k(\bm x) \operatorname{grad} u \operatorname{grad} v \, d x + \int_{\Omega}  c(\bm x) u \, v \, dx +
\int_{\partial \Omega}  \sigma(\bm x) u \, v \, dx \\ 
& - \int_{\Omega} \operatorname{div} (\bm a(\bm x) u) v \, dx +
\int_{\Omega}  \bm b(\bm x) \cdot \operatorname{grad} u \, v \, d x \\ 
& = \lambda \int_{\Omega} u \, v \, d x 
\end{aligned}$

    """

if menu == "Вариационная задача":
    r"""
##### Вариационная задача

Найти $\lambda, u \in V$ такие, что 

$\begin{aligned}
a(u,v) = \lambda b(u,v),
\quad \forall v \in V
\end{aligned}$ 

Билинейные формы

$\begin{aligned}
a(u,v) & = \int_{\Omega} k(\bm x) \operatorname{grad} u \operatorname{grad} v \, d x + \int_{\Omega}  c(\bm x) u \, v \, dx +
\int_{\partial \Omega}  \sigma(\bm x) u \, v \, dx \\ 
& - \int_{\Omega} \operatorname{div} (\bm a(\bm x) u) v \, dx +
\int_{\Omega}  \bm b(\bm x) \cdot \operatorname{grad} u \, v \, d x 
\end{aligned}$ 

$\begin{aligned}
b(u,v) = \int_{\Omega} u \, v \, d x 
\end{aligned}$ 

    """
if menu == "Конечно-элементное решение":
    r"""
##### Конечно-элементное решение

Конечно-элементный базис в $V_h \subset V$

$\begin{aligned}
 \varphi_i(\bm x),
 \quad i = 1,2, \ldots, n 
\end{aligned}$

$\begin{aligned}
 \varphi_i(x_j) = \begin{cases}
  1 ,  &  i = j , \\
  0 ,  &  i \neq j \\
\end{cases}
\end{aligned}$

Приближенное решение

$\begin{aligned}
   y(\bm x) = \sum_{i=1}^{n} y_i \varphi_i(\bm x) ,
   \quad y_i = y(\bm x_i),
   \quad i = 1,2, \ldots, n
\end{aligned}$

    """

if menu == "Матричная задача":
    r"""
##### Матричная задача

Вариационная постановка

$\begin{aligned}
y \in V_h = \, ?
\end{aligned}$ 

$\begin{aligned}
a(y,v) = \lambda b(y,v),
\quad \forall v \in V_h
\end{aligned}$ 

Метод Галеркина

$\begin{aligned}
 \sum_{j=1}^{n} a(\varphi_j, \varphi_i)  y_j  = \lambda
 \sum_{j=1}^{n} b(\varphi_j, \varphi_i)  y_j
 \quad i = 1,2, \ldots , n
\end{aligned}$

Спектральная задача линейной алгебры

$\begin{aligned}
A y = \lambda B y
\end{aligned}$ 

Матрицы

$\begin{aligned}
A = \{a_{ij} \}, \quad B = \{b_{ij} \}
\end{aligned}$ 

с элементами

$\begin{aligned}
  a_{ij} = a(\varphi_j, \varphi_i) ,
  \quad b_{ij} = b(\varphi_j, \varphi_i) ,
  \quad i, j = 1,2, \ldots , n
\end{aligned}$


    """



