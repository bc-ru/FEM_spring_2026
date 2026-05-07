import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np 
import scipy.interpolate as interpolate 
 
menu = st.sidebar.radio('***',
    (
    "Интерполяционный многочлен", 
    "Проблема коэффициентов", 
    "Интерполяционный многочлен Лагранжа",
    "Базисные функции",
    "Интерполяция функции Рунге",
    )
)
  
if menu == "Интерполяционный многочлен":
    r"""
##### Интерполяционный многочлен

Линейная аппроксимация

$\begin{aligned}
  \varphi(x) = \sum_{k=0}^{n} c_k \varphi_k(x)
\end{aligned}$

При аппроксимации полиномами используются функции

$\begin{aligned}
  \varphi_k(x) = x^k,
  \quad k = 0,1,\ldots,n
\end{aligned}$

Аппроксимирующая функция

$\begin{aligned}
  \varphi(x) = \sum_{k=0}^{n} c_k x^k
\end{aligned}$

Задача интерполяции

$\begin{aligned}
  \varphi(x_i) = f(x_i),
 \quad i = 0,1,\ldots,n 
\end{aligned}$

    """ 
    
if menu == "Проблема коэффициентов":
    r"""
##### Проблема коэффициентов

Задача для коэффициентов

$\begin{aligned}
  \sum_{k=0}^{n} c_k \varphi_k(x_i) = f(x_i),
 \quad i = 0,1,\ldots,n 
\end{aligned}$

Система линейных уравнений

$\begin{aligned}
  A c = f
\end{aligned}$

$A$ - плотная матрица без хороших свойств

**Решение проблемы**

Подбор базисных функций (полиномов степени $n$)

$\begin{aligned}
  \varphi_k(x), 
 \quad k = 0,1,\ldots,n   
\end{aligned}$

Идеал - без решения системы уравнений

    """
    
if menu == "Интерполяционный многочлен Лагранжа":
    r"""
##### Интерполяционный многочлен Лагранжа

Многочлен $\varphi(x)$ в форме

$\begin{aligned}
 \varphi(x) =  \sum_{k=0}^{n} f(x_k) \varphi_k(x) 
\end{aligned}$

Коэффициенты: $\quad c_k = f(x_k), \ k = 0,1,\ldots,n$

Условие интерполяции

$\begin{aligned}
 \sum_{k=0}^{n} f(x_k) \varphi_k(x_i)  = f(x_i),
 \quad i = 0,1,\ldots,n 
\end{aligned}$

будет выполнено при

$\begin{aligned}
 \varphi_k(x_i) = \left \{ 
 \begin{array}{ll}
   1, & i = k  \\
   0, & i \neq k \\
\end{array}
\right .
\end{aligned}$

    """
    
if menu == "Базисные функции":
    r"""
##### Базисные функции

Для выполнения $\varphi_k(x_i) = 0, \ i \neq k$ положим

$\begin{aligned}
 \varphi_k(x) = \mathrm{const} (x-x_0) (x-x_1) \cdots {\color{red} (x-x_{k-1})  (x-x_{k+1})} \cdots (x-x_{n})
\end{aligned}$

Из условия $\varphi_k(x_k) = 1$

$\begin{aligned}
  \varphi_k(x) = \frac{{\displaystyle \prod_{k\neq i=0}^{n} (x-x_i) } }{{\displaystyle \prod_{k\neq i=0}^{n} (x_k-x_i) } }
\end{aligned}$

    """
     
if menu == "Интерполяция функции Рунге":
    r"""
##### Интерполяция функции Рунге

**Постановка задачи**

Интерполирование данных в равноотстоящих узлах для функции Рунге

$\begin{aligned}
 f(x) = \frac{1}{1 + 25 x^2}
\end{aligned}$

на интервале $[-1,1]$ при различном числе узлов интерполяции
    """


    tab1, tab2 = st.tabs([" **Полиномиальная интерполяция** ", " **Базисные функции** "])

    with tab1:
        def f(x):
            return 1./(1.+25*x**2)

        c1, cc, c2 = st.columns([5,1,5])
        c1.write("$~~$")
        c1.write("Количество узлов интеполирования")
        ni = c2.slider("n", 2, 30, 8) + 1
        xi = np.linspace(-1.,1.,ni)
        yi = f(xi)
        y0 = np.zeros((ni), "float")
        N = 500
        xx = np.linspace(-1.,1.,N)

        r = interpolate.lagrange(xi, yi)
        ff = r(xx)
        fe = f(xx)
        fig2 = plt.figure(2)
        ss = "$n = $" + str(ni-1)
        plt.title(ss)
        plt.scatter(xi, y0)
        plt.plot(xx, fe)
        plt.plot(xx, ff)
        plt.xlabel('$x$')
        plt.grid(True)
        c1, c2, = st.columns([3,1])
        c1.pyplot(fig2)

    with tab2:
        c1, cc, c2 = st.columns([5,1,5])
        c1.write("$~~$")
        c1.write("Номер базисной функции")
        k = c2.slider("k", 0, ni-1, 0)

        phi = np.zeros((ni), "float")
        phi[k] = 1.
        ri = interpolate.lagrange(xi, phi)
        fi = ri(xx)

        fig1 = plt.figure(1)
        plt.scatter(xi, y0)

        ss = "$\\varphi_k(x), \ k = $" + str(k)
        plt.title(ss)
        plt.plot(xx, fi)
        plt.xlabel('$x$')
        plt.grid(True)
        c1, c2, = st.columns([3,1])
        c1.pyplot(fig1)

    

    
    
