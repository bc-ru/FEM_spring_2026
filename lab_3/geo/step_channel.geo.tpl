// Backward-facing step channel geometry for Gmsh
// Parameters are substituted by geo/generate_geo.py
SetFactory("OpenCASCADE");

L = {L};      // downstream channel length
H = {H};      // upper channel height above y=0
l = {l};      // upstream inlet length
h = {h};      // step depth below y=0
lc = {lc};    // characteristic mesh size
lc_step = {lc_step};

// Domain polygon:
// (-l,0) -> (0,0) -> (0,-h) -> (L,-h) -> (L,H) -> (-l,H)
Point(1) = {{-l, 0, 0, lc}};
Point(2) = {{ 0, 0, 0, lc_step}};
Point(3) = {{ 0,-h, 0, lc_step}};
Point(4) = {{ L,-h, 0, lc}};
Point(5) = {{ L, H, 0, lc}};
Point(6) = {{-l, H, 0, lc}};

Line(1) = {{1, 2}}; // lower upstream wall
Line(2) = {{2, 3}}; // vertical step wall
Line(3) = {{3, 4}}; // lower downstream wall
Line(4) = {{4, 5}}; // outlet
Line(5) = {{5, 6}}; // upper wall
Line(6) = {{6, 1}}; // inlet

Curve Loop(1) = {{1, 2, 3, 4, 5, 6}};
Plane Surface(1) = {{1}};

// Physical IDs used by FEniCS code.
// Keep these IDs synchronized with solver/problem.py.
Physical Surface("domain", 1) = {{1}};
Physical Curve("wall_lower", 11) = {{1, 2, 3}};
Physical Curve("wall_top",   12) = {{5}};
Physical Curve("inlet",      13) = {{6}};
Physical Curve("outlet",     14) = {{4}};
Physical Curve("step",       15) = {{2}};

Mesh.CharacteristicLengthMin = lc_step;
Mesh.CharacteristicLengthMax = lc;
Mesh.Algorithm = 6;
