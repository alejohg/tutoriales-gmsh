# -*- coding: utf-8 -*-
"""
Ejemplo 5: Malla shell en GMSH ( Problema "Twisted beam")

Por: Alejandro Hincapié G.
"""

# %% Se inicializa el módulo:

import gmsh
import numpy as np


gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("modelo_4")

# %% Variables asociadas a la geometría:

L = 12
b = 1.1
N = 2  # La malla será de 6N x N elementos

# %% Se crea la geometría:
geom = gmsh.model.geo

# Puntos:
p1 = geom.addPoint(0, 0, -b/2)
p2 = geom.addPoint(0, 0, b/2)
p3 = geom.addPoint(-b/2, -L, 0)
p4 = geom.addPoint(b/2, -L, 0)

# Líneas:
l1 = geom.addLine(p1, p2)
l2 = geom.addLine(p2, p3)
l3 = geom.addLine(p3, p4)
l4 = geom.addLine(p4, p1)

# Superficie:
cl = geom.addCurveLoop([l1, l2, l3, l4])
s = geom.addSurfaceFilling([cl])


# %% Se define la malla como estructurada:

# Líneas en el sentido Z
for tag in [l1, l3]:
    geom.mesh.setTransfiniteCurve(tag, N+1)

# Líneas en el sentido Y
for tag in [l2, l4]:
    geom.mesh.setTransfiniteCurve(tag, 6*N+1)

geom.mesh.setTransfiniteSurface(s)
geom.mesh.setRecombine(2, s) # Usar cuadriláteros en lugar de triángulos

# %% Finalmente se crea la malla

geom.synchronize()
gmsh.model.mesh.generate(2)
#gmsh.model.mesh.setOrder(1)

# %% Se crean grupos físicos:

gmsh.model.addPhysicalGroup(2, [s], 21)
gmsh.model.setPhysicalName(2, 21, "Superficie")

# %% Se guarda la malla
filename = 'twisted_beam.msh'
gmsh.write(filename)


# Si queremos que en la visualización se muestren los ejes de coordenadas, po-
# demos modificar esta opción, tomado del manual:
# =============================================================================
#  General.Axes
#  Axes (0: none, 1: simple axes, 2: box, 3: full grid, 4: open grid, 5: ruler)
#  Default value: 0
# =============================================================================
gmsh.option.setNumber('General.Axes', 1)  # 1 para "ejes simples"


# Podemos visualizar el resultado en la interfaz gráfica de GMSH
gmsh.fltk.run()

# Se finaliza el programa
gmsh.finalize()
