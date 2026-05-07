import streamlit as st
 
menu = st.sidebar.radio('***',
    (
    "Тестовая задача", 
    "Точное решение",    
    "Ключевые фрагменты кода",         
    "Численное решение", 
    )
)

if menu == "Тестовая задача":
    r"""
##### Тестовая задача

**Область**

$\Omega = \{ x \ | \  0 < x < 1 \} $

**Уравнение**

$\begin{aligned} 
 \frac{\partial u}{\partial t} - \frac{\partial^2 u}{\partial x^2} = f(x,t) ,
 \quad x \in \Omega, 
 \quad 0 < t \leq T  
\end{aligned}$

**Граничные условия**

$\begin{aligned}
  u(0,t) = \mu_1(t),
  \quad u(1,t) = \mu_2(t),
 \quad 0 < t \leq T 
\end{aligned}$

**Начальное условие**

$\begin{aligned}
  u(x,0) = u^0(x),
 \quad x \in \Omega
\end{aligned}$

    """    
      
if menu == "Точное решение":
    r"""
##### Точное решение
    """

    tab1, tab2 = st.tabs([" **Аналитическое представление** " , " **Визуализация** "])

    with tab1:
        r"""
    Тестирование для
    
    $\begin{aligned}
    u_e(x,t) = \exp\Big (- \frac{(x-v t)^2}{d^2} \Big )
    \end{aligned}$ 
    
    Числовые параметры
    
    $\begin{aligned}
    v, \ d, \ T = \frac{1}{v}
    \end{aligned}$ 
    
    Граничные и начальные условия 
    
    $\begin{aligned}
      u(0,t) = u_e(0,t),
      \quad u(1,t) = u_e(1,t),
     \quad 0 < t \leq T 
    \end{aligned}$
    
    $\begin{aligned}
      u(x,0) = u_e(x,0),
     \quad x \in \Omega
    \end{aligned}$
    
    Правая часть
    
    $\begin{aligned} 
     f(x,t) = \frac{\partial u_e}{\partial t} - \frac{\partial^2 u_e}{\partial x^2} ,
     \quad x \in \Omega, 
     \quad 0 < t \leq T  
    \end{aligned}$
        """
    with tab2:

        import matplotlib.pyplot as plt
        import numpy as np
        from fenics import *

        c1, cc, c2 = st.columns([5,1,5])
        c1.write("$~~$")
        c1.write("Параметр $v$")
        vp = c2.slider("", 0.1, 10., 1., 0.1)
        c1, cc, c2 = st.columns([5,1,5])
        c1.write("$~~$")
        c1.write("Параметр $d$")
        dp = c2.slider("", 0.1, 1.,0.25, 0.1)

        c1, cc, c2 = st.columns([5,1,5])
        c1.write("$~~$")
        c1.write("Время $t$")

        T = 1./vp
        tv = 0.01*T
        tt = c2.slider("", 0., T, 0., tv)

        def ue(x,t):
            return exp(-(x-vp*t)**2/dp**2)

        def f(x,t):
            return 2/dp**2*exp(-(x-vp*t)**2/dp**2)*(vp*(x-vp*t)+1-2/dp**2*(x-vp*t)**2)

        N = 100
        xx = np.linspace(0., 1., N)
        yy = np.linspace(0., 1., N)

        fig1 = plt.figure(1, figsize=(8,2))

        for i in range(0, N):
            yy[i]  = ue(xx[i],tt)
        s = "Точное решение:  $t = $" + str(tt)
        plt.title(s)
        plt.plot(xx, yy)
        plt.xlabel('$x$')
        plt.grid(True)
        st.pyplot(fig1)

        fig2 = plt.figure(2, figsize=(8,2))

        for i in range(0, N):
            yy[i]  = f(xx[i],tt)
        s = "Правая часть:  $t = $" + str(tt)
        plt.title(s)
        plt.plot(xx, yy)
        plt.xlabel('$x$')
        plt.grid(True)
        st.pyplot(fig2)
    
if menu == "Ключевые фрагменты кода":
    r"""
##### Ключевые фрагменты кода

**Правая часть и граничное условие**
    """    
    code = """  
t = t + tau

f = Expression("2/pow(dp,2)*exp(-pow(x[0]-vp*t, 2) / pow(dp, 2))*(vp*(x[0]-vp*t)+1-2/pow(dp,2)*pow(x[0]-vp*t,2))", degree=p+2, vp=vp, dp=dp, t=t)
bc = DirichletBC(V, Expression("exp(-pow(x[0]-vp*t, 2) / pow(dp, 2))", degree=p+2, vp=vp, dp=dp, t=t), "on_boundary")

    """ 
    st.code(code, language="python")   
    r"""       
**Решение на новом слое по времени**
    """    
    code = """  
a = u*v*dx + sig*tau*dot(grad(u), grad(v))*dx 
сс = Constant((1.-sig)*tau)
L = y1*v*dx + tau*f*v*dx - сс*dot(grad(y1), grad(v))*dx 
solve(a == L, y, bc)
y1.assign(y)
    """ 
    st.code(code, language="python")   

    r"""        
**Расчет погрешности**
    """    
    code = """  
ue = project(Expression("exp(-pow(x[0]-vp*t, 2) / pow(dp, 2))", degree=p+2, vp=vp, dp=dp, t=t),V)
ern = assemble((y - ue) ** 2 * dx) ** 0.5
    """ 
    st.code(code, language="python")    
      
