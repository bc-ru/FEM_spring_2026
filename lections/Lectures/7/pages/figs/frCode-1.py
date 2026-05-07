import matplotlib.pyplot as plt
import numpy as np
from fenics import *

a = 0; b = 1
m = 3; p = 2

mesh = IntervalMesh(m, 0, 1)
V = FunctionSpace(mesh, "CG", p)
N = 500
xx = np.linspace(a, b, N)
yy = np.linspace(a, b, N)

k = 4
u = Function(V)
u.vector()[k] = 1
for i in range(0, N):
    yy[i]  = u(Point(xx[i]))
plt.plot(xx, yy, label=f"$k = ${k}")
plt.show()