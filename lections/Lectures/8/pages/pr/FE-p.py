import matplotlib.pyplot as plt
import numpy as np 
from fenics import *


fem = 1

if fem == 1:
    sfem = "DG"
else:
    sfem = "CG"


m = 5
p = 2

a = 0.
b = 1.

mesh = IntervalMesh(m, a, b)
xm = mesh.coordinates()
ym = np.zeros((m+1), "float") 

V = FunctionSpace(mesh, sfem, p)
n = V.dim()-1

k = 3
u = Function(V)
u.vector()[k] = 1

xn = V.tabulate_dof_coordinates()
yn = np.zeros((len(xn)), "float")   

N = 500
xx = np.linspace(a, b, N) 
yy = np.linspace(a, b, N)  

for i in range(0, N): 
    yy[i]  = u(Point(xx[i]))
          
fig1 = plt.figure(1)
ss = "$m = $" + str(m) + "$, \ p = $" + str(p)
plt.title(ss)

plt.scatter(xn, yn)  
plt.scatter(xm, ym)  
plt.plot(xx, yy)  
    
plt.xlabel('$x$') 
plt.grid(True) 

plt.show()