import matplotlib.pyplot as plt
import numpy as np 
from fenics import *
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
import time
import pandas as pd

m = 10
p = 2
c = 10

mesh = UnitSquareMesh(m, m)
xm = mesh.coordinates()
ym = np.zeros((m+1), "float") 

V = FunctionSpace(mesh, "CG", p)
n = V.dim()-1

u = TrialFunction(V)
v = TestFunction(V)

f = Expression("x[0]*x[1]", degree=p+2)
q = Expression("0", degree=p+2)    
cc = Constant(c)
a = dot(grad(u), grad(v))*dx + cc*u*v*dx
L = f*v*dx 

A, b = assemble_system(a, L)
mat = as_backend_type(A).mat()
As = csr_matrix(mat.getValuesCSR()[::-1], shape=mat.size)
An = As.toarray()

start_time = time.perf_counter()
wn = Function(V)
yn = np.linalg.solve(An, b) 
wn.vector().set_local(yn)
tn = time.perf_counter() - start_time

start_time = time.perf_counter()
ws = Function(V)
ys = spsolve(As, b)
ws.vector().set_local(ys)
ts = time.perf_counter() - start_time

start_time = time.perf_counter()
w = Function(V)
solve(a == L, w, solver_parameters={"linear_solver": "default", "preconditioner":"default"})
tf = time.perf_counter() - start_time

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
        ye[j,i] = ws(pp)

plt.figure(figsize=(10, 6))
plt.contourf(x,y,yy, cmap='binary')
plt.gca().set_aspect("equal")
plt.colorbar()
plt.grid(True)
plt.xticks(ticks=tk)
plt.yticks(ticks=tk)
plt.savefig('f-12.2.png', format="png", dpi=600)
plt.show()


