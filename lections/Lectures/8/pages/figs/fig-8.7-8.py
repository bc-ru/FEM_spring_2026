import matplotlib.pyplot as plt
import numpy as np
from fenics import *

m = 4
p = 1

a = 0.
b = 1.

mesh = IntervalMesh(m, a, b)
xm = mesh.coordinates()
ym = np.zeros((m+1), "float")

V = FunctionSpace(mesh, "DG", p)
n = V.dim()-1

N = 500
xx = np.linspace(a, b, N)
yy = np.linspace(a, b, N)

xn = V.tabulate_dof_coordinates()
yn = np.zeros((len(xn)), "float")

plt.figure(figsize=(8, 4.5))

plt.scatter(xm, ym, marker='o', c='black', s=50)
plt.scatter(xn, yn, marker='x', c='black')

grt = ['k-', 'k--', 'k:']
l = 0
k_list = [2, 3, 4]
# k_list = [3, 4, 5]
for k in k_list:
    u = Function(V)
    u.vector()[k] = 1

    for i in range(0, N):
        yy[i]  = u(Point(xx[i]))

    ss = grt[l]
    l = l + 1
    plt.plot(xx, yy, ss, label=f"$k = ${k}")

plt.xlabel('$x$')
plt.grid(True)
plt.legend(loc="best")
plt.savefig('f-8.7.png', format="png", dpi=600)
plt.show()
