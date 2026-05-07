import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interpolate
from cycler import cycler

def f(x):
    return 1./(1.+25*x**2)

r"""
**Кусочно-линейная интерполяция**
"""
def pk(x, k, xi):
    h1 = 1/(xi[1]-xi[0])
    g = 0.
    if k == 0:
        if x < xi[1]:
            g = h1*(xi[1]-x)
        return g
    if k == len(xi)-1:
        if x >xi[k-1]:
            g = h1*(x-xi[k-1])
        return g
    if k > 0 and k < len(xi)-1:
        if x > xi[k-1] and x < xi[k]:
            g = h1*(x-xi[k-1])
        if x >= xi[k] and x < xi[k+1]:
            g = h1*(xi[k+1]-x)
        return g

# Настройка для черно-белой печати графиков
bw_cycler = (cycler(color=['black']) *
             cycler(linestyle=['-', '--', '-.', ':']) )
plt.rc('axes', prop_cycle=bw_cycler)

N = 500
xx = np.linspace(-1.,1.,N)
yy = np.linspace(-1.,1.,N)
fe = f(xx)

plt.figure(figsize=(8, 4.5))
plt.plot(xx, fe, label=r"$f(x)$")

ni_list = [3, 5, 9]
for ni in ni_list:
    xi = np.linspace(-1.,1.,ni)
    yi = f(xi)
    y0 = np.zeros((ni), "float")

    for j in range(0, N):
        s = 0.
        for k in range(0, ni):
            s = s + yi[k]*pk(xx[j], k, xi)
        yy[j] = s
    plt.plot(xx, yy, label=f"$n = ${ni-1}")

plt.scatter(xi, y0)

plt.xlabel('$x$')
plt.grid(True)
plt.legend(loc="best")
plt.savefig('f-6.1.png', format="png", dpi=600)
plt.show()