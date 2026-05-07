import matplotlib.pyplot as plt
import numpy as np 
from fenics import *
#from numpy import array

m = 5
p = 2

a = -1.
b = 1.

mesh = IntervalMesh(m, a, b)
xm = mesh.coordinates()
ym = np.zeros((m+1), "float") 

V = FunctionSpace(mesh, "CG", p)
tree = mesh.bounding_box_tree()
n = V.dim()-1

# Evaluate the i-th basis function at point x:
def basis_func(i,x):
    cell_index = tree.compute_first_entity_collision(Point(*x))
    cell_global_dofs = V.dofmap().cell_dofs(cell_index)
    for local_dof in range(0,len(cell_global_dofs)):
        if(i==cell_global_dofs[local_dof]):
            cell = Cell(mesh, cell_index)
            values = np.array([0,])
            return V.element().evaluate_basis(local_dof,x,
                                              cell.get_vertex_coordinates(),
                                              cell.orientation())
    return 0.0

xn = np.linspace(a, b, n+1) 
yn = np.zeros((n+1), "float")   

N = 500
xx = np.linspace(a, b, N) 
yy = np.linspace(a, b, N)  

for i in range(0, N): 
    yy[i]  = basis_func(7, np.array([xx[i]],))
          
fig1 = plt.figure(1)
ss = "$m = $" + str(m) + "$, \ p = $" + str(p)
plt.title(ss)

plt.scatter(xn, yn)  
plt.scatter(xm, ym)  
plt.plot(xx, yy)  
    
plt.xlabel('$x$') 
plt.grid(True) 

plt.show()