import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Тестовая задача", 
    "Численное решение (прямой решатель)",     
    "Итерационные решатели (FEniCS)",     
    "Задачи диффузии", 
    "Задачи диффузии-конвекции", 
    )
)

if menu == "Тестовая задача":
    r"""
##### Тестовая задача

**Область**

$\Omega = \{ \bm x \ | \ \bm x = (x_1, x_2), \ 0 < x_1 < 1, \ 0 < x_2 < 1\} $

**Уравнение**

$\begin{aligned} - 
 \operatorname{div} \operatorname{grad} u + \bm c \cdot   \operatorname{grad} u = 0 ,
 \quad \bm x \in \Omega
\end{aligned}$

с постоянным вектором $\bm c = \{c, c\}$

**Граничные условия**

$\begin{aligned}
  u(\bm x) = x_1 x_2,
  \quad \bm x \in \partial\Omega
\end{aligned}$

    """    
    
if menu == "Численное решение (прямой решатель)":
    r"""
##### Численное решение (прямой решатель)

Влияние шага сетки

    """
    import matplotlib.pyplot as plt
    import numpy as np 
    from fenics import *
    from scipy.sparse import csr_matrix
    from scipy.sparse.linalg import spsolve
    import pandas as pd
    import time
    time.clock = time.time
    
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Число ячеек $m$")        
    m = c2.slider("", 10, 500, 50, 10)
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Порядок полинома $p$")        
    p = c2.slider("", 1, 3, 1)  
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Коэффициент $c$")        
    c = c2.slider("", -0, 100, 10, 1)   
    
    dataList = []
    
    for kk in range(0, 3): 
    
        mesh = UnitSquareMesh(m, m)
        xm = mesh.coordinates()
        ym = np.zeros((m+1), "float") 
        
        V = FunctionSpace(mesh, "CG", p)
        n = V.dim()-1
        
        u = TrialFunction(V)
        v = TestFunction(V)
        
        def boundary(x, on_boundary):
            return on_boundary
        bc = DirichletBC(V, Expression("x[0]*x[1]", degree=p+2), boundary)
        
        f = Expression("0.", degree=p+2)
        cc = Constant([c,c])
        a = dot(grad(u), grad(v))*dx + dot(cc,grad(u))*v*dx
        L = f*v*dx 
        
        start_time = time.clock()
        w = Function(V)
        solve(a == L, w, bc)
        ts = time.clock() - start_time
        dic = {"Шаг сетки": 1./m, "Число неизвестных": n, "Время (с)": ts}
        dataList.append(dic)
        m2 = m
        m = m*2  

    tab1, tab2 = st.tabs([" **Время решения** ", " **Решение** "])

    with tab1:
        df = pd.DataFrame(dataList)
        st.table(df)

    with tab2:
        N = 200
        x = np.linspace(0,1,N)
        y = np.linspace(0,1,N)
        yy  = np.zeros((N,N))
        ye  = np.zeros((N,N))
        tk = np.linspace(0,1,m+1)

        for i in range(0, N):
            for j in range(0, N):
                pp = Point(x[i],y[j])
                yy[j,i] = w(pp)

        fig2 = plt.figure(2)
        ss = "$m = $" + str(m2) + "$, \ p = $" + str(p) + "$, \ c = $" + str(c)
        plt.title(ss)
        plt.contourf(x,y,yy)
        plt.gca().set_aspect("equal")
        plt.colorbar()

        c1, c2, = st.columns([3,1])
        c1.pyplot(fig2)
      
if menu == "Итерационные решатели (FEniCS)":
    r"""
##### Итерационные решатели (FEniCS)

Итерационный метод (выбор итерационных параметров)

* метод сопряженных градиентов для симметричных матриц

  FEniCS (linear_solver): cg $~-~$ conjugate gradient method 
  
* метод минимальных поправок для несимметричных матриц

  FEniCS (linear_solver): gmres $~-~$ generalized minimal residual method 
  
Переобуславливатель (выбор $B$)

* метод Якоби

  $B = D$, $\ D ~-~$  диагональная часть $A$

  FEniCS (preconditioner): jacobi  
  
* неполное $L U$ разложение

  $A = L U$, $\ B = \widetilde{L} \, \widetilde{U} ~-~$ вычисление элементов только вблизи главной диагонали

  FEniCS (preconditioner): ilu  
   
**Фрагмент кода**
    """    
    
    code = """  
solve(a == L, w, bc, solver_parameters={'linear_solver': 'gmres',
                                        'preconditioner': 'ilu'})   
    """     
    st.code(code, language="python")       
    
