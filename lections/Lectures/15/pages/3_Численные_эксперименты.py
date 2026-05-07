import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Тестовая задача", 
    "Формирование матриц (FEniCS)",    
    "Решение спектральных задач (SLEPc)",  
    "Ключевые фрагменты кода",       
    "Параметрическое исследование", 
    )
)

if menu == "Тестовая задача":
    r"""
##### Тестовая задача

**Область**

$\Omega = \{ \bm x \ | \ \bm x = (x_1, x_2), \ 0 < x_1 < 1, \ 0 < x_2 < 1\} $

**Оператор**

$\begin{aligned} 
 \mathcal{A} = - 
 \operatorname{div} \operatorname{grad} u + \bm c \cdot   \operatorname{grad} u ,
 \quad \bm x = (x_1, x_2) \in \Omega
\end{aligned}$

с постоянным вектором $\bm c = \{c, c\}$

для функций

$\begin{aligned}
  \frac{\partial u}{\partial n} (\bm x) = 0,
  \quad \bm x \in \partial\Omega
\end{aligned}$

**Задачи**

* диффузии ($c = 0$)
* конвекции-диффузии ($c \ne 0$)

    """    
      
if menu == "Формирование матриц (FEniCS)":
    r"""
##### Формирование матриц (FEniCS)

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
      
if menu == "Решение спектральных задач (SLEPc)":
    r"""
##### Решение спектральных задач (SLEPc)

Библиотека SLEPc
* вычисления собственных значений и собственных векторов больших разреженных матриц
* симметричные и несимметричные матрицы
* частичная и полная проблема собственных значений
* различные алгоритмы
* поддержка параллельных вычислений
* как модуль PETSc (вызов из FEniCS)

    """    

if menu == "Ключевые фрагменты кода":
    r"""
##### Ключевые фрагменты кода

**Билинейные формы**
    """    
    code = """  
cc = Constant([c,c])
a = dot(grad(u), grad(v))*dx + dot(cc,grad(u))*v*dx
b = u*v*dx
    """ 
    st.code(code, language="python")   
    r"""       
**Формирование матриц**
    """    
    code = """  
A = PETScMatrix()
assemble(a, tensor=A)
B = PETScMatrix()
assemble(b, tensor=B)
    """ 
    st.code(code, language="python")   

    r"""        
**Решение спектральной задачи**
    """    
    code = """  
eigensolver = SLEPcEigenSolver(A,B)
eigensolver.parameters["spectrum"] = "smallest magnitude"
eigensolver.solve(kmax)

for k in range(0, kmax): 
    r, c, rx, cx = eigensolver.get_eigenpair(k)
    ur = Function(V)
    ur.vector()[:] = rx
    ui = Function(V)
    ui.vector()[:] = cx   
    """ 
    st.code(code, language="python") 
    
if menu == "Параметрическое исследование":
    r"""
##### Параметрическое исследование

Конечно-элементная задача
    """
    import matplotlib.pyplot as plt
    import numpy as np 
    from fenics import *
    import pandas as pd
    
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Число ячеек $m$")        
    m = c2.slider("", 10, 50, 20, 10)
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Порядок полинома $p$")        
    p = c2.slider("", 1, 3, 1)  
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Коэффициент $c$")        
    c = c2.slider("", -100, 100, 0, 10)  

    tab1, tab2 = st.tabs([" **Собственные значения** " , " **Собственные функции** "])

    with tab1:
        kmax = 10

        mesh = UnitSquareMesh(m, m)
        xm = mesh.coordinates()
        ym = np.zeros((m+1), "float")

        V = FunctionSpace(mesh, "CG", p)
        n = V.dim()-1

        u = TrialFunction(V)
        v = TestFunction(V)

        cc = Constant([c,c])
        a = dot(grad(u), grad(v))*dx + dot(cc,grad(u))*v*dx
        b = u*v*dx

        # Assemble stiffness form
        A = PETScMatrix()
        assemble(a, tensor=A)
        B = PETScMatrix()
        assemble(b, tensor=B)

        # Create eigensolver
        eigensolver = SLEPcEigenSolver(A,B)
        eigensolver.parameters["spectrum"] = "smallest magnitude"
        # eigensolver.parameters["tolerance"] = 1e-15      # Толерантность EPS
        # eigensolver.parameters["maximum_iterations"] = 50000  # Макс. итераций
        eigensolver.solve(kmax)

        dataList = []
        for k in range(0, kmax):
            r, c, rx, cx = eigensolver.get_eigenpair(k)

            dic = {"Номер собственного значения": k+1, "Действительная часть": r,
                   "Мнимая часть": c}
            dataList.append(dic)
            print(dic)

        df = pd.DataFrame(dataList)
        st.table(df)

    with tab2:
        c1, cc, c2 = st.columns([5,1,5])
        c1.write("$~~$")
        c1.write("Номер собственного значения $k$")
        kk = c2.slider("", 1, kmax, 1, 1)

        r, c, rx, cx = eigensolver.get_eigenpair(kk-1)
        ur = Function(V)
        ur.vector()[:] = rx
        ui = Function(V)
        ui.vector()[:] = cx

        N = 100
        x = np.linspace(0,1.,N)
        y = np.linspace(0,1.,N)
        yy  = np.zeros((N,N))

        for i in range(0, N):
            for j in range(0, N):
                pp = Point(x[i],y[j])
                yy[j,i] = ur(pp)

        fig1 = plt.figure(1)
        plt.contourf(x,y,yy)
        plt.gca().set_aspect("equal")
        plt.colorbar()

        for i in range(0, N):
            for j in range(0, N):
                pp = Point(x[i],y[j])
                yy[j,i] = ui(pp)

        fig2 = plt.figure(2)
        plt.contourf(x,y,yy)
        plt.gca().set_aspect("equal")
        plt.colorbar()

        c1, cc, c2 = st.columns([5,1,5])
        c1.write("Действительная часть")
        c2.write("Мнимая часть")
        c1.pyplot(fig1)
        c2.pyplot(fig2)































