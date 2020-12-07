# -*- coding: utf-8 -*-
"""
Ejemplo: Malla shell en GMSH

Por: Alejandro Hincapié G.
"""

import gmsh
from math import sin, cos, radians

# %% Se inicializa y se crea el modelo:

gmsh.initialize()

gmsh.option.setNumber("General.Terminal", 1)

gmsh.model.add("modelo_shell")


# %% Se crean algunas variables de la geometría:

L = 25           # Longitud del cascarón
r = 25           # radio de la superficie
t = radians(40)  # Ángulo de apertura
N = 8            # Tamaño de la malla (N x N)

# %% La siguiente línea permite abreviar el código:
geom = gmsh.model.geo

# %% Se crean los puntos necesarios
geom.addPoint(0, 0, 0, tag=0)  # Punto central del arco
geom.addPoint(r*sin(t), 0, r*cos(t), tag=1)
geom.addPoint(0, 0, r, tag=2)

# %% Se crea el arco de circunferencia:

geom.addCircleArc(1, 0, 2, tag=1)
# Dado que queremos una malla estructurada, definimos el número de elementos
# que queremos en la línea creada:
# Sintaxis: gmsh.model.geo.mesh.setTransfiniteCurve(tags, # nodos)

geom.mesh.setTransfiniteCurve(1, N+1)  # El número de nodos será N+1


# %% Para crear la superficie se debe extruir el arco anterior:
#    Sintaxis: gmsh.model.geo.extrude([lista de entidades], u, v, w), donde:
#              La lista de entidades consiste en pares (dim, tag)
#              u, v, w son las componentes del vector de traslación
superf = geom.extrude([(1,1)], 0, L, 0, numElements=[N])

# el comando anterior retorna una lista, analicemos de qué se compone:

for i in range(len(superf)):
    print(f'superf[{i}] = {superf[i]}')

# La superficie generada es el segundo elemento de la lista anterior
bd, s, bs, bi = superf


# %% Creamos los grupos físicos:

# Bordes físicos: AB, BC, CD y AD:
nombres = ['AB', 'BC', 'CD', 'AD']
bordes  = [bi[1], bd[1], bs[1], 1]
for i in range(len(nombres)):
    gmsh.model.addPhysicalGroup(1, [bordes[i]], i+1)
    gmsh.model.setPhysicalName(1, i+1, nombres[i])


# Superficie física:
dim, tag = s
gmsh.model.addPhysicalGroup(dim, [tag], 101)
gmsh.model.setPhysicalName(dim, 101, 'ABCD')

# %% Definimos que la superficie creada tenga una malla estructurada:
geom.mesh.setTransfiniteSurface(tag)

# Y recombinamos para que use elementos cuadriláteros en lugar de triángulos
geom.mesh.setRecombine(2, tag)

# %% Finalmente se crea la malla y se guarda:

geom.synchronize()
gmsh.model.mesh.generate(2)

filename = 'malla_shell.msh'
gmsh.write(filename)

# Si queremos que en la visualización se muestren los ejes de coordenadas, po-
# demos modificar esta opción, tomado del manual:
# =============================================================================
#  General.Axes
#  Axes (0: none, 1: simple axes, 2: box, 3: full grid, 4: open grid, 5: ruler)
#  Default value: 0
# =============================================================================
gmsh.option.setNumber('General.Axes', 1)  # 1 para "ejes simples"

gmsh.option.setNumber('Mesh.SurfaceFaces', 1)
gmsh.option.setNumber('Mesh.Points', 1)

# Visualizamos el resultado en la interfaz gráfica de GMSH
gmsh.fltk.run()

# Se finaliza el programa
gmsh.finalize()
