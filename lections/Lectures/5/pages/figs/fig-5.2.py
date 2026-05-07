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

ni = 9
xi = np.linspace(-1.,1.,ni)
y0 = np.zeros((ni), "float")
plt.scatter(xi, y0)

k_list = [0, 1, 2, 4]
for k in k_list:
    phi = np.zeros((ni), "float")
    phi[k] = 1.
    ri = interpolate.lagrange(xi, phi)
    fi = ri(xx)
    plt.plot(xx, fi, label=f"$k = ${k}")

plt.xlabel('$x$')
plt.grid(True)
plt.legend(loc="best")
plt.savefig('f-5.2.png', format="png", dpi=600)
plt.show()