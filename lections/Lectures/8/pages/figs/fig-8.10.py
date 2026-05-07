import matplotlib.pyplot as plt
import numpy as np 
from fenics import *

m = 3
p = 2

p1 = Point(0,0)
p2 = Point(1,1)

mesh = RectangleMesh(p1, p2, m, m)
xm = mesh.coordinates()
ym = np.zeros((m+1), "float") 

V = FunctionSpace(mesh, "DG", p)
n = V.dim()-1

u = Function(V)
k_list = [13, 36, 50, 63, 88]
for k in k_list:
    u.vector()[k] = 1
plot(u)

N = 200
x = np.linspace(0,1,N)
y = np.linspace(0,1,N)
yy  = np.zeros((N,N)) 
vv = np.linspace(-1,1,21)
tk = np.linspace(0,1,m+1)

for i in range(0, N): 
    for j in range(0, N): 
        pp = Point(x[i],y[j])
        yy[j,i]  = u(pp)
          
fig1 = plt.figure(1)
plt.contourf(x,y,yy,vv, cmap='binary')
plt.gca().set_aspect("equal")
plt.grid(True) 
plt.xticks(ticks=tk)
plt.yticks(ticks=tk)
plt.savefig('f-8.10.png', format="png", dpi=600)
plt.show()