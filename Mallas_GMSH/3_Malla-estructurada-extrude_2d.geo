// Ejemplo 3: Programa para crear una malla estructurada sencilla usando la función 'extrude'.

Point(1) = {0, 0, 0}; // Se crea un punto en origen de coordenadas

// Al extruir el punto se genera una línea. El argumento Layers permite definir cuántos elementos
// queremos a lo largo de esta línea

linea[] = Extrude {0, 20, 0} {
		  Point{1}; Layers{10};};

l1 = linea[1]; // Se extrae la etiqueta de la línea generada al extruir el punto 1


// Ahora extruimos la línea anterior para generar una superficie. El argumento Recombine permite
// que en la superficie generada la malla conste de elementos cuadriláteros en lugar de triángulos

superf[] = Extrude {40, 0, 0} {
		   Curve{l1}; Layers{20}; Recombine;};

s1 = superf[1];  // Se extrae la etiqueta de la superficie generada al extruir


Physical Surface("Mi superficie") = {s1};

Mesh 2;
SetOrder 2;                     // Se definen elementos finitos de orden 2
Mesh.SecondOrderIncomplete = 1; // Usar elementos finitos serendípitos (incompletos)
Mesh.SurfaceFaces = 1;          // Ver las "caras" de los elementos finitos 2D
Mesh.Points = 1;                // Ver los nodos de la malla
Save "ejm_3.msh";
