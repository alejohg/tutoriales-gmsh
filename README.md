# Tutoriales de GMSH

El propósito de este repositorio es albergar los códigos utilizados en los [tutoriales de GMSH](https://www.youtube.com/playlist?list=PLu42Gwp4NwSutpf8S_B6mX_vNgETAXtMs) que subí a Youtube.

En estos tutoriales se busca explicar el uso del software libre [GMSH](https://gmsh.info) para la creación de mallas de elementos finitos en 2D, desde los conceptos más básicos hasta algunos aspectos un poco más avanzados que permitan adaptar el uso del programa a las necesidades del usuario, según la malla que desee crear o en función del problema específico que desee modelar.

Los temas cubiertos en estos tutoriales son:
- Conceptos básicos sobre creación de mallas 2D en GMSH
- Mallas estructuradas 2D en GMSH
- Uso del lenguaje del GMSH para crear mallas
- Uso de la API de GMSH en Python para crear mallas
- Mallas de elementos Shell (cascarón) estructuradas y no estructuradas
- Curvas especiales: B-Splines y Bezier 

## Videotutoriales en Youtube

Cada uno de los tutoriales se basa en crear una cierta malla de elementos finitos en la cual se apliquen conceptos básicos o avanzados del software. Los archivos correspondientes a estas mallas se encuentran disponibles tanto en formato Python `.py` como en formato GMSH `.geo`

### Tutorial 1:

Video GMSH: [Tutorial 1 en Youtube](https://youtu.be/FnHi9RWYqWM)

-  Malla formato `.geo`: [Malla 1.geo](/Mallas_GMSH/1_Malla-simple_2d.geo)

Video API de Python: [Tutorial 1 (Python) en Youtube](https://youtu.be/C1O5KMPl1u0)

- Malla formato `.py`: [Malla 1.py](/Mallas_python/1_Malla-simple_2d.py)


## Recursos disponibles:
- El código [leer_GMSH.py](/leer_GMSH.py) contiene funciones útiles para procesar en Python las mallas creadas con el GMSH. Estas funciones permiten obtener la matriz de coordenadas nodales y la matriz de interconexión nodal a partir del archivo **.msh** que exporta GMSH con los datos de la malla. Adicionalmente, incluye una función para graficar las mallas a partir del archivo leído, con múltiples opciones de visualización. *(por ahora, solo permite leer y graficar mallas de elementos 2D y de tipo Shell, no mallas 3D)*.

- El código [obtener_grupos_fisicos.py](/obtener_grupos_fisicos.py) contiene una función que utiliza las funcionalidades de GMSH en Python para leer una malla a partir del archivo **.msh** exportado por GMSH y obtener de él los grupos físicos creados, con sus respectivos nombres (si los hay) y los nodos asociados a cada grupo físico. Muy útil para identificar nodos a los cuales se debe imponer una condición particular asociada al análisis por MEF, por ejemplo, condiciones de frontera del sólido o cargas puntuales/distribuidas aplicadas. *(Por ahora, solo permite leer mallas de elementos 2D y de tipo Shell, no mallas 3D)*.
