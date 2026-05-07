algebraic3d

# Box
solid Box = orthobrick (0, 0, 0; 2, 2, 2);

# Cylinder
solid Cylinder = cylinder (0, 0, 0; 0, 0, 1; 1);


# Domain
solid Domain = Box and not Cylinder;

tlo Domain -col=[0,1,0] -transparent;


