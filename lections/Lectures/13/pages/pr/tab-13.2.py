import matplotlib.pyplot as plt
import numpy as np 
from fenics import *
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
import time
set_log_active(False)

m = 100
p = 1
c = 0

print("p = " + str(p) + ",  c = " + str(c))
print("Метод  Число неизвестных    Время решения")

ss1 = ""
ss2 = ""
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
    
    start_time = time.perf_counter()
    w = Function(V)
    solve(a == L, w, bc, solver_parameters={'linear_solver': 'cg',
                         'preconditioner': 'ilu'})
    ts = time.perf_counter() - start_time
    start_time = time.perf_counter()
    w1 = Function(V)
    solve(a == L, w1, bc, solver_parameters={'linear_solver': 'gmres',
                         'preconditioner': 'ilu'})
    ts1 = time.perf_counter() - start_time

    ss1 = ss1 + f"cg     &   {m}  & {n}  & {ts:.4e} \n"
    ss2 = ss2 + f"gmres  &   {m}  & {n}  & {ts1:.4e} \n"

    m = m*2
print(ss1)
print(ss2)