// Ejemplo 4: Malla shell en GMSH

// Variables de la geometría

L = 25;        // Longitud del cascarón
r = 25;        // radio de la superficie
t = 40*Pi/180; // Ángulo de apertura
N = 8;         // Tamaño de la malla (N x N)


Point(0) = {0, 0, 0}; // Punto central del arco

// Se crean dos puntos que definan el arco

Point(1) = {r*Sin(t), 0, r*Cos(t), 1};
Point(2) = {0, 0, r, 1};

// Se crea el arco y se define el núm. de nodos que tendrá

Circle(1) = {1, 0, 2};
Transfinite Line{1} = N+1;


// Al extruir este arco se genera la superficie

superf[] = Extrude {0, L, 0} {
           Curve{1}; Layers{N};
           };

// Se obtienen tags de: borde derecho, superficie, borde superior y borde inferior
// (el borde izquierdo lógicamente es la curva 1)

bd =  superf[0]; // Borde derecho
s  =  superf[1]; // Superficie generada
bs =  superf[2]; // Borde superior
bi = -superf[3]; // Borde inferior 
 
Printf("bs = %g, s=%g, bs=%g, bi=%g", bd, s, bs, bi);

Physical Line("AB") = {bi};
Physical Line("BC") = {bd};
Physical Line("CD") = {bs};
Physical Line("AD") = {1};
Physical Surface("ABCD") = {s};

Transfinite Surface{s}; // Malla 2D estructurada
Recombine Surface{s};   // Usar EF cuadriláteros

Mesh 2;
Mesh.SurfaceFaces = 1;
Mesh.Points = 1;
General.Axes = 1; // Para que aparezcan los ejes en la interfaz

Save "ejm_4.msh";