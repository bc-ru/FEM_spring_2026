import matplotlib.pyplot as plt
import numpy as np 
from fenics import *

m = 40
c0 = 50

kmax = 10
kk = 1

pList = [1, 2]
lamR = np.zeros((kmax, 4))

for pm in range(0, len(pList)):
    p = pList[pm]
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

        lamR[k,2*pm] = r
        lamR[k,2*pm+1] = c
        print(f"{k+1}, {r:.4e}, {c:.4e}")

# Печать
for i in range(lamR.shape[0]):
    row = ' & ' + f'{lamR[i,0]:.4e}' + f' + {lamR[i,1]:.4e}i' + ' & ' + f'{lamR[i,2]:.4e}' + f' + {lamR[i,3]:.4e}i'
    print(f'{i+1}  {row} \\\\')