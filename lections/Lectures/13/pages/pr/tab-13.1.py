import matplotlib.pyplot as plt
import numpy as np 
from fenics import *
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
import time
set_log_active(False)

p = 1
c = 10

print("p = " + str(p) + ",  c = " + str(c))
print("Число  1D разбиений  Число неизвестных    Время решения")

m = 100
for kk in range(0, 3):

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
    start_time = time.perf_counter()
    solve(a == L, w, bc)
    tsol = time.perf_counter() - start_time

    print(f"{p}  &   {m}  & {n}  & {tsol:.4e} ")

    m = m*2

