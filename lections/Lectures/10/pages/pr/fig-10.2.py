import matplotlib.pyplot as plt
import numpy as np 
from fenics import *
from scipy.sparse import csr_matrix

m = 40
p = 1
kap = 10
sig = 10

plt.figure(figsize=(8, 4.5))
grt = ['k-', 'k--', 'k:']

for k in range(0, 3):

    mesh = IntervalMesh(m, 0, 1)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float") 
    
    V = FunctionSpace(mesh, "CG", p)
    n = V.dim()-1
    
    u = TrialFunction(V)
    v = TestFunction(V)

    f = Expression("1", degree=p+2)
    kk = Expression("x[0] < 0.5 ? 1 : kap", kap = kap, degree=p+2)
    a = kk*dot(grad(u), grad(v))*dx + sig*u*v*ds
    L = f*v*dx

    u = Function(V)
    solve(a == L, u)
    
    N = 500
    xx = np.linspace(0., 1., N) 
    yy = np.linspace(0., 1., N)  
    
    for i in range(0, N): 
        yy[i]  = u(Point(xx[i]))
    s = "$\\sigma = $" + str(sig)
    ss = grt[k]
    plt.plot(xx, yy, ss, label = s)
    sig = sig*10

plt.scatter(xm, ym, c='black', s=10)
plt.xlabel('$x$') 
plt.legend(loc=0)
plt.grid(True)
plt.savefig('f-10.2.png', format="png", dpi=600)
plt.show()

