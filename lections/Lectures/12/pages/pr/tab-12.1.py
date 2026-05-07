import matplotlib.pyplot as plt
import numpy as np 
from fenics import *
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import spsolve
import time
import pandas as pd

m = 40
c = 5.6666

mesh = UnitSquareMesh(m, m)
xm = mesh.coordinates()
ym = np.zeros((m+1), "float")

tn = np.zeros((3), "float")
ts = np.zeros((3), "float")
tf = np.zeros((3), "float")

for im in range(3):
    p = im + 1
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
    fig1 = plt.figure(1)
    plt.spy(As)

    start_time = time.perf_counter()
    wn = Function(V)
    yn = np.linalg.solve(An, b)
    wn.vector().set_local(yn)
    tn[im] = time.perf_counter() - start_time

    start_time = time.perf_counter()
    ws = Function(V)
    ys = spsolve(As, b)
    ws.vector().set_local(ys)
    ts[im] = time.perf_counter() - start_time

    start_time = time.perf_counter()
    w = Function(V)
    solve(a == L, w, solver_parameters={"linear_solver": "default", "preconditioner":"default"})
    tf[im] = time.perf_counter() - start_time

print("m = " + str(m) + ",  c = " + str(c))
print(f"NumPy  & {tn[0]:.4e}  & {tn[1]:.4e}  & {tn[2]:.4e}")
print(f"SciPy  & {ts[0]:.4e}  & {ts[1]:.4e}  & {ts[2]:.4e}")
print(f"FEniCS & {tf[0]:.4e}  & {tf[1]:.4e}  & {tf[2]:.4e}")
