from dolfin import *
import matplotlib.pyplot as plt
import numpy as np

# Загрузка сетки из файла .xml
mesh = Mesh("mesh/1.xml")
boundaries = MeshFunction("size_t", mesh, "mesh/1_facet_region.xml")

ds = Measure("ds", subdomain_data=boundaries)

# Определение функционального пространства
V = FunctionSpace(mesh, "CG", 2)

# Информации о сетке и числе искомых величин
n_c = mesh.num_cells()
n_v = mesh.num_vertices()
n_d = V.dim()

print(f"Число ячеек сетки: {n_c}")
print(f"Число узлов сетки: {n_v}")
print(f"Число искомых дискретных значений: {n_d}")

# Условие на входе в канал
u_1 = Expression("x[1]", degree=2)

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

#  Циркуляция 
n = FacetNormal(mesh)  
u_n = dot(grad(u), n)  
Gamma = assemble(u_n * ds(subdomain_data=boundaries, subdomain_id=5))
print(f"Циркуляция: {Gamma:.5e}")


# Создание сетки для визуализации
coordinates = mesh.coordinates()
x = coordinates[:, 0]
y = coordinates[:, 1]
triangles = mesh.cells()

# Значения решения в узлах сетки
u_values = u.compute_vertex_values(mesh)

plt.figure(figsize=(12, 6)) # задаем размеры графика

# Контурный график с ограничением диапазона от 0 до 1
contour = plt.tricontourf(x, y, triangles, u_values, levels=50, cmap='winter', vmin=0, vmax=1)

# Изолинии через равные промежутки
isolines = plt.tricontour(x, y, triangles, u_values, levels=np.linspace(0, 1, 41), colors='white', linewidths=0.5)

# Отображение графика
plt.savefig('1.png', format="png", dpi=600)
plt.show()