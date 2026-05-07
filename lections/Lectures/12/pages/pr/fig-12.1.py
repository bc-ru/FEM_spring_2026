import matplotlib.pyplot as plt
import numpy as np 
from fenics import *
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
import time
import pandas as pd

m = 5
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

A = assemble(a)
mat = as_backend_type(A).mat()
csr = csr_matrix(mat.getValuesCSR()[::-1], shape=mat.size)

plt.figure(figsize=(6, 6))
plt.spy(csr, marker='o', markersize=2, color='black')
plt.grid(True)
plt.savefig('f-12.1.png', format="png", dpi=600)
plt.show()