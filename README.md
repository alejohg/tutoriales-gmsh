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

Video GMSH + Python: [Tutorial malla extruida en Youtube](https://youtu.be/lppSadXC_T0)

- Malla formato `.geo`: [Malla_3.geo](/Mallas_GMSH/3_Malla-estructurada-extrude_2d.geo)
- Malla formato `.py`: [Malla_3.py](/Mallas_python/3_Malla-estructurada-extrude_2d.py)

### Tutorial 4: Mallas 2D utilizando Splines

Video GMSH + Python: [Tutorial malla con Splines en Youtube](http://52.68.96.58)

- Malla formato `.geo`: [Malla_4.geo](/Mallas_GMSH/7_Malla_con_splines.geo)
- Malla formato `.py`: [Malla_4.py](/Mallas_python/7_Malla_con_splines.py)


## Recursos disponibles:


### Funciones para leer la malla en Python:

El código [leer_GMSH.py](/leer_GMSH.py) contiene funciones útiles para procesar en Python las mallas creadas con el GMSH. Estas funciones permiten obtener la matriz de coordenadas nodales y la matriz de interconexión nodal a partir del archivo **.msh** que exporta GMSH con los datos de la malla. Adicionalmente, incluye una función para graficar las mallas a partir del archivo leído, con múltiples opciones de visualización. *(por ahora, solo permite leer y graficar mallas de elementos 2D y de tipo Shell, no mallas 3D)*.

**Ejemplo de uso:** Con el siguiente código se puede observar como utilizar las funciones dadas en [leer_GMSH.py](/leer_GMSH.py) para obtener los parámetros más importantes de la malla:

```python
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

### Funciones para leer grupos físicos en la malla

El código [obtener_grupos_fisicos.py](/obtener_grupos_fisicos.py) contiene una función que utiliza las funcionalidades de GMSH en Python para leer una malla a partir del archivo **.msh** exportado por GMSH y obtener de él los grupos físicos creados, con sus respectivos nombres (si los hay) y los nodos asociados a cada grupo físico. Muy útil para identificar nodos a los cuales se debe imponer una condición particular asociada al análisis por MEF, por ejemplo, condiciones de frontera del sólido o cargas puntuales/distribuidas aplicadas. Con este propósito, contiene otra función que permite directamente obtener los nodos asociados a un grupo físico específico conociendo el nombre. *(Por ahora, solo permite leer mallas de elementos 2D y de tipo Shell, no mallas 3D)*.

**Ejemplo de uso:** En el siguiente código se puede observar cómo utilizar estas funciones para obtener todos los parámetros de los grupos físicos que se tienen en una malla

```python
from obtener_grupos_fisicos import grupos_fisicos, obtener_nodos

malla = 'scordelis.msh'

# Obtener todos los grupos físicos de la malla:
dict_nombres, dict_nodos = grupos_fisicos(malla)
print('Grupos físicos reportados:\n')
for tag in dict_nombres.keys():
    dim    = dict_nombres[tag][0]
    nombre = dict_nombres[tag][1]
    nodos  = dict_nodos[tag]
    print(f'Grupo físico: {tag}\nDimensión: {dim}\n'
          f'Nombre: {nombre}\nContiene nodos: {nodos}.\n')

# Obtener nodos únicamente del grupo físico llamado "AB":
nod_AB = obtener_nodos(malla, 'AB')
print('~'*50)
print(f'Grupo físico "AB" contiene nodos: {nod_AB}')
```

Esto da como resultado:

```
Grupos físicos reportados:

Grupo físico: 1
Dimensión: 1
Nombre: AB
Contiene nodos: [23 24 20 19 21  3  1 22 25].

Grupo físico: 2
Dimensión: 1
Nombre: BC
Contiene nodos: [12 16  4 15 13 14 17 18  3].

Grupo físico: 3
Dimensión: 1
Nombre: CD
Contiene nodos: [28  4 30 26 29 31  2 27 32].

Grupo físico: 4
Dimensión: 1
Nombre: AD
Contiene nodos: [ 5  8  9  7 10 11  2  1  6].

Grupo físico: 101
Dimensión: 2
Nombre: mi superficie
Contiene nodos: [78 74 70 77 71 66 72 76 63 64 69 79 80 60 67 75 65 73 61 62 81 68 28 39
 49  5  8 12 16 23 50 37  4 41 24 30 51 52 54  9 56 57 15 58  7 20 19 26
 29 40 43 13 55 10 31 53 59 14 17 11 18  2 21 27 34 35 32 36 42 38 47  3
 33 44  1 48 45 46  6 22 25].

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Grupo físico "AB" contiene nodos: [22  1 24  3 23 20 25 19 21]
```