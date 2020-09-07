//---------------------------------------------------------------------
// Ejemplo 6: Malla de elementos Shell de un paraboloide hiperbólico

// Por: Alejandro Hincapié G.
//---------------------------------------------------------------------
N = 8; // Malla estructurada de 2N x N elementos

//---------------------------------------------------------------------
// La superficie a generar es el paraboloide hiperbólico definido por
// la función f(x, y) = y^2 - x^2 en los intervalos 0 <= x <= 1/2 y
// -1/2 <= y <= 1/2.
//---------------------------------------------------------------------
// Para generar la superficie se deben crear sus 4 bordes que están
// definidos por ciertas parábolas de la forma f(x) = ax^2+bx+c:

//---------------------------------------------------------------------
// Lado AB: Parábola z = y^2 - 1/4
//---------------------------------------------------------------------
a = 1; b = 0; c = -1/4;
x = 1/2; // Esta parábola está sobre el plano x=1/2

y1 = -1/2; y2 = 1/2; // Coordenadas inicial y final en Y

plano = 2; // La variable plano será: 1 para xz o 2 para yz

// Se crean puntos inicial y final de esta parábola
pA = newp; Point(pA) = {x, y1, y1^2-x^2};
pB = newp; Point(pB) = {x, y2, y2^2-x^2};

//---------------------------------------------------------------------
// Se crea una macro para convertir la parábola en una curva de Bezier:

Macro obtener_pc_bezier
	// A diferencia de Python, en el lenguaje del GMSH no se pueden
	// crear funciones que tomen argumentos, en su lugar se deben crear
	// Macros que toman y crean variables globales en el programa
	//-----------------------------------------------------------------
	// Ésta usa los parámetros de una parábola f(x) = ax^2+bx+c o
	// f(y) = ay^2 + by + c y obtiene el punto de control que permite
	// dibujarla como una curva de Bezier de 3 puntos

	If (plano == 2) // Si la parábola está en plano YZ
		Cy = (y1+y2)/2;
		Cz = (y2-y1)/2 * (2*a*y1 + b) + (a*y1^2+b*y1+c);
	Else  // Si la parábola está en plano XZ
		Cx = (x1+x2)/2;
		Cz = (x2-x1)/2 * (2*a*x1 + b) + (a*x1^2+b*x1+c);
	EndIf

Return
//---------------------------------------------------------------------

Call obtener_pc_bezier; // Llamando la Macro obtenemos punto de control

pc1 = newp; Point(pc1) = {x, Cy, Cz};
Bezier(1) = {pA, pc1, pB};

//---------------------------------------------------------------------
// Lado BC (parábola z = 1/4 - x^2)
//---------------------------------------------------------------------
a = -1; b = 0; c = 1/4;
y = 1/2; // Esta parábola está sobre el plano y = 1/2

x1 = 1/2; x2 = 0;
plano = 1;

pC = newp; Point(pC) = {x2, y, y^2-x2^2};

Call obtener_pc_bezier;

pc2 = newp; Point(pc2) = {Cx, y, Cz};
Bezier(2) = {pB, pc2, pC};

//---------------------------------------------------------------------
// Lado CD (parábola z = y^2)
//---------------------------------------------------------------------
a = 1; b = 0; c = 0;
x = 0; // Esta parábola está sobre el plano x=0

y1 = 1/2; y2 = -1/2;
plano = 2; // Plano yz

pD = newp; Point(pD) = {x, y2, y2^2-x^2};

Call obtener_pc_bezier;

pc3 = newp; Point(pc3) = {x, Cy, Cz};
Bezier(3) = {pC, pc3, pD};

//---------------------------------------------------------------------
// Lado AD (parábola z = 1/4-x^2)
//---------------------------------------------------------------------
a = -1; b = 0; c = 1/4;
y = -1/2; // Esta parábola está sobre el plano y = 1/2

x1 = 0; x2 = 1/2;
plano = 1; // Plano xz

Call obtener_pc_bezier;

pc4 = newp; Point(pc4) = {Cx, y, Cz};
Bezier(4) = {pD, pc4, pA};

//---------------------------------------------------------------------
// Se crea la superficie
//---------------------------------------------------------------------
Curve Loop(1) = {1, 2, 3, 4};
Surface(1) = {1};
Physical Surface("ABCD") = {1};
//---------------------------------------------------------------------
// Se define la malla como estructurada
//---------------------------------------------------------------------
Transfinite Curve{1, 3} = 2*N + 1;
Transfinite Curve{2, 4} = N + 1;

Transfinite Surface{1};

//---------------------------------------------------------------------
// Se crea y guarda la malla
//---------------------------------------------------------------------
Mesh 2;
Save "paraboloide.msh";

General.Axes = 1;      // Mostrar ejes de coordenadas simples
Mesh.SurfaceFaces = 1; // Ver las "caras de los EF 2D
