import matplotlib.pyplot as plt
import numpy as np 
from fenics import *
from scipy.sparse import csr_matrix

m = 20
p = 2
kap = 5
sig = 10

mesh = IntervalMesh(m, 0, 1)

V = FunctionSpace(mesh, "CG", p)
n = V.dim()-1

u = TrialFunction(V)
v = TestFunction(V)

kk = Expression("x[0] < 0.5 ? 1 : kap", kap = kap, degree=p+2)
a = kk*dot(grad(u), grad(v))*dx + sig*u*v*ds

A = assemble(a)
mat = as_backend_type(A).mat()
csr = csr_matrix(mat.getValuesCSR()[::-1], shape=mat.size)

plt.spy(csr, marker='o', markersize=4, color='black')
plt.grid(True)
plt.savefig('f-10.1.png', format="png", dpi=600)
plt.show()
