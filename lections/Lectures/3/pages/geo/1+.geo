SetFactory("OpenCASCADE");

// шаг сетки
h  = 0.5;
hh = h/5;

// точки для прямоугольника
Point(1) = {0,0,0,h};
Point(2) = {0,4,0,h};
Point(3) = {8,4,0,h};
Point(4) = {8,0,0,h};

// точки для круга
Point(5) = {2,2,0,hh};
Point(6) = {1,2,0,hh};
Point(7) = {2,3,0,hh};
Point(8) = {3,2,0,hh};
Point(9) = {2,1,0,hh};

// линии прямоугольника
Line(1) = {1,2};
Line(2) = {2,3};
Line(3) = {3,4};
Line(4) = {4,1};

// линии окружности
Circle(5) = {6,5,7};
Circle(6) = {7,5,8};
Circle(7) = {8,5,9};
Circle(8) = {9,5,6};

// контуры
Line Loop(11) = {1,2,3,4};
Line Loop(12) = {5,6,7,8};

// поверхности
Plane Surface(21) = {11,12}; // прямоугольник с дыркой
Plane Surface(22) = {12};    // круг

// физические группы
Physical Line(1) = {1};
Physical Line(2) = {2,3,4};

Physical Surface(1) = {21};
Physical Surface(2) = {22};

// ЦВЕТА — синтаксис без ошибок
Color 200,200,255 { Surface{21}; }
Color 255,100,100 { Surface{22}; }

// Для корректной заливки
Mesh 2;
