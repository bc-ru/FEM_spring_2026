import matplotlib.pyplot as plt
import numpy as np
from fenics import *

def f(x):
    return 1./(1.+25*x**2)

m = 4
p = 2

a = -1.
b = 1.

N = 500
xx = np.linspace(a, b, N)
yy = np.linspace(a, b, N)
ye = f(xx)

plt.figure(figsize=(8, 4.5))

grt = ['k-', 'k--', 'k-.', 'k:']
l = 0
m_list = [2, 3, 4]

plt.plot(xx, ye, grt[0], label=f"$f(x)$")
for m in m_list:
    mesh = IntervalMesh(m, a, b)
    V = FunctionSpace(mesh, "DG", p)

    fr = Expression("1/(1+25*x[0]*x[0])", degree=p+2)
    u = interpolate(fr, V)
    for i in range(0, N):
        yy[i]  = u(Point(xx[i]))

    ss = grt[l+1]
    l = l + 1
    plt.plot(xx, yy, ss, label=f"$m = ${m}")

plt.xlabel('$x$')
plt.grid(True)
plt.legend(loc="best")
plt.savefig('f-8.12.png', format="png", dpi=600)
plt.show()

