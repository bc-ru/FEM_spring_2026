import matplotlib.pyplot as plt
import numpy as np 
from fenics import *

m = 40
p = 2

kap = 0.1
rr =  0.01
# kap = 0.2
# rr =  0.25

mesh = UnitSquareMesh(m, m)
xm = mesh.coordinates()
ym = np.zeros((m+1), "float") 

V1 = FiniteElement("CG", mesh.ufl_cell(), p)
V2 = FiniteElement("CG", mesh.ufl_cell(), p)
V = FunctionSpace(mesh, V1*V2)

u = TrialFunction(V)
v = TestFunction(V)

def left(x, on_boundary):
    return near(x[0], 0) and x[1] < 0.5 and on_boundary
def right(x, on_boundary):
    return near(x[0], 1) and on_boundary

bc1 = DirichletBC(V.sub(0), Constant(0.), left)
bc2 = DirichletBC(V.sub(0), Constant(1.), right)
bcs = [bc1, bc2]

F = dot(grad(u[0]), grad(v[0]))*dx + rr*(u[0]-u[1])*v[0]*dx \
  + kap*dot(grad(u[1]), grad(v[1]))*dx - rr*(u[0]-u[1])*v[1]*dx 
a = lhs(F)
L = rhs(F)

w = Function(V)
solve(a == L, w, bcs)
(u1, u2) = w.split(True)

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
plt.contourf(x,y,yy, cmap='binary', levels=np.linspace(0,1, 11))
plt.gca().set_aspect("equal")
plt.colorbar()
plt.xticks(ticks=tk)
plt.yticks(ticks=tk)
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
plt.savefig('f-16.2-1.png', format="png", dpi=600)
plt.show()



