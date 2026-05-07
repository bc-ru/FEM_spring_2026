import matplotlib.pyplot as plt
import numpy as np 
from scipy.special import legendre
from scipy import integrate
from scipy.linalg import solve_banded
 
def f(x):
    return 1./(1.+25*x**2)  
def pk(x, k, xi):
    h1 = 1/(xi[1]-xi[0])
    g = 0.        
    if k == 0:
        if x < xi[1]:
            g = h1*(xi[1]-x)
        return g
    if k == len(xi)-1:
        if x >xi[k-1]:
            g = h1*(x-xi[k-1])
        return g   
    if k > 0 and k < len(xi)-1:
        if x > xi[k-1] and x < xi[k]:
            g = h1*(x-xi[k-1])  
        if x >= xi[k] and x < xi[k+1]:
            g = h1*(xi[k+1]-x)                 
        return g   
ff = lambda x : 1./(1.+25*x**2)*pk(x, k, xi)      
    
ni = 15
xi = np.linspace(-1.,1.,ni)
y0 = np.zeros((ni), "float")  
fk = np.zeros((ni), 'float')
    
for k in range(0, ni): 

    aa, err = integrate.quad(ff, -1., 1.)  
    fk[k] = aa
    print (fk[k], err, aa)   

A = np.zeros((ni,ni), 'float')
for k in range(0, ni):
    kk0 = lambda x : pk(x, k, xi)*pk(x, k, xi)
    A[k,k], err = integrate.quad(kk0, -1, 1)  
    if k > 0:
        kk1 = lambda x : pk(x, k, xi)*pk(x, k-1, xi)
        A[k,k-1], err = integrate.quad(kk1, -1, 1)  
    if k < ni-1:
        kk2 = lambda x : pk(x, k, xi)*pk(x, k+1, xi)
        A[k,k+1], err = integrate.quad(kk2, -1, 1)   
        
# ck =  np.linalg.solve(A, fk)

Ab = np.zeros((3,ni), 'float')
for k in range(0, ni):
    Ab[1,k] = A[k,k]
    if k > 0:
        Ab[0,k] =  A[k-1,k]
    if k < ni-1:
        Ab[2,k] =  A[k,k+1]
print(Ab)
ck = solve_banded((1, 1), Ab, fk)  

print(ck)

N = 500
xx = np.linspace(-1.,1.,N) 
yy = np.linspace(-1.,1.,N)  
fe = f(xx)     

for j in range(0, N): 
    s = 0.     
    for k in range(0, ni): 
        s = s + ck[k]*pk(xx[j], k, xi)  
    yy[j] = s 

fig2 = plt.figure(2)
ss = "$n = $" + str(ni-1) 
plt.title(ss)
plt.scatter(xi, y0)  
plt.plot(xx, fe) 
plt.plot(xx, yy)     
plt.xlabel('$x$') 
plt.grid(True) 

plt.show()
