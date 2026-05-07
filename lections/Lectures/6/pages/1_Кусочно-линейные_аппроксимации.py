import streamlit as st
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np 
from scipy import integrate
 
menu = st.sidebar.radio('***',
    (
    "Задачи интерполяции", 
    "Базисные функции",
    "Кусочно-линейная интерполяция функции Рунге",
    "Приближение функций",
    "Кусочно-линейное приближение функции Рунге",
    )
)
  
if menu == "Задачи интерполяции":
    r"""
##### Задачи интерполяции

В узлах интерполирования $a = x_0 < x_1 < \ldots < x_n = b$
$\\ \quad$ заданы значения функции $f(x_i), \ i = 0,1,\ldots,n$

Интерполирующая функция $\varphi(x)$ 

$\begin{aligned}
  \varphi(x_i) = f(x_i),
  \quad i = 0,1,\ldots,n .
\end{aligned}$

Кусочно-линейная интерполяция
$\\ \quad$  $\varphi(x)$ - линейная функция на каждом интервале $[x_i,x_{i+1}], \  i=0,1,\ldots,n-1$

    """    
    
if menu == "Базисные функции":
    r"""
##### Базисные функции

Интерполирующая функция

$\begin{aligned}
  \varphi(x) = \sum_{i=0}^{n} c_k \varphi_k(x)
\end{aligned}$

Коэффициенты: $\quad c_k = f(x_k), \ k = 0,1,\ldots,n$
$\\ \quad$ при

$\begin{aligned}
 \varphi_k(x_i) = \left \{ 
 \begin{array}{ll}
   1, & i = k  \\
   0, & i \neq k \\
\end{array}
\right .
\end{aligned}$

Кусочно-линейные базисные функции

$\begin{aligned}
 \varphi_k(x) = \left \{ 
 \begin{array}{ll}
   0, & x \le x_{k-1}  \\
   h^{-1} (x-x_{k-1}), & x_{k-1} \le x \le x_{k}  \\
   h^{-1} (x_{k+1}-x), & x_{k} \le x \le x_{k+1}  \\   
   0, &  x \ge x_{k+1} \\
\end{array}
\right .
\end{aligned}$

$\\ \quad$ для равноотстоящих узлов интерполяции ($x_{i+1} - x_i = h$)

    """
    
if menu == "Кусочно-линейная интерполяция функции Рунге":
    r"""
##### Кусочно-линейная интерполяция функции Рунге

**Постановка задачи**

Кусочно-линейные интерполирование данных в равноотстоящих узлах для функции Рунге

$\begin{aligned}
 f(x) = \frac{1}{1 + 25 x^2}
\end{aligned}$

на интервале $[-1,1]$ при различном числе узлов интерполяции

    """
    tab1, tab2 = st.tabs([" **Кусочно-линейная интерполяция** ", " **Базисные функции** "])

    with tab1:
        def f(x):
            return 1./(1.+25*x**2)
        def pk(x, k, xi):
            h1 = 1/(xi[1]-xi[0])
            g = 0.
            if k == 0:
                if x < xi[1]:
                    g = h1*(xi[1]-x)
                return g
            if k == len(xi)-1:
                if x >xi[k-1]:
                    g = h1*(x-xi[k-1])
                return g
            if k > 0 and k < len(xi)-1:
                if x > xi[k-1] and x < xi[k]:
                    g = h1*(x-xi[k-1])
                if x >= xi[k] and x < xi[k+1]:
                    g = h1*(xi[k+1]-x)
                return g

        c1, cc, c2 = st.columns([5,1,5])
        c1.write("$~~$")
        c1.write("Количество узлов интеполирования")
        ni = c2.slider("n", 2,12, 8) + 1
        xi = np.linspace(-1.,1.,ni)
        yi = f(xi)
        y0 = np.zeros((ni), "float")
        N = 500
        xx = np.linspace(-1.,1.,N)
        yy = np.linspace(-1.,1.,N)
        fe = f(xx)

        for j in range(0, N):
            s = 0.
            for k in range(0, ni):
                s = s + yi[k]*pk(xx[j], k, xi)
            yy[j] = s

        fig2 = plt.figure(2)
        ss = "$n = $" + str(ni-1)
        plt.title(ss)
        plt.scatter(xi, y0)
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
        k = c2.slider("k", 0, ni-1, 0)

        yy1 = np.linspace(-1.,1.,N)
        for j in range(0, N):
            yy1[j] =  pk(xx[j], k, xi)

        fig1 = plt.figure(1)
        plt.scatter(xi, y0)
        ss = "$\\varphi_k(x), \ k = $" + str(k)
        plt.title(ss)
        plt.plot(xx,yy1)
        plt.xlabel('$x$')
        plt.grid(True)
        c1, c2, = st.columns([3,1])
        c1.pyplot(fig1)
    
