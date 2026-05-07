from dolfin import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Вращающийся цилиндр
Gamma = 1.0

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
n = FacetNormal(mesh)  

print(f"Число ячеек сетки: {n_c}")
print(f"Число узлов сетки: {n_v}")
print(f"Число искомых дискретных значений: {n_d}")

# Условие на входе в канал
u_1 = Expression("x[1]", degree=2)

# Пробная и тестовая функции
u = TrialFunction(V)
v = TestFunction(V)
f = Constant(0.0)  

# Создание сетки для визуализации
coordinates = mesh.coordinates()
x = coordinates[:, 0]
y = coordinates[:, 1]
triangles = mesh.cells()

# Решение первой вспомогательной задачи

# Граничные условия
bcs1 = [DirichletBC(V, Constant(0.0), boundaries, 1),
       DirichletBC(V, Constant(1.0), boundaries, 2),
       DirichletBC(V, Constant(0.0), boundaries, 5),
       DirichletBC(V, u_1, boundaries, 3)]

# Вариационная задача
a = dot(grad(u), grad(v)) * dx
L = f * v * dx

# Решение задачи
u1 = Function(V)
solve(a == L, u1, bcs1)

#  Циркуляция u1
u_n = dot(grad(u1), n)  
circ1 = assemble(u_n * ds(subdomain_data=boundaries, subdomain_id=5))
print(f"Циркуляция поля u1: {circ1:.5e}")

# Решение второй вспомогательной задачи

# Граничные условия
bcs2 = [DirichletBC(V, Constant(0.0), boundaries, 1),
       DirichletBC(V, Constant(0.0), boundaries, 2),
       DirichletBC(V, Constant(1.0), boundaries, 5),
       DirichletBC(V, Constant(0.0), boundaries, 3)]

# Вариационная задача
a = dot(grad(u), grad(v)) * dx
L = f * v * dx

# Решение задачи
u2 = Function(V)
solve(a == L, u2, bcs2)

#  Циркуляция u2
u_n = dot(grad(u2), n)  
circ2 = assemble(u_n * ds(subdomain_data=boundaries, subdomain_id=5))
print(f"Циркуляция поля u2: {circ2:.5e}")

# Параметр взвешивания
kappa = (Gamma - circ1)/circ2
print(f"Параметр взвешивания: {kappa:.5e}")

# Решение задачи

# Значения решения в узлах сетки
u_values = u1.compute_vertex_values(mesh) + kappa*u2.compute_vertex_values(mesh)

plt.figure(figsize=(12, 6)) # задаем размеры графика

# Контурный график с ограничением диапазона от 0 до 1
contour = plt.tricontourf(x, y, triangles, u_values, levels=50, cmap='winter', vmin=0, vmax=1)

# Изолинии через равные промежутки
isolines = plt.tricontour(x, y, triangles, u_values, levels=np.linspace(0, 1, 41), colors='white', linewidths=0.5)

# Круговая стрелка
ax = plt.gca()
arc = patches.Arc([0.75,0.5],0.2,0.2,0,0,250,color='black')
ax.add_patch(arc)
endX=0.75+0.1*np.cos(np.radians(250)) #Do trig to determine end position
endY=0.5+0.1*np.sin(np.radians(250))
ax.add_patch(patches.RegularPolygon((endX, endY),3, 0.2/9, np.radians(250),color='black'))

# Отображение графика
plt.savefig('c-3.png', format="png", dpi=600)
plt.show()









