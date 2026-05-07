import matplotlib.pyplot as plt
import numpy as np 

def f(x,y):
    return (1-(x**2+y**3))*np.exp(-(x**2+y**2)/2)
    
N = 200
x = np.linspace(-3,3,N)
y = np.linspace(-3,3,N)
yy  = np.zeros((N,N)) 

for i in range(0, N): 
    for j in range(0, N): 
        yy[j,i]  = f(x[i], y[j])
          
fig1 = plt.figure(1)
plt.contourf(x,y,yy, cmap='binary')
plt.gca().set_aspect("equal")
plt.colorbar()
plt.savefig('f-7.12.png', format="png", dpi=600)
plt.show()