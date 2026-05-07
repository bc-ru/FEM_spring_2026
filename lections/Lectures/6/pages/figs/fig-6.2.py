import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interpolate
from cycler import cycler

def f(x):
    return 1./(1.+25*x**2)

r"""
**Кусочно-линейные базисные функции**
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

ni = 9
xi = np.linspace(-1.,1.,ni)
y0 = np.zeros((ni), "float")
plt.scatter(xi, y0)

k_list = [0, 1, 2, 4]
for k in k_list:
    for j in range(0, N):
        yy[j] =  pk(xx[j], k, xi)
    plt.plot(xx, yy, label=f"$k = ${k}")

plt.xlabel('$x$')
plt.grid(True)
plt.legend(loc="best")
plt.savefig('f-6.2.png', format="png", dpi=600)
plt.show()