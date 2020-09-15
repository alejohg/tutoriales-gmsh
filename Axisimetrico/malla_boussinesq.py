# -*- coding: utf-8 -*-
"""
Malla de elementos finitos para el problema de Boussinesq.
EF a utilizar: Cuadrilátero serendípito de 8 nodos

Por: Alejandro Hincapié G.
"""

import gmsh

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("modelo_ejm")


geom = gmsh.model.geo
h = 10
L = 10
n = 20  # No. de EF en el lado largo
m = 10  # No. de EF en el lado cargado

p1 = geom.addPoint(0, -h, 0, 1)
p2 = geom.addPoint(L, -h, 0, 1)
p3 = geom.addPoint(L, 0, 0, 1)
p4 = geom.addPoint(1, 0, 0, 0.05)
p5 = geom.addPoint(0, 0, 0, 0.05)

l1 = geom.addLine(p1, p2)
l2 = geom.addLine(p2, p3)
l3 = geom.addLine(p3, p4)
l4 = geom.addLine(p4, p5)
l5 = geom.addLine(p5, p1)



geom.addCurveLoop([l1, l2, l3, l4, l5], 1)
s1 = geom.addPlaneSurface([1])



gmsh.model.addPhysicalGroup(1, [l4], 11)
gmsh.model.setPhysicalName(1, 11, "carga_0_-4000")

gmsh.model.addPhysicalGroup(1, [l1, l2], 12)
gmsh.model.setPhysicalName(1, 12, "borde_res_xy")

gmsh.model.addPhysicalGroup(1, [l5], 13)
gmsh.model.setPhysicalName(1, 13, "borde_res_x")

gmsh.model.addPhysicalGroup(2, [s1], 101)
gmsh.model.setPhysicalName(2, 101, "mat_1e6_0.3_0")

geom.synchronize()
gmsh.option.setNumber("Mesh.RecombineAll", 1)
gmsh.option.setNumber("Mesh.Algorithm", 1)
gmsh.option.setNumber("Mesh.SecondOrderIncomplete", 1)
gmsh.option.setNumber("Mesh.RecombinationAlgorithm", 3)
gmsh.option.setNumber('Mesh.SurfaceFaces', 1)
gmsh.option.setNumber('Mesh.Points', 1)

gmsh.model.mesh.generate(2)
gmsh.model.mesh.setOrder(2)


gmsh.write("malla_boussinesq.msh")

gmsh.fltk.run()

gmsh.finalize()