# Tutoriales de GMSH

<p align="center">
  <img src="https://gitlab.onelab.info/uploads/-/system/project/avatar/3/gmsh.png" height="100">
  <img src="https://anthoncode.com/wp-content/uploads/2019/01/python-logo-png.png" height="100">
</p>

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

### Tutorial 1: Conceptos básicos sobre creación de mallas

Video GMSH: [Tutorial 1 en Youtube](https://youtu.be/Jn4QbNt-lfU)

-  Malla formato `.geo`: [Malla_1.geo](/Mallas_GMSH/1_Malla-simple_2d.geo)

Video API de Python: [Tutorial 1 (Python) en Youtube](https://youtu.be/az4OATXyA9E)

- Malla formato `.py`: [Malla_1.py](/Mallas_python/1_Malla-simple_2d.py)

### Tutorial 2: Mallas estructuradas (Transfinite meshes)

Video GMSH + Python: [Tutorial malla estructurada en Youtube](https://youtu.be/8IrGJzqJ9SE)

- Malla formato `.geo`: [Malla_2.geo](/Mallas_GMSH/2_Malla-estructurada_2d.geo)
- Malla formato `.py`: [Malla_2.py](/Mallas_python/2_Malla-estructurada_2d.py)

### Tutorial 3: Mallas estructuradas extruidas (Extruded meshes)

Video GMSH + Python: [Tutorial malla extruida en Youtube](http://52.68.96.58)

- Malla formato `.geo`: [Malla_2.geo](/Mallas_GMSH/2_Malla-estructurada-extrude_2d.geo)
- Malla formato `.py`: [Malla_2.py](/Mallas_python/2_Malla-estructurada-extrude_2d.py)

## Recursos disponibles:
- El código [leer_GMSH.py](/leer_GMSH.py) contiene funciones útiles para procesar en Python las mallas creadas con el GMSH. Estas funciones permiten obtener la matriz de coordenadas nodales y la matriz de interconexión nodal a partir del archivo **.msh** que exporta GMSH con los datos de la malla. Adicionalmente, incluye una función para graficar las mallas a partir del archivo leído, con múltiples opciones de visualización. *(por ahora, solo permite leer y graficar mallas de elementos 2D y de tipo Shell, no mallas 3D)*.

- El código [obtener_grupos_fisicos.py](/obtener_grupos_fisicos.py) contiene una función que utiliza las funcionalidades de GMSH en Python para leer una malla a partir del archivo **.msh** exportado por GMSH y obtener de él los grupos físicos creados, con sus respectivos nombres (si los hay) y los nodos asociados a cada grupo físico. Muy útil para identificar nodos a los cuales se debe imponer una condición particular asociada al análisis por MEF, por ejemplo, condiciones de frontera del sólido o cargas puntuales/distribuidas aplicadas. *(Por ahora, solo permite leer mallas de elementos 2D y de tipo Shell, no mallas 3D)*.

### Ejemplo de uso:

Con el siguiente código se puede observar como utilizar las funciones dadas en [leer_GMSH.py](/leer_GMSH.py) para obtener los parámetros más importantes de la malla:

```
from leer_GMSH import xnod_from_msh, LaG_from_msh, plot_msh

malla = 'ejm_2.msh'

# Matriz de coordenadas nodales
xnod = xnod_from_msh(malla, dim=2)

# Se imprimen los primeros 10 nodos
for i in range(10):
    x, y = xnod[i]
    print(f'Nodo {i+1:2.0f}: x = {x:.4f}, y = {y:.4f}')

# Matriz de interconexión nodal
LaG = LaG_from_msh(malla)
nef = LaG.shape[0]

# Se imprimen los primeros 5 elementos y los 5 últimos:
print()
for e in list(range(5)) + list(range(nef-5, nef)):
    print(f'Elemento {e+1:3.0f}: Superficie = {LaG[e, 0]+1},   '
          f'Nodos = {LaG[e, 1:]+1}')


# Se grafica la malla:
plot_msh(malla, '2D', mostrar_nodos=True, mostrar_num_nodo=False, 
         mostrar_num_elem=True)
```

Esto da como resultado:
```
Nodo  1: x = 1.0000, y = 0.0000
Nodo  2: x = 3.2500, y = 0.0000
Nodo  3: x = 3.2500, y = 3.2500
Nodo  4: x = 0.0000, y = 3.2500
Nodo  5: x = 0.0000, y = 1.0000
Nodo  6: x = 0.7071, y = 0.7071
Nodo  7: x = 1.1500, y = 0.0000
Nodo  8: x = 1.3000, y = 0.0000
Nodo  9: x = 1.4500, y = 0.0000
Nodo 10: x = 1.6000, y = 0.0000

Elemento   1: Superficie = 1,   Nodos = [ 1  7 85 84]
Elemento   2: Superficie = 1,   Nodos = [84 85 86 83]
Elemento   3: Superficie = 1,   Nodos = [83 86 87 82]
Elemento   4: Superficie = 1,   Nodos = [82 87 88 81]
Elemento   5: Superficie = 1,   Nodos = [81 88 89 80]
Elemento 296: Superficie = 2,   Nodos = [332 333  70  71]
Elemento 297: Superficie = 2,   Nodos = [333 334  69  70]
Elemento 298: Superficie = 2,   Nodos = [334 335  68  69]
Elemento 299: Superficie = 2,   Nodos = [335 336  67  68]
Elemento 300: Superficie = 2,   Nodos = [336  52   5  67]
```
![grafico](/grafico_malla2.png)
