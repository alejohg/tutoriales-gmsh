//-----------------------------------------------------------------------------------
// Malla para el perfil de un ala (Airfoil) usando B-Splines en GMSH
// 
// Por: Alejandro Hincapié G.
//-----------------------------------------------------------------------------------

L = 1;  // Longitud desde el centro de la malla interior hasta los bordes

//-----------------------------------------------------------------------------------
// Se crean los puntos de control de la Spline:
//-----------------------------------------------------------------------------------
Point(1)  = {1, 0, 0};
Point(2)  = {0.8, 0.027, 0};
Point(3)  = {0.55, 0.058, 0};
Point(4)  = {0.3, 0.08, 0};
Point(5)  = {0.15, 0.078, 0};
Point(6)  = {0, 0.052, 0};
Point(7)  = {0, 0, 0};
Point(8)  = {0, -0.01, 0};
Point(9)  = {0.15, -0.052, 0};
Point(10) = {0.3, -0.05, 0};
Point(11) = {0.55, -0.043, 0};
Point(12) = {0.8, -0.017, 0};

//-----------------------------------------------------------------------------------
// Se crea la B-Spline con tomando los puntos anteriores como puntos de control
//-----------------------------------------------------------------------------------
af = newl; BSpline(af) = {1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 1};

Transfinite Curve(af) = 301; // Refinamos malla en el contorno del airfoil para adaptar a la curvatura

cint = newll; Curve Loop(cint) = {af};  // Curve loop interior


//-----------------------------------------------------------------------------------
// Se crea el contorno de la superficie exterior
//-----------------------------------------------------------------------------------
p1 = newp; Point(p1) = {0.5-L, -L, 0};
p2 = newp; Point(p2) = {0.5+L, -L, 0};
p3 = newp; Point(p3) = {0.5+L, L, 0};
p4 = newp; Point(p4) = {0.5-L, L, 0};

l1 = newl; Line(l1) = {p1, p2};
l2 = newl; Line(l2) = {p2, p3};
l3 = newl; Line(l3) = {p3, p4};
l4 = newl; Line(l4) = {p4, p1};

cext = newll; Curve Loop(cext) = {l1, l2, l3, l4};  // Curve loop exterior

//-----------------------------------------------------------------------------------
// Se generan ambas superficies
//-----------------------------------------------------------------------------------
s1 = news; Plane Surface(s1) = {cext, cint};  // Superficie que define el aire
s2 = news; Plane Surface(s2) = {cint}; // Superficie que define el airfoil 

//-----------------------------------------------------------------------------------
// Se crean puntos auxiliares para controlar tamaño de malla interior:
//-----------------------------------------------------------------------------------
x = 0.1;


For i In {1:0.8/0.05 + 1}
    paux = newp; Point(paux) = {x, 0, 0, 0.5};
    Point{paux} In Surface{s2};
    x += 0.05;
EndFor


Physical Surface("Aire")    = {s1};
Physical Surface("Airfoil") = {s2};

//-----------------------------------------------------------------------------------
// Finalmente se crea la malla y se guarda:
//-----------------------------------------------------------------------------------

Mesh 2;

SetOrder 2; // Creamos una malla con elementos de orden 2:

Save "airfoil.msh";

Mesh.SurfaceFaces = 1;
Mesh.Points = 1;
Mesh.HighOrderOptimize = 2;
