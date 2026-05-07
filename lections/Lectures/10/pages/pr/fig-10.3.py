import matplotlib.pyplot as plt
import numpy as np 
from fenics import *

m = 40
p = 2
c = 1

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
    bc = DirichletBC(V, Expression("x[0]", degree=p+2), boundary)
    
    f = Expression("0.", degree=p+2)
    cc = Constant(c)
    a = u.dx(0)*v.dx(0)*dx + cc*u.dx(0)*v*dx
    L = f*v*dx

    w = Function(V)
    solve(a == L, w, bc)
    
    N = 500
    xx = np.linspace(0., 1., N) 
    yy = np.linspace(0., 1., N)  
    
    for i in range(0, N): 
        yy[i]  = w(Point(xx[i]))
    s = "$c = $" + str(c)
    ss = grt[k]
    plt.plot(xx, yy, ss, label = s)
    c = c*10

plt.xlabel('$x$')
plt.legend(loc=0)
plt.grid(True)
plt.savefig('f-10.6.png', format="png", dpi=600)
plt.show()