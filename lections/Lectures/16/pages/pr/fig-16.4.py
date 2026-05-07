import matplotlib.pyplot as plt
import numpy as np 
from fenics import *

m = 80
pp = 2

mesh = UnitSquareMesh(m, m)
xm = mesh.coordinates()
ym = np.zeros((m+1), "float") 

U = VectorElement("Lagrange", mesh.ufl_cell(), pp)
P = FiniteElement("Lagrange", mesh.ufl_cell(), pp-1)
V = FunctionSpace(mesh, U*P)

u, p = TrialFunctions(V)
v, q = TestFunctions(V)

def on_top(x, on_boundary):
    return near(x[1], 1) and on_boundary
def no_top(x, on_boundary):
    return on_boundary and not near(x[1], 1) 

bc1 = DirichletBC(V.sub(0), Constant((1,0)), on_top)
bc2 = DirichletBC(V.sub(0), Constant((0,0)), no_top)
bcs = [bc1, bc2]

F = inner(grad(u), grad(v))*dx - div(v)*p*dx + q*div(u)*dx 
a = lhs(F)
L = rhs(F)

w = Function(V)
solve(a == L, w, bcs)
us, ps = w.split(True)
u1, u2 = us.split(True)

N = 200
x = np.linspace(0,1,N)
y = np.linspace(0,1,N)
yy  = np.zeros((N,N))
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
plt.savefig('f-16.4-1.png', format="png", dpi=600)
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
plt.savefig('f-16.4-2.png', format="png", dpi=600)
plt.show()


