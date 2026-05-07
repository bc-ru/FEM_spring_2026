import matplotlib.pyplot as plt
import numpy as np 
from fenics import *
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
import time

m = 200
p = 2
c = 10

mesh = UnitSquareMesh(m, m)
xm = mesh.coordinates()
ym = np.zeros((m+1), "float")

V = FunctionSpace(mesh, "CG", p)
n = V.dim()-1

u = TrialFunction(V)
v = TestFunction(V)

def boundary(x, on_boundary):
    return on_boundary
bc = DirichletBC(V, Expression("x[0]*x[1]", degree=p+2), boundary)

f = Expression("0.", degree=p+2)
cc = Constant([c,c])
a = dot(grad(u), grad(v))*dx + dot(cc,grad(u))*v*dx
L = f*v*dx

w = Function(V)
solve(a == L, w, bc)

N = 200
x = np.linspace(0,1,N)
y = np.linspace(0,1,N)
yy  = np.zeros((N,N))
tk = np.linspace(0,1,11)

for i in range(0, N):
    for j in range(0, N):
        pp = Point(x[i],y[j])
        yy[j,i] = w(pp)

plt.figure(figsize=(10, 6))
plt.contourf(x,y,yy, cmap='binary')
plt.gca().set_aspect("equal")
plt.colorbar()
plt.xticks(ticks=tk)
plt.yticks(ticks=tk)
plt.savefig('f-13.1.png', format="png", dpi=600)
plt.show()

