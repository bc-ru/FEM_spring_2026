import matplotlib.pyplot as plt
import numpy as np 
from fenics import *

m = 10
p = 2
c = 1000

mesh = UnitSquareMesh(m, m)
xm = mesh.coordinates()
ym = np.zeros((m+1), "float") 

V = FunctionSpace(mesh, "CG", p)
n = V.dim()-1

u = TrialFunction(V)
v = TestFunction(V)

boundary_markers = MeshFunction('size_t', mesh, mesh.topology().dim()-1)
tol = 1E-14
b0 = CompiledSubDomain("on_boundary && near(x[0], 0, tol)", tol=tol)
b1 = CompiledSubDomain("on_boundary && near(x[1], 0, tol)", tol=tol)
b0.mark(boundary_markers, 0)
b1.mark(boundary_markers, 1)
ds = Measure("ds", domain=mesh, subdomain_data=boundary_markers)

u_D = Expression("0", degree=p+2)
bcs = [DirichletBC(V, u_D, b0), DirichletBC(V, u_D, b1)]


f = Expression("1", degree=p+2)
cc = Expression("x[0] > 0.5 and x[1] > 0.5 ? c : 0", c = c, degree=p+2)
a = dot(grad(u), grad(v))*dx + cc*u*v*dx
L = f*v*dx 

w = Function(V)
solve(a == L, w, bcs)

N = 200
x = np.linspace(0,1,N)
y = np.linspace(0,1,N)
yy  = np.zeros((N,N)) 
ye  = np.zeros((N,N)) 
tk = np.linspace(0,1,m+1)

for i in range(0, N): 
    for j in range(0, N): 
        pp = Point(x[i],y[j])
        yy[j,i] = w(pp)

plt.figure(figsize=(10, 6))
plt.contourf(x,y,yy, cmap='binary')
plt.gca().set_aspect("equal")
plt.colorbar()
plt.grid(True) 
plt.xticks(ticks=tk)
plt.yticks(ticks=tk)
plt.savefig('f-11.5.png', format="png", dpi=600)
plt.show()


