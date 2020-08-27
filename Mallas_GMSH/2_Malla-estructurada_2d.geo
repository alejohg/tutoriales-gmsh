// Ejm 2: Malla estructurada

// Variables asociadas a la geometría
L = 6.5/2;
r = 1;

// Puntos:
pc = newp; Point(pc) = {0, 0, 0}; // Punto central del círculo
p1 = newp; Point(p1) = {r, 0, 0};
p2 = newp; Point(p2) = {L, 0, 0};
p3 = newp; Point(p3) = {L, L, 0};
p4 = newp; Point(p4) = {0, L, 0};
p5 = newp; Point(p5) = {0, r, 0};
p6 = newp; Point(p6) = {r*Cos(Pi/4), r*Sin(Pi/4), 0};

// Líneas:
l1 = newl; Line(l1) = {p1, p2};
l2 = newl; Line(l2) = {p2, p3};
l3 = newl; Line(l3) = {p3, p4};
l4 = newl; Line(l4) = {p4, p5};
l5 = newl; Line(l5) = {p3, p6};
c1 = newc; Circle(c1) = {p5, pc, p6};
c2 = newc; Circle(c2) = {p6, pc, p1};

// Curve Loops:
cl1 = newll; Curve Loop(cl1) = {l1, l2, l5, c2};
cl2 = newll; Curve Loop(cl2) = {-l5, l3, l4, c1};

// Superficies:
s1 = news; Plane Surface(s1) = {cl1};
s2 = news; Plane Surface(s2) = {cl2};

Physical Surface("Mi superficie") = {s1, s2};

// Queremos una malla estructurada con m elementos en las líneas perpendiculares al círculo
// y n elementos en las otras
m = 15;
n = 10;

Transfinite Curve{c1, l3, c2, l2} = n+1; // Definimos m+1 nodos en líneas perpendiculares al círculo

Transfinite Curve{l1, l5, l4} = m+1;     // Definimos n+1 nodos en las demás líneas

Transfinite Surface{s1, s2}; // Usar malla 2D estructurada
Recombine Surface{s1, s2}; // Para usar elementos cuadriláteros en vez de triángulos

Mesh.SurfaceFaces = 1;
Mesh.Points = 1;

Mesh 2;

Save "ejm_2.msh";
