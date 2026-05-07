import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np 
from scipy.special import legendre
from scipy import integrate
 
menu = st.sidebar.radio('***',
    (
    "Постановка задачи", 
    "Наилучшее приближение", 
    "Метод Галеркина",     
    "Приближение полиномами",
    "Приближение функции Рунге",
    )
)
  
if menu == "Постановка задачи":
    r"""
##### Постановка задачи

Приближение на всем отрезке $[a, b]$

$\begin{aligned}
 \varphi(x) \approx f(x),
 \quad a \leq x \leq b 
\end{aligned}$

$H$ - вещественное гильбертово пространство 
$\\ \quad$ со скалярным
произведением $(u,v)$ и нормой $\|u\| = (u,u)^{1/2}$

Для $H = L_2(a,b)$ 

$\begin{aligned}
  (u,v) = \int_a^b u(x) v(x) dx,
  \quad \|u\| = \left ( \int_a^b |u(x)|^2 dx \right )^{1/2} 
\end{aligned}$

Аппроксимирующая функция 

$\begin{aligned}
   \varphi(x) = \sum_{k=0}^{n} c_k \varphi_k(x) ,
  \quad \varphi_i(x) \in H,
  \quad i = 0,1,\ldots,n
\end{aligned}$

Коэффициенты $c_k, \ k = 0, 1, \ldots, n$ 
$\\ \quad$ из минимума нормы погрешности аппроксимации

$\begin{aligned}
  \|f(x) - \sum_{k=0}^{n} c_k \varphi_k(x)\| 
  \rightarrow  \min
\end{aligned}$

    """ 
    
if menu == "Наилучшее приближение":
    r"""
##### Наилучшее приближение

**Метод наименьших квадратов**

$\begin{aligned}
  \min_c J(c), 
 \quad J(c) =  \|f(x) - \sum_{k=0}^{n} c_k \varphi_k(x)\|^2 
\end{aligned}$

Коэффициенты из решения
следующей системы линейных уравнений

$\begin{aligned}
  \sum_{k=0}^{n} c_k (\varphi_k,\varphi_i) = (f,\varphi_i),
  \quad i = 0,1,\ldots,n 
\end{aligned}$

**Идеальный выбор базисных функций**

$\begin{aligned}
 (\varphi_k, \varphi_i) = \left \{ 
 \begin{array}{ll}
   1, & i = k  \\
   0, & i \neq k \\
\end{array}
\right .
\end{aligned}$

В этом случае 

$\begin{aligned}
 c_k = \frac{1}{\|\varphi_k\|^2}(f, \varphi_k),
 \quad k = 0,1,\ldots,n 
\end{aligned}$

    """
    
if menu == "Метод Галеркина":
    r"""
##### Метод Галеркина

Приближенное решение уравнения

$\begin{aligned}
 \varphi(x) = f(x),
 \quad a \leq x \leq b 
\end{aligned}$

Скалярно домножим на  $ \varphi_i(x), \ i = 0, 1, \ldots, n$

$\begin{aligned}
 (\varphi, \varphi_i) = (f, \varphi_i) ,
 \quad i = 0, 1, \ldots, n
\end{aligned}$

Система линейных уравнений

$\begin{aligned}
  \sum_{k=0}^{n} c_k (\varphi_k,\varphi_i) = (f,\varphi_i),
  \quad i = 0,1,\ldots,n 
\end{aligned}$

    """
    
if menu == "Приближение полиномами":
    r"""
##### Приближение полиномами

Базисные функции

$\begin{aligned}
  \varphi_k(x) = x^k,
  \quad k = 0,1,\ldots,n
\end{aligned}$

Полиномы Лежандра $P_k(x)$ ортогональны на отрезке $[-1,1]$

$ P_0(x) = 1 $

$ P_1(x) = x $
 
$ P_2(x) = \frac12 (3x^2-2) $

$ ... $

Рекурентная формула

$\begin{aligned}
 (k+1) P_{k+1} (x) = (2 k+1) x P_{k} (x) - k P_{k-1}(x)
\end{aligned}$

    """
    
    
if menu == "Приближение функции Рунге":
    r"""
##### Приближение функции Рунге

**Постановка задачи**

Аппроксимировать полиномом функцию Рунге

$\begin{aligned}
 f(x) = \frac{1}{1 + 25 x^2}
\end{aligned}$

на интервале $[-1,1]$
    """
    
    f = lambda x : 1./(1.+25*x**2)

    tab1, tab2 = st.tabs([" **Полиномиальная аппроксимация** ", " **Базисные функции (полиномы Лежандра)** "])

    with tab1:
        c1, cc, c2 = st.columns([5,1,5])
        c1.write("$~~$")
        c1.write("Порядок полинома")
        ni = c2.slider("n", 2, 30, 8) + 1

        ck = np.zeros((ni), "float")
        for k in range(0, ni):
            pk = legendre(k)
            fk = lambda x : 1./(1.+25*x**2)*pk(x)
            ck[k], err = integrate.quad(fk, -1, 1)

        print(ck)

        N = 500
        xx = np.linspace(-1.,1.,N)
        yy = np.linspace(-1.,1.,N)
        fe = f(xx)

        for j in range(0, N):
            s = 0.
            for k in range(0, ni):
                pk = legendre(k)
                s = s + ck[k]*(2*k+1)*0.5*pk(xx[j])
            yy[j] = s


        fig2 = plt.figure(2)
        ss = "$n = $" + str(ni-1)
        plt.title(ss)
        plt.plot(xx, fe)
        plt.plot(xx, yy)
        plt.xlabel('$x$')
        plt.grid(True)
        c1, c2, = st.columns([3,1])
        c1.pyplot(fig2)

    with tab2:
        c1, cc, c2 = st.columns([5,1,5])
        c1.write("$~~$")
        c1.write("Номер базисной функции")
        k = c2.slider("k", 0, ni-1, ni-1)

        ri = legendre(k)
        fi = ri(xx)

        fig1 = plt.figure(1)
        ss = "$\\varphi_k(x), \ k = $" + str(k)
        plt.title(ss)
        plt.plot(xx, fi)
        plt.xlabel('$x$')
        plt.grid(True)
        c1, c2, = st.columns([3,1])
        c1.pyplot(fig1)
    
    

    
    
