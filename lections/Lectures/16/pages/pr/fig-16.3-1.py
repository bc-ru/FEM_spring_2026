import matplotlib.pyplot as plt
import numpy as np 
from fenics import *

plt.figure(figsize=(8, 4.5))
grt = ['k-', 'k--', 'k:']
pList = [2, 2, 2]
mList = [20, 40, 80]

for pm in range(0, len(pList)):
    pp = pList[pm]
    m = mList[pm]
    print(f"p = {pp}, m = {m}")

    mesh = UnitSquareMesh(m, m)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float")

    U = VectorElement("Lagrange", mesh.ufl_cell(), pp)
    P = FiniteElement("Lagrange", mesh.ufl_cell(), pp-1)
    V = FunctionSpace(mesh, U*P)

    u, p = TrialFunctions(V)
    v, q = TestFunctions(V)

    def on_top(x, on_boundary):
        return near(x[1], 1) and on_boundary
    def no_top(x, on_boundary):
        return on_boundary and not near(x[1], 1)

    bc1 = DirichletBC(V.sub(0), Constant((1,0)), on_top)
    bc2 = DirichletBC(V.sub(0), Constant((0,0)), no_top)
    bcs = [bc1, bc2]

    F = inner(grad(u), grad(v))*dx - div(v)*p*dx + q*div(u)*dx
    a = lhs(F)
    L = rhs(F)

    w = Function(V)
    solve(a == L, w, bcs)
    us, ps = w.split(True)
    u1, u2 = us.split(True)

    N = 500
    xx = np.linspace(0., 1., N)
    yy = np.linspace(0., 1., N)

    for i in range(0, N):
        yy[i]  = u1(Point(0.5,xx[i]))
    s = "$m = $" + str(m)
    ss = grt[pm]
    plt.plot(xx, yy, ss, label = s)

plt.xlabel('$x_1 = 0.5, x_2$')
plt.legend(loc=0)
plt.grid(True)
plt.savefig('f-16.3-1.png', format="png", dpi=600)
plt.show()

