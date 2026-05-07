import matplotlib.pyplot as plt
import numpy as np
from fenics import *

sig = 1.

vp = 1.
dp = 0.25
T = 1./vp
p = 1

plt.figure(figsize=(10, 6))
grt = ['k-', 'k--', 'k:']
mList = [20, 40, 80]
NList = [50, 200, 800]
for mN in range(0, len(mList)):
    m = mList[mN]
    N = NList[mN]
    tau = T/N
    print(f"N = {N}, m = {m}")

    mesh = IntervalMesh(m, 0, 1)
    xm = mesh.coordinates()
    ym = np.zeros((m+1), "float")

    V = FunctionSpace(mesh, "CG", p)

    u = TrialFunction(V)
    v = TestFunction(V)

    t = 0.
    y1 = project(Expression("exp(-pow(x[0]-vp*t, 2) / pow(dp, 2))", degree=p+2, vp=vp, dp=dp, t=t),V)

    y = Function(V)
    ue = Function(V)
    tt = [0.]
    ut = [0.]
    er = [0.]
    for n in range(N):
        t = t + tau
        ts = sig*t + (1-sig)*(t-tau)

        f = Expression("2/pow(dp,2)*exp(-pow(x[0]-vp*t, 2) / pow(dp, 2))"
                       "*(vp*(x[0]-vp*t)+1-2/pow(dp,2)*pow(x[0]-vp*t,2))",
                       degree=p+2, vp=vp, dp=dp, t=ts)
        bc = DirichletBC(V, Expression("exp(-pow(x[0]-vp*t, 2) / pow(dp, 2))",
                                       degree=p+2, vp=vp, dp=dp, t=t), "on_boundary")

        a = u*v*dx + sig*tau*dot(grad(u), grad(v))*dx
        cc = Constant((1-sig)*tau)
        L = y1*v*dx + tau*f*v*dx - cc*dot(grad(y1), grad(v))*dx
        solve(a == L, y, bc)
        y1.assign(y)

        tt.append(t)
        ue = project(Expression("exp(-pow(x[0]-vp*t, 2) / pow(dp, 2))", degree=p+2, vp=vp, dp=dp, t=t),V)
        ut.append(y.vector()-ue.vector())
        ern = assemble((y - ue) ** 2 * dx) ** 0.5
        er.append(ern)

    s = "$m = $" + str(m) + ",  N = " + str(N)
    ss = grt[mN]
    plt.plot(tt, er, ss, label = s)

plt.xlabel('$t$')
plt.ylabel('$\\varepsilon$')
plt.legend(loc=0)
plt.grid(True)
plt.savefig('f-18.1.png', format="png", dpi=600)
plt.show()

