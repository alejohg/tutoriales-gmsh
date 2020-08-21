# Tutoriales de GMSH

El propósito de este repositorio es albergar los códigos utilizados en los tutoriales de GMSH (próximamente, pendiente zelda :v).

En estos tutoriales se busca explicar el uso del software libre [GMSH](https://gmsh.info) para la creación de mallas de elementos finitos en 2D, desde los conceptos más básicos hasta algunos aspectos un poco más avanzados que permitan adaptar el uso del programa a las necesidades del usuario, según la malla que desee crear o en función del problema específico que desee modelar.

Los temas cubiertos en estos tutoriales son:
- Pendiente
- Pendiente x2

## Recursos disponibles:
- El código [leer_GMSH.py](/leer_GMSH.py) contiene funciones útiles para procesar en Python las mallas creadas con el GMSH. Estas funciones permiten obtener la matriz de coordenadas nodales y la matriz de interconexión nodal a partir del archivo **.msh** que exporta GMSH con los datos de la malla. Adicionalmente, incluye una función para graficar las mallas a partir del archivo leído, con múltiples opciones de visualización. *(por ahora, solo permite leer y graficar mallas de elementos 2D y de tipo Shell, no mallas 3D)*.

- El código [obtener_grupos_fisicos.py](/obtener_grupos_fisicos.py) contiene una función que utiliza las funcionalidades de GMSH en Python para leer un una malla a partir de un archivo **.msh** y obtener de él los grupos físicos creados, con sus respectivos nombres (si los hay) y los nodos asociados a cada grupo físico. Muy útil para identificar nodos ca los cuales se debe imponer una condición particular asociada al análisis por MEF, por ejemplo, condiciones de frontera del sólido o cargas puntuales/distribuidas aplicadas. *(Por ahora, solo permite leer mallas de elementos 2D y de tipo Shell, no mallas 3D)*.
