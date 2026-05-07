import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Итерационные методы", 
    "Двухслойный итерационный метод",    
    "Построение итерационных методов", 
    "Методы Якоби и Зейделя",  
    "Операторная (матричная) запись",      
    "Некоторые более общие методы",        
    )
)
  
if menu == "Итерационные методы":
    r"""
##### Итерационные методы

Решается система линейных уравнений

$\begin{aligned}
     A y = g
\end{aligned}$

Матрица $A ~-~$ линейный оператор, действующий
в $H = l_2$, в котором 

$\begin{aligned}
(y,v) = \sum_{i=1}^{n} y_i v_i, 
\quad \|y\| = (y,y)^{1/2}
\end{aligned}$

$k ~-~$  номер итерации

При заданном начальном  приближении  $y^0 \in H$ 

$\quad ~$    последовательно определяются приближенные решения  $y^1, y^2,\ldots, y^k, \ldots$  

Значения $y^{k+1}$ определяются по ранее найденным $y^k,~ y^{k-1},\ldots$

**Основные итерационные методы**

* Одношаговый (двухслойный) 

  вычисление $y^{k+1}$ по ранее найденному $y^k$

* Двухшаговый (трехслойный) 

  вычисление $y^{k+1}$ по $y^k, \ y^{k-1}$

    """

if menu == "Двухслойный итерационный метод":
    r"""
##### Двухслойный итерационный метод 

Каноническая форма

$\begin{aligned}
  B \frac {y^{k+1} - y^k}{\tau_{k+1}} + A y^k = g,
  \quad k = 0,1,\ldots 
\end{aligned}$

Решение из

$\begin{aligned}
 y^{k+1} = y^{k} - \tau_{k+1} B^{-1} r^k,
 \quad r^k = Ay^k - g = Ay^k - Ay 
\end{aligned}$

Погрешность $z^k  = y^k  -  y$, невязка $r^k  = Az^k$

Итерационный метод сходится в $H_R$, $R = R^* > 0$, 

$\quad ~$  если $\|z^k \|_R \to 0$ при $k \to \infty$

Относительная погрешность $\varepsilon$ при выполнении $K$ итераций

$\begin{aligned}
  \|y^K - y\|_R \le \varepsilon \|y^0 - y\|_R 
\end{aligned}$

Например, при $R = A^* A$ 

$\begin{aligned}
  \|r^K \| \le \varepsilon \|r^0 \| 
\end{aligned}$
    """
    
if menu == "Построение итерационных методов":
    r"""
##### Построение итерационных методов

Минимизация вычислительной работы по нахождению приближенного
решения с заданной точностью

Пусть $Q_k ~-~$ число арифметических действий для нахождения приближения $y^k$ и
пусть делается $K= K(\varepsilon)$ итераций 

Вычислительные затраты 

$\begin{aligned}
  Q(\varepsilon) = \sum_{k=1}^{K} Q_k 
\end{aligned}$

В двухслойном итерационном  методе 

$\begin{aligned}
  B_k \frac {y^{k+1} - y^k}{\tau_{k+1}} + A y^k = g,
  \quad k = 0,1,\ldots 
\end{aligned}$

Минимизация $Q(\varepsilon)$ за счет выбора

* операторов $B_k$
* параметров $\tau_{k+1}$

Матрицы $B_k ~-~$ из условий близости к $A$ ($B = A ~-~$ одна итерация) 

Общие стратегии выбора итерационных параметров
    """
    
if menu == "Методы Якоби и Зейделя":
    r"""
##### Методы Якоби и Зейделя

Система линейных уравнений

$\begin{aligned}
  \sum_{j=1}^{n} a_{ij} y_{j} = g_i,
  \quad i=1,2,\ldots,n 
\end{aligned}$

Метод Якоби: новое приближение на $k+1$-й итерации

$\begin{aligned}
  \sum_{j=1}^{i-1} a_{ij} y_{j}^{k} + a_{ii} {\color{red}y_{i}^{k+1}} +
  \sum_{j=i+1}^{n} a_{ij} y_{j}^{k} = g_i,
  \quad i=1,2,\ldots,n 
\end{aligned}$

Компонента $y_{i}^{k+1}$ из $i$-ого уравнения, другие компоненты с  $k$-й итерации

Метод Зейдела 

$\begin{aligned}
  \sum_{j=1}^{i-1} a_{ij} {\color{red}y_{j}^{k+1}} + a_{ii} {\color{red}y_{i}^{k+1}} +
  \sum_{j=i+1}^{n} a_{ij} y_{j}^{k} = g_i,
  \quad i=1,2,\ldots,n 
\end{aligned}$

Найденное приближение для компонент решения сразу же задействуются в вычислениях

    """
    
if menu == "Операторная (матричная) запись":
    r"""
##### Операторная (матричная) запись

Разложение матрицы $A$

$\begin{aligned}
  A = L + D + U
\end{aligned}$

$D = {\rm diag} \{a_{11},a_{22},\ldots,a_{nn} \} ~-~$ 
диагональная часть матрицы $A$

$\begin{aligned}
 L = \begin{pmatrix}
  0      & 0      & 0      & \cdots &  0       \\
  a_{21} & 0      & 0      & \cdots &  0       \\
  a_{31} & a_{32} & 0      & \cdots &  0       \\
  \cdots & \cdots & \cdots & \cdots &  \cdots  \\
  a_{n1} & a_{n2} & a_{n3} & \cdots &  0       \\
\end{pmatrix} 
\end{aligned}$

$\begin{aligned}
U = \begin{pmatrix}
  0      & a_{12} & a_{12} & \cdots &  a_{1n}  \\
  0      & 0      & a_{23} & \cdots &  a_{2n}  \\
  0      & 0      & 0      & \cdots &  a_{2n}  \\
  \cdots & \cdots & \cdots & \cdots &  \cdots  \\
  0      & 0      & 0      & \cdots &  0       \\
\end{pmatrix} 
\end{aligned}$

Итерационный метод Якоби 

$\begin{aligned}
  B = D, \quad \tau_{k+1} = 1
\end{aligned}$

Итерационный метод Зейделя

$\begin{aligned}
  B = D + L,
  \quad \tau_{k+1} = 1
\end{aligned}$
    """    

if menu == "Некоторые более общие методы":
    r"""
##### Некоторые более общие методы 

Переменные итерационные параметры

$\begin{aligned}
  D \frac {y^{k+1} - y^k}{\tau_{k+1}} + A y^k = g,
  \quad k = 0,1,\ldots 
\end{aligned}$

$\begin{aligned}
  (D + L) \frac {y^{k+1} - y^k}{\tau_{k+1}} + A y^k = g,
  \quad k = 0,1,\ldots 
\end{aligned}$

Метод верхней релаксации

$\begin{aligned}
  (D + \tau L) \frac {y^{k+1} - y^k}{\tau} + A y^k = g,
  \quad k = 0,1,\ldots 
\end{aligned}$
    """  

    
