# -*- coding: utf-8 -*-
"""
Ejemplo 3: Programa para crear una malla estructurada sencilla usando la fun-
ción 'extrude'.

Por: Alejandro Hincapié G.
"""

import gmsh

# %% Se inicializa el modelo
gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("modelo_3")

# Línea para abreviar el código
geom = gmsh.model.geo

# %% Se crean las entidades
p1 = geom.addPoint(0, 0 ,0)

# Podemos generar una línea extruyendo el punto creado anteriormente
line = geom.extrude([(0, p1)], 0, 20, 0, numElements=[10])

print(line)  # Se muestra la lista creada al extruir

# =============================================================================
# En la lista que se crea al extruir una entidad, el segundo elemento siempre
# corresponde a la entidad de dimensión superior generada. En este caso, al ex-
# truir un punto (dim=2), la entidad de orden superior que se genera es una linea
# (dim=1). En la lista creada, cada elemento corresponde a una tupla (dim, tag)
# =============================================================================
l1 = line[1]  # Se obtiene la tupla (dim, tag) de la línea recién creada

# %% Se crea la superficie extruyendo la línea anterior
# =============================================================================
#     Sintaxis: gmsh.model.geo.extrude([lista de entidades], u, v, w), donde:
#               - La lista de entidades consiste en pares (dim, tag)
#               - u, v, w son las componentes del vector de traslación
#               - El argumento numElements nos permite especificar el número de
#                 "capas" creadas al extruir
#               - El argumento recombine fuerza que la malla estructurada que se
#                 genera conste de cuadriláteros en lugar de triángulos
# =============================================================================

surf = geom.extrude([l1], 40, 0, 0, numElements=[20], recombine=True)
print(surf)  # Se muestra la lista generada al extruir la línea

s1 = surf[1]  # Y nuevamente obtenemos su dupla (dim, tag)

# %%% Se crea la superficie física
gmsh.model.addPhysicalGroup(2, [s1[1]], 21)
gmsh.model.setPhysicalName(2, 21, 'superficie')

# %% Se sincroniza el modelo y se crea la malla
geom.synchronize()

gmsh.model.mesh.generate(2)

# Creamos una malla con elementos de orden 2:
gmsh.model.mesh.setOrder(2)

# Usar elementos serendípitos (incompletos):
gmsh.option.setNumber('Mesh.SecondOrderIncomplete', 1)

gmsh.option.setNumber('Mesh.SurfaceFaces', 1)  # Para mejorar la visualización

gmsh.fltk.run()  # Muestra el resultado en la interfaz gráfica

gmsh.finalize()
