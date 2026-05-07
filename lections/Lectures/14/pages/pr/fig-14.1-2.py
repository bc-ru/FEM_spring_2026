import matplotlib.pyplot as plt
import numpy as np 
from fenics import *

m = 50
p = 2
al = 5.
bet = 2.

def k(u):
    return 1 + al*u**bet
def kp(u):
    return al*bet*u**(bet-1)

mesh = UnitSquareMesh(m, m)
xm = mesh.coordinates()
ym = np.zeros((m+1), "float") 

V = FunctionSpace(mesh, "CG", p)
n = V.dim()-1

u = TrialFunction(V)
v = TestFunction(V)
w = Function(V)

f = Expression("1", degree=p+2) 
bc = DirichletBC(V,  Expression("0.", degree=p+2), "on_boundary")

F = (k(w) * dot(grad(w), grad(v)) - f * v) * dx
solve(F == 0, w, bc)

N = 200
x = np.linspace(0,1,N)
y = np.linspace(0,1,N)
yy  = np.zeros((N,N)) 
ye  = np.zeros((N,N)) 
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
plt.savefig('f-14.1.png', format="png", dpi=600)
plt.show()

itMax = 9
ii = []
ei1 = []
ei2 = []

u_0 = Expression("0", degree=p+2) 
u1 = project(u_0, V)
u2 = project(u_0, V)
for it in range(0, itMax): 

    a1 = k(u1) * dot(grad(u), grad(v))*dx 
    L1 = f*v*dx 
    solve(a1 == L1, u1, bc)
    er1 = assemble((u1-w) ** 2 * dx) ** 0.5

    a2 = (k(u2) * dot(grad(u), grad(v))*dx
          + dot(kp(u2)*u*grad(u2),grad(v))*dx)
    L2 = dot(kp(u2)*u2*grad(u2),grad(v))*dx + f*v*dx 
    solve(a2 == L2, u2, bc)
    er2 = assemble((u2-w) ** 2 * dx) ** 0.5

    ii.append(it+1)
    ei1.append(er1)
    ei2.append(er2)

plt.figure(figsize=(8, 4.5))
st1 = "простая линеаризация"
st2 = "метод Ньютона"
plt.semilogy(ii,ei1,'k-', label=st1)
plt.semilogy(ii,ei2, 'k--', label=st2)
plt.legend(loc=0)
plt.xlabel('$k$')
plt.ylabel('$\\varepsilon$')
plt.grid(True)
plt.savefig('f-14.2.png', format="png", dpi=600)
plt.show()

