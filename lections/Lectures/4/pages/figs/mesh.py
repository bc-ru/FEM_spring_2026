from fenics import *
import numpy as np
import matplotlib.pyplot as plt

# Исходная сетка (gr1.png)

n1 = 7
n2 = 5
mesh = UnitSquareMesh(n1, n2)

plot(mesh)
plt.savefig("gr1.png", format="png", dpi=200)
plt.clf()

# алгебраическая трансформация  (gr2.png)

th1 = mesh.coordinates()[:, 0]
mesh.coordinates()[:, 0] = 2*th1**2

plot(mesh)
plt.savefig("gr2.png", format="png", dpi=200)
plt.clf()

# циндрические координаты (gr3.png)

mesh = UnitSquareMesh(n1, n2)
th1 = mesh.coordinates()[:, 0]
th2 = mesh.coordinates()[:, 1]

rho = 1 + th1
s1 = np.cos(0.5*np.pi*th2)
s2 = np.sin(0.5*np.pi*th2)
mesh.coordinates()[:, 0] = rho*s1
mesh.coordinates()[:, 1] = rho*s2
plot(mesh)
plt.savefig("gr3.png", format="png", dpi=200)
plt.clf()

# трансформация по одной переменной (gr3.png)

mesh = UnitSquareMesh(n1, n2)
th1 = mesh.coordinates()[:, 0]
th2 = mesh.coordinates()[:, 1]

fgr = 1 - 0.5 * np.cos(np.pi*th1)
mesh.coordinates()[:, 0] = 2*th1
mesh.coordinates()[:, 1] = th2*fgr
plot(mesh)
plt.savefig("gr4.png", format="png", dpi=200)
plt.clf()

# сравнение сеток

mesh = RectangleMesh(Point(0, 0), Point(2, 1), 17, 9)
plot(mesh)
plt.savefig("gr5.png", format="png", dpi=200)
plt.clf()
print(mesh.num_vertices(), mesh.num_cells())


mesh = Mesh("2.xml")
plot(mesh)
plt.savefig("gr6.png", format="png", dpi=200)
plt.clf()
print(mesh.num_vertices(), mesh.num_cells())

# параллелепипед
import pyvista as pv
import meshio
mesh = BoxMesh(Point(0,0,0), Point(1,1,1), 4,4,4)

# Конвертация через meshio "на лету"
pv_mesh = pv.wrap(meshio.Mesh(
    points=mesh.coordinates(),
    cells=[("tetra", mesh.cells())]
))

plotter = pv.Plotter()
plotter.add_mesh(pv_mesh, show_edges=True)
plotter.add_axes()

# Покажем окно, но НЕ закроем его автоматически
plotter.show(auto_close=False)

# После закрытия окна вручную (клик ×), выполнится:
plotter.screenshot("gr7.png", return_img=False)
plotter.close()

# модуль mshr

from mshr import *
domain = Rectangle(Point(0., 0.), Point(2, 2)) - Circle(Point(0.0, 0.0), 1) 
mesh = generate_mesh(domain, 10)
plot(mesh)
plt.savefig("gr8.png", format="png", dpi=200)
plt.clf()

