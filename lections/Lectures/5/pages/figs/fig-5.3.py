import numpy as np
import matplotlib.pyplot as plt
from scipy.special import legendre
from scipy import integrate
from cycler import cycler

def f(x):
    return 1./(1.+25*x**2)

r"""
**Приближение функции Рунге**
"""
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

ni_list = [5, 9, 17]
for ni in ni_list:
    xi = np.linspace(-1.,1.,ni)
    yi = f(xi)

    ck = np.zeros((ni), "float")
    for k in range(0, ni):
        pk = legendre(k)
        fk = lambda x : 1./(1.+25*x**2)*pk(x)
        ck[k], err = integrate.quad(fk, -1, 1)

    for j in range(0, N):
        s = 0.
        for k in range(0, ni):
            pk = legendre(k)
            s = s + ck[k]*(2*k+1)*0.5*pk(xx[j])
        yy[j] = s

    plt.plot(xx, yy, label=f"$n = ${ni-1}")

plt.xlabel('$x$')
plt.grid(True)
plt.legend(loc="best")
plt.savefig('f-5.3.png', format="png", dpi=600)
plt.show()