import matplotlib.pyplot as plt
import numpy as np 
from fenics import *

c0 = 0

kmax = 10
kk = 1

pList = [1, 1, 2, 2]
mList = [20, 40, 20, 40]
lamR = np.zeros((kmax, 4))

for pm in range(0, len(pList)):
    p = pList[pm]
    m = mList[pm]
    print(f"p = {p}, m = {m}")

    mesh = UnitSquareMesh(m, m)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float")

    V = FunctionSpace(mesh, "CG", p)
    n = V.dim()-1

    u = TrialFunction(V)
    v = TestFunction(V)

    cc = Constant([c0,c0])
    a = dot(grad(u), grad(v))*dx + dot(cc,grad(u))*v*dx
    b = u*v*dx

    # Assemble stiffness form
    A = PETScMatrix()
    assemble(a, tensor=A)
    B = PETScMatrix()
    assemble(b, tensor=B)

    # Create eigensolver
    eigensolver = SLEPcEigenSolver(A,B)
    eigensolver.parameters["spectrum"] = "smallest magnitude"
    eigensolver.solve(kmax)

    for k in range(0, kmax):
        r, c, rx, cx = eigensolver.get_eigenpair(k)

        lamR[k,pm] = r
        print(f"{k+1}, {r:.4e}, {c:.4e}")

# Правильная печать
for i in range(lamR.shape[0]):
    row = ' & '.join(f'{lamR[i,j]:.4e}' for j in range(lamR.shape[1]))
    print(f'{i+1} & {row} \\\\')
