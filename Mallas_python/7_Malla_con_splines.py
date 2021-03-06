# -*- coding: utf-8 -*-
"""
Malla para el perfil de un ala (Airfoil) usando B-Splines en GMSH

Por: Alejandro Hincapié G.
"""

import gmsh # pip install --upgrade gmsh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("modelo_6")

geom = gmsh.model.geo  # Línea para abreviar los comandos de geometría

L = 1  # Longitud desde el centro de la malla interior hasta los bordes

# %% Se crean los puntos de control de la Spline:

geom.addPoint(1, 0, 0)
geom.addPoint(0.8, 0.027, 0)
geom.addPoint(0.55, 0.058, 0)
geom.addPoint(0.3, 0.08, 0)
geom.addPoint(0.15, 0.078, 0)
geom.addPoint(0, 0.052, 0)
geom.addPoint(0, 0, 0)
geom.addPoint(0, -0.01, 0)
geom.addPoint(0.15, -0.052, 0)
geom.addPoint(0.3, -0.05, 0)
geom.addPoint(0.55, -0.043, 0)
geom.addPoint(0.8, -0.017, 0)


# Se crea la B-Spline con tomando los puntos anteriores como puntos de control:

af = geom.addBSpline([1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 1, 1])

geom.mesh.setTransfiniteCurve(af, 301)

cint = geom.addCurveLoop([af])  # Curve loop interior

# %% Se crea el borde de la superficie exterior:
p1 = geom.addPoint(0.5-L, -L, 0)
p2 = geom.addPoint(0.5+L, -L, 0)
p3 = geom.addPoint(0.5+L, L, 0)
p4 = geom.addPoint(0.5-L, L, 0)

l1 = geom.addLine(p1, p2)
l2 = geom.addLine(p2, p3)
l3 = geom.addLine(p3, p4)
l4 = geom.addLine(p4, p1)

cext = geom.addCurveLoop([l1, l2, l3, l4])  # Curve loop exterior

s1 = geom.addPlaneSurface([cext, cint])     # Se crea la superficie exterior

# Se crea superficie física
gmsh.model.addPhysicalGroup(2, [s1], tag=101)
gmsh.model.setPhysicalName(2, 101, "Aire")

# %% Finalmente se crea la malla y se guarda:

geom.synchronize()
gmsh.model.mesh.generate(2)

# Creamos una malla con elementos de orden 2:
gmsh.model.mesh.setOrder(2)

filename = 'airfoil.msh'
gmsh.write(filename)

gmsh.option.setNumber('Mesh.SurfaceFaces', 1)
gmsh.option.setNumber('Mesh.Points', 1)

# Visualizamos el resultado en la interfaz gráfica de GMSH
gmsh.fltk.run()

# Se finaliza el programa
gmsh.finalize()
