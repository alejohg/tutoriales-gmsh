# -*- coding: utf-8 -*-
"""
Programa para crear una malla estructurada en GMSH usando la API de Python.

Por: Alejandro Hincapié G.
"""

import gmsh
from math import cos, sin, pi


gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)

gmsh.model.add("modelo_2")


# %% Variables asociadas a la geometría:
L = 6.5/2
r = 1

# %% Se crea la geometría:

# La siguiente línea permite abreviar el código:
geom = gmsh.model.geo

# Puntos:
pc = geom.addPoint(0, 0, 0)  # Punto central del círculo
p1 = geom.addPoint(r, 0, 0)
p2 = geom.addPoint(L, 0, 0)
p3 = geom.addPoint(L, L, 0)
p4 = geom.addPoint(0, L, 0)
p5 = geom.addPoint(0, r, 0)
p6 = geom.addPoint(r*cos(pi/4), r*sin(pi/4), 0)


# Líneas
l1 = geom.addLine(p1, p2)
l2 = geom.addLine(p2, p3)
l3 = geom.addLine(p3, p4)
l4 = geom.addLine(p4, p5)
l5 = geom.addLine(p3, p6)
c1 = geom.addCircleArc(p5, pc, p6)
c2 = geom.addCircleArc(p6, pc, p1)

# Curve loops:
cl1 = geom.addCurveLoop([l1, l2, l5, c2])
cl2 = geom.addCurveLoop([-l5, l3, l4, c1])


# Dado que queremos una malla estructurada, definimos el número de elementos
# que queremos en ciertas líneas:
# Sintaxis: gmsh.model.geo.mesh.setTransfiniteCurve(tag, # nodos)

m = 15  # Líneas perpendiculares al círculo
n = 10  # Líneas en el sentido del círculo

for tag in [c1, l3, c2, l2]:
    gmsh.model.geo.mesh.setTransfiniteCurve(tag, n+1)
for tag in [l5, l4, l1]:
    gmsh.model.geo.mesh.setTransfiniteCurve(tag, m+1)

# Finalmente creamos la superficie:
s1 = geom.addPlaneSurface([cl1])
s2 = geom.addPlaneSurface([cl2])
# Definimos la superficie física:
gmsh.model.addPhysicalGroup(2, [s1, s2], 101)
gmsh.model.setPhysicalName(2, 101, 'mi superficie')


# %% Definimos que la superficie creada tenga una malla estructurada:
geom.mesh.setTransfiniteSurface(s1)   
geom.mesh.setTransfiniteSurface(s2)

# Y recombinamos para que use elementos cuadriláteros en lugar de triángulos
geom.mesh.setRecombine(2, s1)
geom.mesh.setRecombine(2, s2)


# %% Finalmente se crea la malla y se guarda:

geom.synchronize()

# Ver las "caras" de los elementos finitos 2D
gmsh.option.setNumber('Mesh.SurfaceFaces', 1)

# Ver los nodos de la malla
gmsh.option.setNumber('Mesh.Points', 1)

gmsh.model.mesh.generate(2)

# Se guarda la malla
filename = 'ejm_2.msh'
gmsh.write(filename)

# Podemos visualizar el resultado en la interfaz gráfica de GMSH
gmsh.fltk.run()

# Se finaliza el programa
gmsh.finalize()

# %% Podemos graficar la malla para ver el resultado:

from leer_GMSH import plot_msh  # Funciones para leer y graficar la malla

#plot_msh(filename, '2D', True)
