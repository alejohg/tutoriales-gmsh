// Ejemplo 3: Programa para crear una malla estructurada sencilla usando la función 'extrude'.
// Por: Alejandro Hincapie G.


Point(1) = {0, 0, 0}; // Se crea un punto en origen de coordenadas

// Al extruir el punto se genera una línea. El argumento Layers permite definir cuántos elementos
// queremos a lo largo de esta línea

l_ext1[] = Extrude {0, 20, 0} {
		   Point{1}; Layers{10};};

l1 = l_ext1[1]; // Se extrae la etiqueta de la línea generada al extruir el punto 1
n = #l_ext1[];  // Número de elementos de la lista generada

Printf("Extrusión punto 1:");
For i In {0:n-1}
	Printf("l_ext1[%g] = %g", i, l_ext1[i]);
EndFor

// Ahora extruimos la línea anterior para generar una superficie. El argumento Recombine permite
// que en la superficie generada la malla conste de elementos cuadriláteros en lugar de triángulos

s_ext1[] = Extrude {40, 0, 0} {
	       Curve{l1}; Layers{20}; Recombine;};

Printf(" ");
Printf("Extrusión línea l1:");

For i In {0:#s_ext1[]-1}
    Printf("s_ext1[%g] = %g", i, s_ext1[i]);
EndFor

s1 = s_ext1[1];  // Se extrae la etiqueta de la superficie generada al extruir

Physical Surface("Superficie 1") = {s1};


//-------------------------------------------------------------------------------------------------
// Crear malla usando función Extrude alrededor de un eje de rotación
//-------------------------------------------------------------------------------------------------

p1 = newp; Point(p1) = {50, 0, 0};
l_ext2[] = Extrude {15, 0, 0} {Point{p1}; Layers{10};};

l2 = l_ext2[1];

// Ahora usamos la función 'Extrude' para generar la superficie

s_ext2[] = Extrude {{0, 0, 1}, {45, 0, 0}, Pi/2} {
	       Curve{l2}; Layers{15}; Recombine;};

s2 = s_ext2[1];

Physical Surface("Superficie 2") = {s2};


// Ajustes finales de la malla		   
Mesh 2;                         // Generar la malla 2D
SetOrder 2;                     // Se definen elementos finitos de orden 2
Mesh.SecondOrderIncomplete = 1; // Usar elementos finitos serendípitos (incompletos)
Mesh.SurfaceFaces = 1;          // Ver las "caras" de los elementos finitos 2D
Mesh.Points = 1;                // Ver los nodos de la malla
Save "extrude.msh";
