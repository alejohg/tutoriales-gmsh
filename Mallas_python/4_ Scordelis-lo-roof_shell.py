# -*- coding: utf-8 -*-
"""
Ejemplo 4: Malla shell en GMSH

Por: Alejandro Hincapié G.
"""

import gmsh
from math import sin, cos, radians

# %% Se inicializa y se crea el modelo:

gmsh.initialize()

gmsh.option.setNumber("General.Terminal", 1)

gmsh.model.add("modelo_3")


# %% Se crean algunas variables de la geometría:

L = 25           # Longitud del cascarón
r = 25           # radio de la superficie
t = radians(40)  # Ángulo de apertura
N = 8            # Tamaño de la malla (N x N)

# %% La siguiente línea permite abreviar el código:
geom = gmsh.model.geo

# %% Se crean los puntos necesarios
geom.addPoint(0, 0, 0, tag=0)
geom.addPoint(r*sin(t), 0, r*cos(t), tag=1)
geom.addPoint(0, 0, r, tag=2)

# %% Se crea el arco de circunferencia:

geom.addCircleArc(1, 0, 2, tag=3)
# Dado que queremos una malla estructurada, definimos el número de elementos
# que queremos en la línea creada:
# Sintaxis: gmsh.model.geo.mesh.setTransfiniteCurve(tags, # nodos)

geom.mesh.setTransfiniteCurve(3, N+1)  # El número de nodos será N+1


# %% Para crear la superficie se debe extruir el arco anterior:
#    Sintaxis: gmsh.model.geo.extrude([lista de entidades], u, v, w), donde:
#              La lista de entidades consiste en pares (dim, tag)
#              u, v, w son las componentes del vector de traslación
superf = geom.extrude([(1,3)], 0, L, 0, numElements=[N])

# el comando anterior retorna una lista, analicemos de qué se compone:

for i in range(len(superf)):
    print(f'superf[{i}] = {superf[i]}')

# La superficie generada es el segundo elemento de la lista anterior
bd, s, bs, bi = superf


# %% Creamos los grupos físicos:

# Bordes físicos: AB, BC, CD y AD:
tags_bordes = 'AB BC CD AD'.split()
bordes = [bi[1], bd[1], bs[1], 3]
for i in range(len(tags_bordes)):
    gmsh.model.addPhysicalGroup(1, [bordes[i]], i+1)
    gmsh.model.setPhysicalName(1, i+1, tags_bordes[i])

# Verificamos si los grupos físicos fueron creados adecuadamente:
grupos = gmsh.model.getPhysicalGroups(dim=1)
print('\nGrupos físicos de dimensión 1:')
for i in range(len(grupos)):
    grupo = grupos[i][1]
    nombre = gmsh.model.getPhysicalName(1, grupo)
    curvas_grupo = gmsh.model.getEntitiesForPhysicalGroup(1, grupo)
    
    print(f'\nGrupo físico: {grupo}\nNombre: {nombre}\n'
          f'Contiene las curvas: {curvas_grupo}')


# Superficie física:
gmsh.model.addPhysicalGroup(s[0], [s[1]], 101)
gmsh.model.setPhysicalName(2, 101, 'mi superficie')

# %% Definimos que la superficie creada tenga una malla estructurada:
geom.mesh.setTransfiniteSurface(s[1])

# Y recombinamos para que use elementos cuadriláteros en lugar de triángulos
geom.mesh.setRecombine(2, s[1])

# %% Finalmente se crea la malla y se guarda:

geom.synchronize()
gmsh.model.mesh.generate(2)

filename = 'scordelis.msh'
gmsh.write(filename)

# Si queremos que en la visualización se muestren los ejes de coordenadas, po-
# demos modificar esta opción, tomado del manual:
# =============================================================================
#  General.Axes
#  Axes (0: none, 1: simple axes, 2: box, 3: full grid, 4: open grid, 5: ruler)
#  Default value: 0
# =============================================================================
gmsh.option.setNumber('General.Axes', 1)  # 1 para "ejes simples"

# Visualizamos el resultado en la interfaz gráfica de GMSH
gmsh.fltk.run()

# Se finaliza el programa
gmsh.finalize()

# %% Graficamos la malla:

from leer_GMSH import plot_msh  # Funciones para leer y graficar la malla

#plot_msh(filename, 'shell', True, True, True)