if menu == "Задачи диффузии":
    r"""
##### Задачи диффузии

Коэффициент $c = 0 ~-~$ симметричная матрица

    """

    import matplotlib.pyplot as plt
    import numpy as np 
    from fenics import *
    from scipy.sparse import csr_matrix
    from scipy.sparse.linalg import spsolve
    import pandas as pd
    import time
    time.clock = time.time
    
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Число ячеек $m$")        
    m = c2.slider("", 10, 500, 50, 10)
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Порядок полинома $p$")        
    p = c2.slider("", 1, 3, 1)  
    c = 0  
    
    dataList = []
    
    for kk in range(0, 3): 
    
        mesh = UnitSquareMesh(m, m)
        xm = mesh.coordinates()
        ym = np.zeros((m+1), "float") 
        
        V = FunctionSpace(mesh, "CG", p)
        n = V.dim()-1
        
        u = TrialFunction(V)
        v = TestFunction(V)
        
        def boundary(x, on_boundary):
            return on_boundary
        bc = DirichletBC(V, Expression("x[0]*x[1]", degree=p+2), boundary)
        
        f = Expression("0.", degree=p+2)
        cc = Constant([c,c])
        a = dot(grad(u), grad(v))*dx + dot(cc,grad(u))*v*dx
        L = f*v*dx 
        
        start_time = time.clock()
        w = Function(V)
        solve(a == L, w, bc, solver_parameters={'linear_solver': 'cg',
                             'preconditioner': 'ilu'})   
        ts = time.clock() - start_time    
        start_time = time.clock()
        w1 = Function(V)
        solve(a == L, w1, bc, solver_parameters={'linear_solver': 'gmres',
                             'preconditioner': 'ilu'})   
        ts1 = time.clock() - start_time        
        
        dic = {"Шаг сетки": 1./m, "Число неизвестных": n, 
               "Метод": "gmres", "Время (с)": ts1}
        dic1 = {"Шаг сетки": 1./m, "Число неизвестных": n, 
               "Метод": "cg", "Время (с)": ts}    
        dataList.append(dic1) 
        dataList.append(dic)
        m2 = m
        m = m*2

    tab1, tab2 = st.tabs([" **Решение** ", " **Время решения** "])

    with tab1:
        N = 200
        x = np.linspace(0,1,N)
        y = np.linspace(0,1,N)
        yy  = np.zeros((N,N))
        ye  = np.zeros((N,N))
        tk = np.linspace(0,1,m+1)

        for i in range(0, N):
            for j in range(0, N):
                pp = Point(x[i],y[j])
                yy[j,i] = w(pp)

        fig2 = plt.figure(2)
        ss = "$m = $" + str(m2) + "$, \ p = $" + str(p) + "$, \ c = $" + str(c)
        plt.title(ss)
        plt.contourf(x,y,yy)
        plt.gca().set_aspect("equal")
        plt.colorbar()

        c1, c2, = st.columns([3,1])
        c1.pyplot(fig2)

    with tab2:
        df = pd.DataFrame(dataList)

        st.table(df)
    
    
if menu == "Задачи диффузии-конвекции":
    r"""
##### Задачи диффузии-конвекции

Несимметричная матрица ($c \neq 0$)

    """

    import matplotlib.pyplot as plt
    import numpy as np 
    from fenics import *
    from scipy.sparse import csr_matrix
    from scipy.sparse.linalg import spsolve
    import pandas as pd
    import time
    time.clock = time.time
    
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Число ячеек $m$")        
    m = c2.slider("", 10, 500, 50, 10)
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Порядок полинома $p$")        
    p = c2.slider("", 1, 3, 1)  
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Коэффициент $c$")        
    c = c2.slider("", -10, 10, 1, 1)  
    
    dataList = []
    
    for kk in range(0, 3): 
    
        mesh = UnitSquareMesh(m, m)
        xm = mesh.coordinates()
        ym = np.zeros((m+1), "float") 
        
        V = FunctionSpace(mesh, "CG", p)
        n = V.dim()-1
        
        u = TrialFunction(V)
        v = TestFunction(V)
        
        def boundary(x, on_boundary):
            return on_boundary
        bc = DirichletBC(V, Expression("x[0]*x[1]", degree=p+2), boundary)
        
        f = Expression("0.", degree=p+2)
        cc = Constant([c,c])
        a = dot(grad(u), grad(v))*dx + dot(cc,grad(u))*v*dx
        L = f*v*dx 
        
        start_time = time.clock()
        w = Function(V)
        solve(a == L, w, bc, solver_parameters={'linear_solver': 'gmres',
                             'preconditioner': 'jacobi'})   
        ts = time.clock() - start_time    
        start_time = time.clock()
        w1 = Function(V)
        solve(a == L, w1, bc, solver_parameters={'linear_solver': 'gmres',
                             'preconditioner': 'ilu'})   
        ts1 = time.clock() - start_time        
        
        dic = {"Шаг сетки": 1./m, "Число неизвестных": n, 
               "Переобуславливатель": "jacobi", "Время (с)": ts}
        dic1 = {"Шаг сетки": 1./m, "Число неизвестных": n, 
               "Переобуславливатель": "ilu", "Время (с)": ts1}
        dataList.append(dic)
        dataList.append(dic1)
        m2 = m
        m = m*2

    tab1, tab2 = st.tabs([" **Решение** ", " **Время решения** "])

    with tab1:
        N = 200
        x = np.linspace(0,1,N)
        y = np.linspace(0,1,N)
        yy  = np.zeros((N,N))
        ye  = np.zeros((N,N))
        tk = np.linspace(0,1,m+1)

        for i in range(0, N):
            for j in range(0, N):
                pp = Point(x[i],y[j])
                yy[j,i] = w(pp)

        fig2 = plt.figure(2)
        ss = "$m = $" + str(m2) + "$, \ p = $" + str(p) + "$, \ c = $" + str(c)
        plt.title(ss)
        plt.contourf(x,y,yy)
        plt.gca().set_aspect("equal")
        plt.colorbar()

        c1, c2, = st.columns([3,1])
        c1.pyplot(fig2)

    with tab2:
        df = pd.DataFrame(dataList)

        st.table(df)
    