if menu == "Приближение функций":
    r"""
##### Приближение функций

**Аппроксимация функции**

Приближение на всем отрезке $[a, b]$

$\begin{aligned}
 \varphi(x) \approx f(x),
 \quad a \leq x \leq b 
\end{aligned}$

Аппроксимирующая функция 

$\begin{aligned}
   \varphi(x) = \sum_{k=0}^{n} c_k \varphi_k(x) 
\end{aligned}$

$\varphi_k(x), \ k = 0,1,\ldots,n$ - кусочно-линейные базисные функции

**Метод Галеркина**

В гильбертовом пространстве $L_2(a,b)$ 

$\begin{aligned}
  (u,v) = \int_a^b u(x) v(x) dx,
  \quad \|u\| = \left ( \int_a^b |u(x)|^2 dx \right )^{1/2} 
\end{aligned}$

Скалярно домножим на  $ \varphi_l(x), \ l = 0, 1, \ldots, n$

$\begin{aligned}
 (\varphi, \varphi_l) = (f, \varphi_l) ,
 \quad l = 0, 1, \ldots, n
\end{aligned}$

Система линейных уравнений

$\begin{aligned}
  \sum_{k=0}^{n} c_k (\varphi_k,\varphi_l) = (f,\varphi_l),
  \quad l = 0,1,\ldots,n 
\end{aligned}$

Кусочно-линейные базисные функции

$\begin{aligned}
  (\varphi_k,\varphi_l) \neq 0,
  \quad l = k-1, \ k+1
\end{aligned}$

    """ 
    
if menu == "Кусочно-линейное приближение функции Рунге":
    r"""
##### Кусочно-линейное приближение функции Рунге

**Постановка задачи**

Выполнить кусочно-линейное приближение функции Рунге

$\begin{aligned}
 f(x) = \frac{1}{1 + 25 x^2}
\end{aligned}$

на интервале $[-1,1]$ при различном числе разбиений

    """

    tab1, tab2 = st.tabs([" **Кусочно-линейное приближение** ", " **Соседние базисные функции** "])

    with tab1:
        def f(x):
            return 1./(1.+25*x**2)
        def pk(x, k, xi):
            h1 = 1/(xi[1]-xi[0])
            g = 0.
            if k == 0:
                if x < xi[1]:
                    g = h1*(xi[1]-x)
                return g
            if k == len(xi)-1:
                if x >xi[k-1]:
                    g = h1*(x-xi[k-1])
                return g
            if k > 0 and k < len(xi)-1:
                if x > xi[k-1] and x < xi[k]:
                    g = h1*(x-xi[k-1])
                if x >= xi[k] and x < xi[k+1]:
                    g = h1*(xi[k+1]-x)
                return g

        c1, cc, c2 = st.columns([5,1,5])
        c1.write("$~~$")
        c1.write("Число разбиений")
        ni = c2.slider("n", 2, 12, 8) + 1

        xi = np.linspace(-1.,1.,ni)
        y0 = np.zeros((ni), "float")
        fk = np.zeros((ni), 'float')
        for k in range(0, ni):
            ff = lambda x : 1./(1.+25*x**2)*pk(x, k, xi)
            fk[k], err = integrate.quad(ff, -1, 1)


        A = np.zeros((ni,ni), 'float')
        for k in range(0, ni):
            kk0 = lambda x : pk(x, k, xi)*pk(x, k, xi)
            A[k,k], err = integrate.quad(kk0, -1, 1)
            if k > 0:
                kk1 = lambda x : pk(x, k, xi)*pk(x, k-1, xi)
                A[k,k-1], err = integrate.quad(kk1, -1, 1)
            if k < ni-1:
                kk2 = lambda x : pk(x, k, xi)*pk(x, k+1, xi)
                A[k,k+1], err = integrate.quad(kk2, -1, 1)

        ck =  np.linalg.solve(A, fk)

        N = 500
        xx = np.linspace(-1.,1.,N)
        yy = np.linspace(-1.,1.,N)
        fe = f(xx)

        for j in range(0, N):
            s = 0.
            for k in range(0, ni):
                s = s + ck[k]*pk(xx[j], k, xi)
            yy[j] = s

        fig2 = plt.figure(2)
        ss = "$n = $" + str(ni-1)
        plt.title(ss)
        plt.scatter(xi, y0)
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
        k = c2.slider("k", 0, ni-1, 0)

        fig1 = plt.figure(1)
        yy1 = np.linspace(-1.,1.,N)
        for j in range(0, N):
            yy1[j] =  pk(xx[j], k, xi)
        plt.plot(xx,yy1)
        if k > 0:
            for j in range(0, N):
                yy1[j] =  pk(xx[j], k-1, xi)
            plt.plot(xx,yy1)
        if k < ni-1:
            for j in range(0, N):
                yy1[j] =  pk(xx[j], k+1, xi)
            plt.plot(xx,yy1)

        plt.scatter(xi, y0)
        ss = "$\\varphi_{k-1}(x), \ \\varphi_k(x), \ \\varphi_{k+1}(x), \ k = $" + str(k)
        plt.title(ss)

        plt.xlabel('$x$')
        plt.grid(True)
        c1, c2, = st.columns([3,1])
        c1.pyplot(fig1)