if menu == "Численное решение":
    r"""
##### Численное решение

**Точное решение**
    """

    import matplotlib.pyplot as plt
    import numpy as np 
    from fenics import *
    
    c1, cc, c2, cc, c3, cc, c4 = st.columns([5,1,5,1,5,1,5])
    c1.write("$~~$")
    c1.write("Параметр $v$")        
    vp = c2.slider("", 0.1, 10., 1., 0.1)
    c3.write("$~~$")
    c3.write("Параметр $d$")
    dp = c4.slider("", 0.1, 1.,0.25, 0.1)

    r"""
**Расчетные параметры**
    """

    c1, cc, c2, cc, c3, cc, c4 = st.columns([5,1,5,1,5,1,5])
    c1.write("$~~$")
    c1.write("Число ячеек $m$")
    m = c2.slider("", 10, 50, 20, 1)
    c3.write("$~~$")
    c3.write("Порядок полинома $p$")
    p = c4.slider("", 1, 3, 1)

    c1, cc, c2, cc, c3, cc, c4 = st.columns([5,1,5,1,5,1,5])
    c1.write("$~~$")
    c1.write("Число временных шагов $N$")        
    N = c2.slider("", 10, 100, 50, 1)
    c3.write("$~~$")
    c3.write("Весовой параметр $\sigma$")
    sig = c4.slider("", 0., 1., 0.5, 0.01)
    
    T = 1./vp 
    tau = T/N
        
    mesh = IntervalMesh(m, 0, 1)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    V = FunctionSpace(mesh, "CG", p)
    n = V.dim()-1
    
    u = TrialFunction(V)
    v = TestFunction(V)
    
    t = 0. 
    y1 = project(Expression("exp(-pow(x[0]-vp*t, 2) / pow(dp, 2))", degree=p+2, vp=vp, dp=dp, t=t),V)
    
    y = Function(V)
    ue = Function(V)
    tt = [0.]
    ut = [0.]
    er = [0.]
    for n in range(N):
        t = t + tau
        ts = sig*t + (1-sig)*(t-tau)
    
        f = Expression("2/pow(dp,2)*exp(-pow(x[0]-vp*t, 2) / pow(dp, 2))*(vp*(x[0]-vp*t)+1-2/pow(dp,2)*pow(x[0]-vp*t,2))", degree=p+2, vp=vp, dp=dp, t=ts)
        bc = DirichletBC(V, Expression("exp(-pow(x[0]-vp*t, 2) / pow(dp, 2))", degree=p+2, vp=vp, dp=dp, t=t), "on_boundary")
        
        a = u*v*dx + sig*tau*dot(grad(u), grad(v))*dx 
        L = y1*v*dx + tau*f*v*dx - Constant((1.-sig)*tau)*dot(grad(y1), grad(v))*dx 
        solve(a == L, y, bc)
        y1.assign(y)
        
        tt.append(t)
        ue = project(Expression("exp(-pow(x[0]-vp*t, 2) / pow(dp, 2))", degree=p+2, vp=vp, dp=dp, t=t),V)
        ut.append(y.vector()-ue.vector())    
        ern = assemble((y - ue) ** 2 * dx) ** 0.5
        er.append(ern)
    
    
    fig1 = plt.figure(1, figsize=(8,2))
        
    s = "Норма погрешностиt: $\\sigma = $" + str(sig)
    plt.title(s)
    plt.plot(tt, er) 
    plt.xlabel('$t$') 
    # plt.ylabel('$\\varepsilon$') 
    plt.grid(True)        
    st.pyplot(fig1)     
    
    c1, cc, c2 = st.columns([5,1,5])
    c1.write("$~~$")
    c1.write("Номер слоя по времени $n$")  
    n = c2.slider("", 0, N, 0)  
    y.vector()[:] = ut[n]
    
    N = 100
    xx = np.linspace(0., 1., N) 
    yy = np.linspace(0., 1., N)  
    
    fig2 = plt.figure(2, figsize=(8,2))
        
    for i in range(0, N): 
        yy[i]  = y(xx[i])
    s = "Погрешность при $t^n, \ n = $" + str(n)
    plt.title(s)
    plt.plot(xx, yy) 
    plt.xlabel('$x$') 
    plt.grid(True)      
    st.pyplot(fig2)  































