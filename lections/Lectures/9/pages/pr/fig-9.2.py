import matplotlib.pyplot as plt
import numpy as np 
from fenics import *

m = 10
p = 1
kap = 10

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
    
    def boundary(x, on_boundary):
        return on_boundary
    bc = DirichletBC(V, Constant("0."), boundary)
    
    f = Expression("1", degree=p+2)
    kk = Expression("x[0] < 0.5 ? 1 : kap", kap = kap, degree=p+2)
    a = kk*dot(grad(u), grad(v))*dx
    L = f*v*dx

    u = Function(V)
    solve(a == L, u, bc)
    
    N = 500
    xx = np.linspace(0., 1., N) 
    yy = np.linspace(0., 1., N)  
    
    for i in range(0, N): 
        yy[i]  = u(Point(xx[i]))
    s = "$m = $" + str(m)
    ss = grt[k]
    plt.plot(xx, yy, ss, label = s)
    m = m*2

plt.scatter(xm, ym, c='black', s=10)
plt.xlabel('$x$') 
plt.legend(loc=0)
plt.grid(True)
plt.savefig('f-9.2.png', format="png", dpi=600)
plt.show()
