import streamlit as st
from PIL import Image
 
menu = st.sidebar.radio("***",
    ("FEniCS: сетки", 
    "FEniCS: конечные элементы", 
    "FEniCS: краевые условия",        
    "FEniCS: краевая задача",
    "FEniCS: дискретная задача",    
    "FEniCS: линейные решатели",
    "FEniCS: визуализация",   
    )
)
    
if menu == "FEniCS: сетки":
    r"""
##### FEniCS: сетки
* Типы сеток

  1D, 2D (треугольники), 3D (тетраэдры)
* Xml формат для сеток

  маркирование частей границы и подобластей
* Простые области

  встроенные элементы, простые редакторы областей 
  
* Модуль mshr

  2D и 3D из примитивов с поддержкой Constructive Solid Geometry
  
* Импорт из сторонних программ

  gmsh, netgen
  
**Пример**
    """
    code = """  
    # Область и сетка
    mesh = UnitSquareMesh(n, n)
    """ 
    st.code(code, language="python")     
    
      
if menu == "FEniCS: конечные элементы":
    r"""
##### FEniCS: конечные элементы
* Форма: симплекс - n-мерный тетраэдр, n = 1,2,3
* Непрерывные и разрывные лагранжевые конечные элементы
* Скалярные и векторные пространства
* Смешанные конечные элементы

**Пример**
    """
    code = """  
    # Функциональное пространство
    V = FunctionSpace(mesh, "Lagrange", 2)
    """ 
    st.code(code, language="python")       
    
if menu == "FEniCS: краевые условия":
    r""" 
##### FEniCS: краевые условия
* Смешанные граничные условия

  Выделение участков границы
* Задание главных краевых условий

  Выделение подпространства конечных элементов
* Естественные граничные условие

  Включение в вариационную формулировку
  
**Пример**
    """    
    code = """  
    # Часть границы
    class DirichletBoundary(SubDomain):
        def inside(self, x, on_boundary):
            return x[0] + x[1] > 1.0 - DOLFIN_EPS and on_boundary

    # Краевые условия Дирихле
    bc = DirichletBC(V, Constant(0.0), DirichletBoundary())
    """ 
    st.code(code, language="python")   
    
if menu == "FEniCS: краевая задача":
    r""" 
##### FEniCS: краевая задача
* Линейная задача

  $a(u,v) = L(v)$
* Нелинейная задача
  
  $F(u;v) = 0$
* Система уравнений
  
  $F(u;v) = F_1(u_1;v_1) + F_2(u_2;v_2) + ...$

**Пример**
    """    
    code = """  
    # Вариационная задача
    u = TrialFunction(V)
    v = TestFunction(V)
    f = interpolate(Expression("x[0]", degree=2), V)
    a = eps * inner(grad(u), grad(v)) * dx + u * v * dx
    L = f * v * dx
    """ 
    st.code(code, language="python")   
      
if menu == "FEniCS: дискретная задача":
    r"""
##### FEniCS: дискретная задача

* Автоматическая генерация дискретной задачи
* Решение систем уравнений

    + Линейная задача

      solve(a == L, u, …)

    + Нелинейная задача

      solve(F == 0, u, …)

      метод Ньютона (автоматическое дифференцирование)

**Пример**
    """    
    
    code = """  
    # Численное решение
    u_sol = Function(V)
    solve(a == L, u_sol, bc,
          solver_parameters={'linear_solver': 'mumps'})
    """ 
    st.code(code, language="python")       
      
if menu == "FEniCS: линейные решатели":
    r"""
##### FEniCS: линейные решатели
* Система линейных уравнений 

  $Ay = b$
* Прямой метод

  LU, SuperLU, UMFPACK
* Симметричная матрица
 
  cg - метод сопряженных градиентов
* Несимметричная матрица

  bicgstab, minres, gmres
* Переобуславливатели

  sor, icc, ilu, amg

    """
      
if menu == "FEniCS: визуализация":
    r"""
##### FEniCS: визуализация
* Встроенный визуализатор на базе matplotlib

  plot(mesh), plot(u)

* Экспорт для визуализации в ParaView

  формат pvd, скалярные и векторные поля, динамическая визуализация

**Пример**
    """

    code = """  
# График
plot(u_sol, title="Решение")
plt.savefig("gr2.png", format="png", dpi=300)
plt.clf()
    """ 
    st.code(code, language="python")       
