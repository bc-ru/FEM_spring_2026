import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Параболическая задача", 
    "Метод конечных элементов",    
    "Вариационная задача", 
    "Априорная оценка",   
    "Аппроксимация по пространству",      
    "Задача для коэффициентов",     
    "Система ОДУ",    
    "Оценка для коэффициентов",           
    "Операторная формулировка для решения",     
    )
)
  
if menu == "Параболическая задача":
    r"""
##### Параболическая задача

$\Omega - $ ограниченная область с границей $\partial \Omega$

Эллиптический оператор $\mathcal{A}$ 

$\begin{aligned}
 \mathcal{A} u = - \operatorname{div} (k(x) \operatorname{grad} u ) + d(x) u ,
 \quad x \in \Omega  
\end{aligned}$

на множестве функций

$\begin{aligned}
 u(x) = 0 , 
 \quad x \in \partial \Omega  
\end{aligned}$

Коэффициенты  $k(x)$ и $d(x)$

$\begin{aligned}
 k(x) \geq \kappa > 0,
 \quad d(x) \geq 0 ,
 \quad x \in \Omega 
\end{aligned}$

Рассматривается задача Коши

$\begin{aligned}
 \frac{\partial u}{\partial t} + \mathcal{A} u = f(x,t),
 \quad x \in \Omega, 
 \quad 0 < t \leq T  
\end{aligned}$

$\begin{aligned}
 u(x,0) = u^0(x),
 \quad x \in \Omega  
\end{aligned}$

    """
    
if menu == "Метод конечных элементов":
    r"""
##### Метод конечных элементов

При решении нестационарных задач 

**Частичная аппроксимация конечными элементами**

* Аппроксимация конечными элементами по пространству
* Разностная аппроксимация по времени

**Глобальная аппроксимация конечными элементами** 

* Переменные $x$ и $t$ не различаются
* Конечно-элементная аппроксимация функций от переменной $s = (x_1, \ldots, x_d, t)$

    """
    
if menu == "Вариационная задача":
    r"""
##### Вариационная задача

Пространства

* пространство достаточно гладких функций

* подпространство $V_0 = \{ v \ | \ v \in V, \ v(x) = 0,
  \ x \in \partial\Omega \}$ 
  
Домножая уравнение на $v(x) \in V_0$ и интегрируя по области $\Omega$, 
придем 

$\begin{aligned}
 \left( \frac{\partial u}{\partial t}, v \right ) + a(u,v) = (f, v), 
 \quad \forall  v \in V_0 ,
 \quad 0 < t \leq T 
\end{aligned}$

Билинейная форма

$\begin{aligned}
 a(u,v) = \int_{\Omega} ( k \operatorname{grad} u \cdot \operatorname{grad} v + d \, u \, v)  d  x 
\end{aligned}$

Начальное условие

$\begin{aligned}
 (u(0),v) = (u^0, v), 
 \quad \forall  v \in V_0
\end{aligned}$

Вариационная формулировка

$u(x, t) \in V_0 = ?$ 

    """
    
if menu == "Априорная оценка":
    r"""
##### Априорная оценка

Положим $v = u$

$\begin{aligned}
 \left( \frac{\partial u}{\partial t}, u \right ) + a(u,u) = (f, u)
\end{aligned}$

Принимая во внимание

$\begin{aligned}
 a(u,u) \geq \kappa \int_{\Omega} |\operatorname{grad} u|^2 dx \geq 0
\end{aligned}$

$\begin{aligned}
 (f,u) \leq \|f\| \|u\| 
\end{aligned}$

получим неравенство

$\begin{aligned}
 \frac{d }{d t} \|u(t)\| \leq \|f(t)\| 
\end{aligned}$

Из этого неравенство следует 

$\begin{aligned}
 \|u(t)\| \leq \|u^0\| + \int_{0}^{t}\|f(\theta)\| d \theta 
\end{aligned}$

    """    

if menu == "Аппроксимация по пространству":
    r"""
##### Аппроксимация по пространству

Пространства

* конечно-элементное пространство $V$ (кусочно-гладкие фенкции)

* подпространство $V_0 = \{ v \ | \ v \in V, \ v(x) = 0,
  \ x \in \partial\Omega \}$ 

Пробные функции в $V_0$ 

$\varphi_i(x) , \quad i = 1,2, \ldots, m$

$\begin{aligned}
 \varphi_i(x_j) = \begin{cases}
  1 ,  &  i = j \\
  0 ,  &  i \neq j \\
\end{cases}
\end{aligned}$

Приближенное решение нестационарной задачи

$\begin{aligned}
   & u(x,t) \approx y(x,t) = \sum_{i=1}^{m} y_i(t) \varphi_i(x) \\
   & y_i(t) = y(x_i,t),
   \quad i = 1,2, \ldots, m
\end{aligned}$

    """

