algebraic3d

# Box
solid Box = orthobrick (0, 0, 0; 8, 4, 2);

# Ball
solid Ball = sphere (2, 2, 2; 1);

# Domain
solid Domain = Box and not Ball;

# tlo Box - col=[0,0,1];
tlo Ball - col=[1,0,0];
tlo Domain -col=[0,1,0] -transparent;


