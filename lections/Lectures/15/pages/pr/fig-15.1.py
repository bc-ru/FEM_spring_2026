import matplotlib.pyplot as plt
import numpy as np 
from fenics import *

c0 = 0

m = 40
p = 2
kmax = 10
kk = 1

mesh = UnitSquareMesh(m, m)
xm = mesh.coordinates()
ym = np.zeros((m+1), "float")

V = FunctionSpace(mesh, "CG", p)
n = V.dim()-1

u = TrialFunction(V)
v = TestFunction(V)

cc = Constant([c0,c0])
a = dot(grad(u), grad(v))*dx + dot(cc,grad(u))*v*dx
b = u*v*dx

# Assemble stiffness form
A = PETScMatrix()
assemble(a, tensor=A)
B = PETScMatrix()
assemble(b, tensor=B)

# Create eigensolver
eigensolver = SLEPcEigenSolver(A,B)
eigensolver.parameters["spectrum"] = "smallest magnitude"
eigensolver.solve(kmax)

for k in range(0, kmax):
    r, c, rx, cx = eigensolver.get_eigenpair(k)

    print(f"{k+1}, {r:.4e}, {c:.4e}")

    if k == 2:
        u1 = Function(V)
        u1.vector()[:] = rx
    if k == 4:
        u2 = Function(V)
        u2.vector()[:] = rx

N = 200
x = np.linspace(0,1,N)
y = np.linspace(0,1,N)
yy  = np.zeros((N,N))
ye  = np.zeros((N,N))
tk = np.linspace(0,1,11)

for i in range(0, N):
    for j in range(0, N):
        pp = Point(x[i],y[j])
        yy[j,i] = u1(pp)

plt.figure(figsize=(10, 6))
plt.contourf(x,y,yy, cmap='binary')
plt.gca().set_aspect("equal")
plt.colorbar()
plt.xticks(ticks=tk)
plt.yticks(ticks=tk)
plt.savefig('f-15.2-1.png', format="png", dpi=600)
plt.show()

for i in range(0, N):
    for j in range(0, N):
        pp = Point(x[i],y[j])
        yy[j,i] = u2(pp)

plt.figure(figsize=(10, 6))
plt.contourf(x,y,yy, cmap='binary')
plt.gca().set_aspect("equal")
plt.colorbar()
plt.xticks(ticks=tk)
plt.yticks(ticks=tk)
plt.savefig('f-15.2-2.png', format="png", dpi=600)
plt.show()

    