if menu == "Задача для коэффициентов":
    r"""
##### Задача для коэффициентов

Приближенное решение $y(x,t) \in V_0, \ 0 \le t \le T$ нестационарной задачи

$\begin{aligned}
   y(x,t) = \sum_{i=1}^{m} y_i(t) \varphi_i(x) 
\end{aligned}$

Вариационная задача

$\begin{aligned}
 \left( \frac{\partial y}{\partial t}, v \right ) + a(y,v) = (f, v), 
 \quad \forall  v \in V_0 ,
 \quad 0 < t \leq T 
\end{aligned}$

$\begin{aligned}
 (y(0),v) = (u^0, v), 
 \quad \forall  v \in V_0
\end{aligned}$

Выберем (метод Галеркина)  $v(x) = \varphi_i(x) , \quad i = 1,2, \ldots, m$

$\begin{aligned}
& \sum_{j=1}^{m} \frac{d y_j}{d t} (t) \, (\varphi_j, \varphi_i)  +
 \sum_{j=1}^{m} y_j (t) \, a (\varphi_j, \varphi_i) =  (f, \varphi_i),
 \quad 0 < t \leq T 
\end{aligned}$

$\begin{aligned}
 \sum_{j=1}^{m} y_j (0) \, (\varphi_j, \varphi_i) =  (u^0, \varphi_i), 
 \quad i = 1,2, ..., m
\end{aligned}$

    """

if menu == "Система ОДУ":
    r"""
##### Система ОДУ

Матричная форма

$\begin{aligned}
 B \frac{d y}{d t} + A y = \chi (t),
 \quad 0 < t \leq T 
\end{aligned}$

$\begin{aligned}
 y(0) = y^0 .
\end{aligned}$

$y(t) = \{y_i (t)\} - $ искомый вектор

$\chi (t) = \{\chi_i\}, \ \chi_i = (f, \varphi_i) - $  заданная правая часть (вектор)

Матрица масс

$\begin{aligned}
 B = \{b_{ij}\}, \quad  b_{ij} = (\varphi_j, \varphi_i),
 \quad i,j =  1,2, ..., m 
\end{aligned}$

Матрица жесткости

$\begin{aligned}
 A = \{a_{ij}\}, \quad  a_{ij} = a(\varphi_j, \varphi_i),
 \quad i,j =  1,2, ..., m
\end{aligned}$

Задача Коши для системы 
обыкновенных дифференциальных уравнений  

$\quad$ для вектора неизвестных $y_i(t), \ i = 1,2, ..., m$ 

    """
    
if menu == "Оценка для коэффициентов":
    r"""
##### Оценка для коэффициентов

Мы можем рассматривать вещественные квадратные матрицы $B$ и $A$ как операторы в пространстве  $\mathbb{R}^{m}$

Для векторов $y = \{y_1, y_2, \dots, y_{m}\}$ из $\mathbb{R}^{m}$
скалярное произведение и норма есть

$\begin{aligned}
 (y,v) = \sum_{i=1}^{M_h} y_i v_i,
 \quad \|y \| = (y,y)^{1/2}  
\end{aligned}$

Принимая во внимания расчетные формулы для элементов  матрицы масс и матрицы жесткости, получим

$\begin{aligned}
 B = B^* > 0, 
 \quad A = A^* > 0  
\end{aligned}$

в гильбертовом пространстве  $\mathbb{R}^{m}$

Пусть $H_B - $  гильбертово пространство, порожденное оператором  $B$, в котором

$\begin{aligned}
 (y,v)_B = (B y, v),
 \quad \|y\|_B =  (B y, y)^{1/2} 
\end{aligned}$

Домножая уравнение скалярно в  $\mathbb{R}^{m}$ на $y$, придем к оценке

$\begin{aligned}
 \|y(t)\|_B \leq \|y^0\|_{B} + \int_{0}^{t}\|\chi(s)\|_{B^{-1}} d x 
\end{aligned}$

    """

if menu == "Операторная формулировка для решения":
    r"""
##### Операторная формулировка для решения

Нас интересует операторная формулировка задачи в пространстве решений $V_0$
 
Определим оператор $A: V_0 \rightarrow V_0$ такой, что

$\begin{aligned}
 (A y, v) = a(y, v) ,
 \quad \forall  y, v \in V_0 
\end{aligned}$

С учетом свойств билинейной формы $a(\cdot, \cdot)$ оператор $A$ является самосопряженным и положительно определенным
в $V_0$

Уравнение в операторной форме

$\begin{aligned}
 \frac{d y}{d t} + A y = P f, 
 \quad 0 < t \leq T 
\end{aligned}$

Начальное условие

$\begin{aligned}
 y(0) = P u^0 
\end{aligned}$

Ортогональный проектор $P$ гильбертового пространства $L_2(\Omega)$ 

$\quad$ на конечномерное пространство $V$ 

$\begin{aligned}
 (P u - u, v ) = 0,
 \quad \forall v \in V, \ u \in L_2(\Omega) 
\end{aligned}$

    """
















