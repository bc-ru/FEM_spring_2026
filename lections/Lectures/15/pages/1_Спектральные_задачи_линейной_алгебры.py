import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Проблема собственных значений", 
    "Характеристическое уравнение",    
    "Простейшие примеры", 
    "Классы спектральных задач",   
    "Ортогональность собственных векторов",      
    "Сопряженная матрица",     
    "Отношения Релея и собственные значения",       
    "Максимальное по модулю собственное значение",    
    "Минимальное по модулю собственное значение",         
    "Полная проблема собственных значений",     
    )
)
  
if menu == "Проблема собственных значений":
    r"""
##### Проблема собственных значений

$A - $ квадратная вещественная матрица

Собственным числом называется число $\lambda$ такое, что для
некоторого ненулевого вектора (собственного вектора) $\phi$
имеет место равенство

$\begin{aligned}
  A \phi = \lambda \phi 
\end{aligned}$

Собственные вектора определены с точностью до числового множителя

Множество всех собственных значений матрицы $A$ называется
спектром матрицы $A$

Собственные значения и собственные функции, вообще говоря, комплексные

    """    
if menu == "Характеристическое уравнение":
    r"""
##### Характеристическое уравнение

Ищется решение системы

$\begin{aligned}
 (A - \lambda I) \phi = 0
\end{aligned}$

Эта система имеет решение $\phi \neq 0$ тогда и только тогда, когда

$\begin{aligned}
 \mathrm{det} (A - \lambda I) = 0
\end{aligned}$

Для $\lambda$ алгебраическое уравнение $l$-степени

$\begin{aligned}
 \lambda^l + b_1 \lambda^{l-1} + b_2 \lambda^{l-2} + \cdots + b_l = 0 
\end{aligned}$

$l$ корней $\lambda_1, \lambda_2, \ldots, \lambda_l$ (возможно, кратных и комплексных)

Для $A = A^* - $  $\lambda$ и $\phi$ действительные

Комплексные собственные значения в виде пар

$\begin{aligned}
 \lambda = \alpha + i \beta , 
 \quad \overline{\lambda} = \alpha  - i \beta ,
 \quad \beta \neq 0
\end{aligned}$

    """
    
if menu == "Простейшие примеры":
    r"""
##### Простейшие примеры

Диагональная матрица

$\begin{aligned}
 A = {\rm diag}\{d_{1},d_{2},\ldots,d_{l}\} =  \begin{pmatrix}
  d_1 & 0 & \cdots &  0  \\
  0   & d_2 & \cdots &  0 \\
  \cdots & \cdots & \cdots &  \cdots  \\
  0 & 0 & \cdots &  d_l  \\
\end{pmatrix} 
\end{aligned}$

Собственные значения

$\begin{aligned}
 \lambda_k = d_k, 
 \quad k = 1, 2, \ldots, l 
\end{aligned}$

Нижняя или верхняя треугольные матрицы

$\begin{aligned}
 A = \begin{pmatrix}
  a_{11} & 0      & \cdots &  0       \\
  a_{21} & a_{22} & \cdots &  0       \\
  \cdots & \cdots & \cdots &  \cdots  \\
  a_{l1} & a_{l2} & \cdots &  a_{ll}  \\
\end{pmatrix} ,
\quad A = \begin{pmatrix}
  a_{11} & a_{12} & \cdots &  a_{1l}  \\
  0      & a_{22} & \cdots &  a_{2l}  \\
  \cdots & \cdots & \cdots &  \cdots  \\
  0      & 0      & \cdots &  a_{ll}  \\
\end{pmatrix}  
\end{aligned}$

Собственные значения

$\begin{aligned}
 \lambda_k = a_{kk}, 
 \quad k = 1, 2, \ldots, l 
\end{aligned}$
    """
    
if menu == "Классы спектральных задач":
    r"""
##### Классы спектральных задач

**(i)  Полная проблема собственных значений**

$\quad$ необходимо найти все собственные
значения матрицы $A$

**(ii)  Частичная проблема собственных значений**

$\quad$ некоторые собственные значения (максимальные, минимальные, ...) 

**Пример: задача Коши для системы ОДУ**

$\begin{aligned}
 \frac{d y}{d t} + A y = 0,
 \quad t > 0,  
 \quad y(0) = y^0 
\end{aligned}$

**(i)** Решение  для $A = A^* \ (\lambda_1 \leq \lambda_2 \leq  \cdots \leq \lambda_l)$  

$\begin{aligned}
 y(t) = \sum_{k = 1}^{l} (y^0, \phi_k) e^{- \lambda_k t} \phi_k
\end{aligned}$
 
**(ii)** Устойчивость

$\begin{aligned}
 \|y(t) \| \leq e^{- \lambda_1 t} \|y^0\|
\end{aligned}$

    """
    
