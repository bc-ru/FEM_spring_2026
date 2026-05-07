import matplotlib.pyplot as plt
import numpy as np
from fenics import *

m = 10
p = 1

def f(x,y):
    return (1-(x**2+y**3))*np.exp(-(x**2+y**2)/2)

p1 = Point(-3,-3)
p2 = Point(3,3)

mesh = RectangleMesh(p1, p2, m, m)
xm = mesh.coordinates()
ym = np.zeros((m+1), "float")

V = FunctionSpace(mesh, "CG", p)
n = V.dim()-1

fr = Expression("(1-x[0]*x[0]-x[1]*x[1]*x[1])*exp(-0.5*(x[0]*x[0]+x[1]*x[1]))", degree=p+2)
u = interpolate(fr, V)
w = project(fr,V)

N = 200
x = np.linspace(-3,3,N)
y = np.linspace(-3,3,N)
yy  = np.zeros((N,N))
ye  = np.zeros((N,N))
ww  = np.zeros((N,N))
tk = np.linspace(-3,3,m+1)

for i in range(0, N):
    for j in range(0, N):
        pp = Point(x[i],y[j])
        yy[j,i] = u(pp)
        ww[j,i] = w(pp)
        ye[j,i] = f(x[i], y[j])

fig1 = plt.figure(1)
ss = "$m = $" + str(m) + "$,  p = $" + str(p)
plt.title(ss)
plt.contourf(x,y,yy, cmap='binary')
plt.gca().set_aspect("equal")
plt.colorbar()
plt.grid(True)
plt.xticks(ticks=tk)
plt.yticks(ticks=tk)

fig2 = plt.figure(2)
plt.contourf(x,y,ww-ye, cmap='binary')
plt.gca().set_aspect("equal")
plt.colorbar()
plt.grid(True)
plt.xticks(ticks=tk)
plt.yticks(ticks=tk)
plt.savefig('f-7.14-1.png', format="png", dpi=600)

fig2 = plt.figure(3)
plt.contourf(x,y,yy-ye, cmap='binary')
plt.gca().set_aspect("equal")
plt.colorbar()
plt.grid(True)
plt.xticks(ticks=tk)
plt.yticks(ticks=tk)
plt.savefig('f-7.13-1.png', format="png", dpi=600)
plt.show()