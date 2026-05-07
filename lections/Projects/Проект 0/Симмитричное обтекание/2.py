from dolfin import *
import matplotlib.pyplot as plt
import numpy as np

# Загрузка сетки из файла .xml
mesh = Mesh("mesh/3.xml")
boundaries = MeshFunction("size_t", mesh, "mesh/3_facet_region.xml")

ds = Measure("ds", subdomain_data=boundaries)

# Информация о сетке 
n_c = mesh.num_cells()
n_v = mesh.num_vertices()
print(f"Число ячеек сетки: {n_c}")
print(f"Число узлов сетки: {n_v}")

# Условие на входе в канал
u_1 = Expression("x[1]", degree=2)

# Цикл по значениям p
for p in [1, 2, 3]:
    print(f"\nРасчет для p = {p}")

    # Определение функционального пространства
    V = FunctionSpace(mesh, "CG", p)

    # Число искомых величин
    n_d = V.dim()

    print(f"Число искомых дискретных значений: {n_d}")
        
    # Граничные условия
    bcs = [DirichletBC(V, Constant(0.0), boundaries, 1),
           DirichletBC(V, Constant(1.0), boundaries, 2),
           DirichletBC(V, Constant(0.5), boundaries, 5),
           DirichletBC(V, u_1, boundaries, 3)]

    # Вариационная задача
    u = TrialFunction(V)
    v = TestFunction(V)
    f = Constant(0.0)  
    a = dot(grad(u), grad(v)) * dx
    L = f * v * dx

    # Решение задачи
    u = Function(V)
    solve(a == L, u, bcs)

    # Вычисление циркуляции
    n = FacetNormal(mesh)  
    u_n = dot(grad(u), n)  
    Gamma = assemble(u_n * ds(subdomain_data=boundaries, subdomain_id=5))
    print(f"Циркуляция: {Gamma:.5e}")