if menu == "Ортогональность собственных векторов":
    r"""
##### Ортогональность собственных векторов

Для собственных векторов матрицы $A = A^*$,  соответствующие различным собственным значениям 

$\begin{aligned}
 (\phi_k,\phi_e) = 0, 
 \quad k \neq e,
 \quad k, e = 1,2, \ldots, l 
\end{aligned}$

Имеем

$\begin{aligned}
\begin{matrix}
  A \phi_k = \lambda_k \phi_k \\
  A \phi_e = \lambda_e \phi_e 
\end{matrix}
{\color{red}
\quad  \left |  \quad 
\begin{matrix} 
 \phi_e \\
 \phi_k 
\end{matrix}
\right .
}
\end{aligned}$

С учетом $(A \phi_k, \phi_e) = (\phi_k, A \phi_e)$

$\begin{aligned}
 (\lambda_k - \lambda_e) (\phi_k, \phi_e) = 0
\end{aligned}$
    """    

if menu == "Сопряженная матрица":
    r"""
##### Сопряженная матрица

Спектральные задачи

$\begin{aligned}
 A \phi = \lambda \phi ,
 \quad A^*\psi = \mu\psi 
\end{aligned}$

Основное свойство собственных значений

$\begin{aligned}
  \lambda_{k}=\mu_{k},
  \quad k=1,2,\ldots,l
\end{aligned}$

Следует из того, что $\mathrm{det} (A) = \mathrm{det} (A^*)$ 

Ортогональность

$\begin{aligned}
  (\phi_k, \psi_e) = 0,
  \quad k \neq e 
\end{aligned}$
    """

if menu == "Отношения Релея и собственные значения":
    r"""
##### Отношения Релея и собственные значения

Симметричная матрица $A$ 

$\begin{aligned}
 \lambda_1 \leq \lambda_2 \leq \cdots \leq \lambda_l
\end{aligned}$

Отношение Релея

$\begin{aligned}
 R(A,y) = \frac{(Ay,y)}{(y,y)}, 
 \quad \lambda_k = R(A,\phi_k), 
 \quad k = 1, 2, \ldots, l 
\end{aligned}$

Для любого $y \neq 0$

$\begin{aligned}
 \lambda_1 \leq \frac{(Ay,y)}{(y,y)} \leq \lambda_l ,
 \quad   \lambda_1 = \min_{y \neq 0} \frac{(Ay,y)}{(y,y)},
 \quad \lambda_l  = \max_{y \neq 0} \frac{(Ay,y)}{(y,y)} 
\end{aligned}$

Для $y$ 

$\begin{aligned}
 y = \sum_{k=1}^{l} c_k \phi_k,
 \quad (\phi_k, \phi_e) = \delta_{ke} = \left \{
 \begin{matrix}
  1, & \ k = e \\
  0, & \ k \neq e
\end{matrix} 
\right .
\end{aligned}$ 

Для $R(A,y)$ 

$\begin{aligned}
 R(A,y) = \frac{\sum_{k=1}^{l} \lambda_k c_k^2}{\sum_{k=1}^{l} c_k^2} 
\end{aligned}$
    """

if menu == "Максимальное по модулю собственное значение":
    r"""
##### Максимальное по модулю собственное значение

Пусть $A = A^*$ и все собственные значения простые, причем

$\begin{aligned}
  |\lambda_1 | < | \lambda_2 | < \cdots < |\lambda_l| 
\end{aligned}$

Прямые итерации (явный метод)

$\begin{aligned}
  y^{s+1} = A y^{s},
  \quad s = 0,1,\ldots
\end{aligned}$

при некотором заданном $y^0 \neq 0$

При $(y^0,\phi^l) \neq 0$

$\begin{aligned}
  R(A,y^s) =  \frac{(y^{s+1},y^s)}{(y^s,y^s)} =
  \lambda_l + \mathcal{O} \bigg( \left |\frac{\lambda_{l-1}}{\lambda_l} \right |^{2k} \bigg)
\end{aligned}$

Для собственного вектора

$\begin{aligned}
 \lim_{s \rightarrow \infty} y^s = \phi^l
\end{aligned}$
    """

if menu == "Минимальное по модулю собственное значение":
    r"""
##### Минимальное по модулю собственное значение

Собственные значения обратной матрицы $A^{-1}$ 

$\begin{aligned}
 \frac{1}{\lambda_k} , 
 \quad k = 1,2, \dots, l
\end{aligned}$

Обратные итерации

$\begin{aligned}
  y^{s+1} = {\color{red}A^{-1} y^s},
  \quad (y^0,\phi^1) \neq 0,
  \quad s = 0,1,\ldots
\end{aligned}$

При $(y^0,\phi^1) \neq 0$

$\begin{aligned}
  R(A,y^s) =  \frac{(y^{s+1},y^s)}{(y^s,y^s)} =
  \frac{1}{\lambda_1} + \mathcal{O} \bigg( \left |\frac{\lambda_{1}}{\lambda_2} \right |^{2s} \bigg)
\end{aligned}$

Для собственного вектора

$\begin{aligned}
 \lim_{s \rightarrow \infty} y^s = \phi_1
\end{aligned}$
    """

if menu == "Полная проблема собственных значений":
    r"""
##### Полная проблема собственных значений

* Спектральная проблема для $A=A^* \\$ 
	итерационный метод (метод Якоби) (применение матриц вращения)
          
* Общий случай $\\ $ на основе $QR$-разложение матрицы ($A = QR$)   $\\ Q - $ 	ортогональная  ($Q^* Q = I$)  $\\ R - $  верхняя треугольная

    """
















