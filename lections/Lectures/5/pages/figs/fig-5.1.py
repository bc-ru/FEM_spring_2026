import numpy as np
import matplotlib.pyplot as plt
import scipy.interpolate as interpolate
from cycler import cycler

def f(x):
    return 1./(1.+25*x**2)

r"""
**Полиномиальная интерполяция**
"""
# Настройка для черно-белой печати графиков
bw_cycler = (cycler(color=['black']) *
             cycler(linestyle=['-', '--', '-.', ':']) )
plt.rc('axes', prop_cycle=bw_cycler)

N = 500
xx = np.linspace(-1.,1.,N)
fe = f(xx)

plt.figure(figsize=(8, 4.5))
plt.plot(xx, fe, label=r"$f(x)$")

ni_list = [3, 5, 9]
for ni in ni_list:
    xi = np.linspace(-1.,1.,ni)
    yi = f(xi)
    y0 = np.zeros((ni), "float")

    r = interpolate.lagrange(xi, yi)
    ff = r(xx)
    plt.plot(xx, ff, label=f"$n = ${ni-1}")

plt.scatter(xi, y0)

plt.xlabel('$x$')
plt.grid(True)
plt.legend(loc="best")
plt.savefig('f-5.1.png', format="png", dpi=600)
plt.show()