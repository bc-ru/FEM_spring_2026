import numpy as np
import matplotlib.pyplot as plt
from scipy.special import legendre
from scipy import integrate
from cycler import cycler

def f(x):
    return 1./(1.+25*x**2)

r"""
**Базисные функции**
"""
# Настройка для черно-белой печати графиков
bw_cycler = (cycler(color=['black']) *
             cycler(linestyle=['-', '--', '-.', ':']) )
plt.rc('axes', prop_cycle=bw_cycler)

N = 500
xx = np.linspace(-1.,1.,N)
yy = np.linspace(-1.,1.,N)

plt.figure(figsize=(8, 4.5))

k_list = [1, 2, 5, 8]
for k in k_list:

    ri = legendre(k)
    fi = ri(xx)

    plt.plot(xx, fi, label=f"$k = ${k}")

plt.xlabel('$x$')
plt.grid(True)
plt.legend(loc="best")
plt.savefig('f-5.4.png', format="png", dpi=600)
plt.show()