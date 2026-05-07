import matplotlib.pyplot as plt
import numpy as np 
from fenics import *
from scipy.sparse import csr_matrix

m = 5
p = 1
c = 1

mesh = UnitSquareMesh(m, m)

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

A = assemble(a)
mat = as_backend_type(A).mat()
csr = csr_matrix(mat.getValuesCSR()[::-1], shape=mat.size)

plt.figure(figsize=(6, 6))
plt.spy(csr, marker='o', markersize=4, color='black')
plt.grid(True)
plt.savefig('f-11.1.png', format="png", dpi=600)
plt.show()
