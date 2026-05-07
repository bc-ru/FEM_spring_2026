import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Система нелинейных уравнений", 
    "Одношаговые итерационные методы",    
    "Стационарный итерационный метод", 
    "Одно уравнение",   
    "Итерационный метод Ньютона",  
    "Система уравнений",   
    "Модифицированный метод Ньютона",   
    "Методы Якоби и Зейделя",                   
    )
)
  
if menu == "Система нелинейных уравнений":
    r"""
##### Система нелинейных уравнений

Система из $n$ уравнений 

$\begin{aligned}
f_i(y_1,y_2,\ldots,y_n) = 0,
\quad i=1,2,\ldots,n 
\end{aligned}$

$y = \{y_1,y_2,\ldots,y_n\} - $ вектор неизвестных

$F(y) = \{f_1,f_2,\ldots,f_n\} - $ вектор-функция

Краткая запись

$\begin{aligned}
  F(y) = 0
\end{aligned}$
    """

if menu == "Одношаговые итерационные методы":
    r"""
##### Одношаговые итерационные методы

Система нелинейных уравнений

$\begin{aligned}
  F(y) = 0
\end{aligned}$

В одношаговых итерационных методах
новое приближение $y^{k+1}$ определяется по предыдущему приближению  $y^{k}$

Итерационный метод

$\begin{aligned}
  B_{k+1}(y^k) \frac{y^{k+1}-y^k}{\tau_{k+1}} + F(y^k) = 0,
  \quad k =0,1,\ldots
\end{aligned}$

$\tau_{k+1} - $  итерационные параметры

$B_{k+1}(y^k) - $ квадратная матрица $n\times n$, имеющая обратную
    """
    
if menu == "Стационарный итерационный метод":
    r"""
##### Стационарный итерационный метод

Пусть $B_{k+1}(y^k) = B$ и $\tau_{k+1} = \tau$

Перейдем от уравнения

$\begin{aligned}
  F(y) = 0
\end{aligned}$

к уравнению

$\begin{aligned}
 y = S(y),
 \quad S(y) = y - \tau B^{-1} F(y) 
\end{aligned}$

Метод простой итерации

$\begin{aligned}
  y^{k+1} = S(y^k),
  \quad k =0,1,\ldots
\end{aligned}$
    """
    
if menu == "Одно уравнение":
    r"""
##### Одно уравнение

Для нахождения $y$

$\begin{aligned}
 f(y) = 0
\end{aligned}$

используется итерационный метод

$\begin{aligned}
 b(y^k) \frac{y^{k+1} - y^k}{\tau_{k+1}} + f(y^k) = 0,
 \quad k = 0,1, \ldots 
\end{aligned}$

Решение на новой итерации

$\begin{aligned}
 y^{k+1} = y^k - \tau_{k+1} b^{-1}(y^k) f(y^k) 
\end{aligned}$

Метод простой итерации

$\begin{aligned}
  b^{-1}(y) = g(y) ,
 \quad \tau_{k+1} = 1 ,
 \quad k = 0,1, \ldots   
\end{aligned}$ 

    """
if menu == "Итерационный метод Ньютона":
    r"""
##### Итерационный метод Ньютона

Ряд Тейлора

$\begin{aligned}
 f(y^{k+1}) = f(y^k) + (y^{k+1} - y^k) f'(y^*), 
  \quad f'(y) \equiv \frac{df}{dy} (y)
\end{aligned}$ 

Из $f(y^{k+1}) \approx  0$ 
для нового приближения 

$\begin{aligned}
  y^{k+1} = y^k - \frac{f(y^k)}{f'(y^k)},
  \quad k =0,1,\ldots
\end{aligned}$ 

В общей форме

$\begin{aligned}
  b(y) = - f'(y) ,
 \quad \tau_{k+1} = 1 ,
 \quad k = 0,1, \ldots    
\end{aligned}$   

    """    
if menu == "Система уравнений":
    r"""
##### Система уравнений

Новое приближение определяется из решения системы линейных уравнений

$\begin{aligned}
&  \sum_{j=1}^{n} (y_j^{k+1}-y_j^k) \frac{\partial f_i(y^{k})}{\partial y_j}+
  f_i(y^k) = 0 \\
& i =1,2,\ldots,n,
  \quad k=0,1,\ldots 
\end{aligned}$  

Матрица Якоби

$\begin{aligned}
  F'(y) = \begin{pmatrix}
    {\displaystyle
    \frac{\partial f_1(y)}{\partial y_1}} &
    {\displaystyle \frac{\partial f_1(y)}{\partial y_2} }&
    \cdots &
    {\displaystyle \frac{\partial f_1(y)}{\partial y_n} }\\[10pt]
    {\displaystyle
    \frac{\partial f_2(y)}{\partial y_1} }&
    {\displaystyle \frac{\partial f_2(y)}{\partial y_2} }&
    \cdots &
    {\displaystyle \frac{\partial f_2(y)}{\partial y_n} }\\[0pt]
    {\displaystyle
    \cdots }& \cdots & \cdots & \cdots \\[0pt]
    {\displaystyle
    \frac{\partial f_n(y)}{\partial y_1} }&
    {\displaystyle \frac{\partial f_n(y)}{\partial y_2} }&
    \cdots &
    {\displaystyle \frac{\partial f_n(y)}{\partial y_n} }\
\end{pmatrix}
\end{aligned}$  

Метод Ньютона

$\begin{aligned}
  F'(y^k) (y^{k+1}-y^k) + F(y^k) = 0,
  \quad k=0,1,\ldots 
\end{aligned}$  

Одношаговый итерационный метод

$\begin{aligned}
 B_{k+1}(y^k) = F'(y^k), 
 \quad  \tau_{k+1} = 1
\end{aligned}$       
    """
    
if menu == "Модифицированный метод Ньютона":
    r"""
##### Модифицированный метод Ньютона

Основные вычислительные сложности применения метода Ньютона 

* необходимость решения линейной системы уравнений с матрицей Якоби на каждой итерации
* от итерации к итерации эта матрица меняется 

В модифицированном методе Ньютона

$\begin{aligned}
  F'(y^{0}) (y^{k+1}-y^k) + F(y^k) = 0,
  \quad k=0,1,\ldots
\end{aligned}$   

матрица Якоби обращается только один раз
    """
    
if menu == "Методы Якоби и Зейделя":
    r"""
##### Методы Якоби и Зейделя

Прямые аналоги стандартных итерационных методов для
решения систем линейных уравнений

**Нелинейный метод Якоби**

$\begin{aligned}
    f_i(y^{k}_1,y^{k}_2,\ldots,{\color{red} y^{k+1}_i},y^k_{i+1},\ldots,y^k_n) = 0,
    \quad i=1,2,\ldots,n 
\end{aligned}$  

**Нелинейный метод Зейделя**

$\begin{aligned}
    f_i({\color{red}y^{k+1}_1,y^{k+1}_2,\ldots,y^{k+1}_i},y^k_{i+1},\ldots,y^k_n) = 0,
    \quad i=1,2,\ldots,n 
\end{aligned}$  

Каждая компонента нового приближения находится из решения
нелинейного уравнения
    """




