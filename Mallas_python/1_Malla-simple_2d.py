# -*- coding: utf-8 -*-
'''
Programa para crear una malla básica en GMSH usando la API de Python.

Por: Alejandro Hincapié G.
'''

import gmsh

# %% Para comenzar a usar funciones de la API de GMSH se debe incializar:

gmsh.initialize()

# %% Con este comando se activa la opción de que GMSH imprima mensajes en la
#    consola, ya que por defecto no lo hace: 

gmsh.option.setNumber("General.Terminal", 1)

# %% Podemos crear un nuevo modelo con la siguiente línea. Esta línea es opcio-
#    nal, si no se usa el programa genera un modelo "Unnamed" por defecto.

gmsh.model.add("modelo_1")

# %% Se crean las primeras entidades: Los puntos (dimensión 0):

# En este programa se usará el kernel de geometría que trae por defecto el
# GMSH, no es el único, pero para este caso funciona bastante bien.

# Sintaxis: gmsh.model.geo.addPoint(x, y, z, tm, tag)
#           tm = Tamaño de malla en el punto

tm = 2  # Tamaño de malla a utilizar en todos los puntos
tmr = 0.3  # Tamaño de malla refinada (alrededor del agujero)

gmsh.model.geo.addPoint(0,  0,  0, tm, 1)  # Punto 1 coord (0,0,0)
gmsh.model.geo.addPoint(40, 0,  0, tm, 2)  # Punto 2 coord (40,0,0) ...
gmsh.model.geo.addPoint(40, 20, 0, tm, 3)
gmsh.model.geo.addPoint(0,  20, 0, tm, 4)

# Se deben definir 3 puntos que permitan crear luego el círculo. El centro, un
# punto a la izquierda y otro a la derecha:

r = 3  # radio del círculo

gmsh.model.geo.addPoint(20, 10, 0, tm, 5)    # Punto central del círculo
gmsh.model.geo.addPoint(20+r, 10, 0, tmr, 6)
gmsh.model.geo.addPoint(20-r, 10, 0, tmr, 7)

# %% Se crean las siguientes entidades: Las curvas (dimensión 1):

# Primero las líneas rectas de los bordes:
# Sintaxis: gmsh.model.geo.addLine(punto inicial, punto final, tag)

gmsh.model.geo.addLine(1, 2, 1)  # Éste sería el borde inferior
gmsh.model.geo.addLine(2, 3, 2)  # ...
gmsh.model.geo.addLine(3, 4, 3)
gmsh.model.geo.addLine(4, 1, 4)

# Ahora los arcos de circunferencia para el agujero (se deben crear 2 arcos, ya
# que el kernel built-in no permite crear arcos con un ángulo mayor a 180°)
# Sintaxis: gmsh.model.geo.addCircle(p. inicial, p. centro, p. final, tag)

gmsh.model.geo.addCircleArc(6, 5, 7, 5)  # Arco superior
gmsh.model.geo.addCircleArc(7, 5, 6, 6)  # Arco inferior

# %% Ahora se define la siguiente entidad: La superficie (dimensión 2):

# Para definir superficies, primero se deben definir 'Curve Loops' que las
# limiten. En este caso un Curve Loop será el borde exterior, y el otro será
# el agujero.

gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)
gmsh.model.geo.addCurveLoop([5, 6], 2)

# Ahora sí se puede definir la superficie, así:
#Sintaxis: gmsh.model.geo.addPlaneSurface([Lista de Curve Loops], tag), donde:
#          En la lista de Curve Loops el primer elemento es el loop que define
#          el contorno de la superficie, los demás son agujeros dentro de ella.

gmsh.model.geo.addPlaneSurface([1, 2], 1)

# %% Ahora se crean los grupos físicos que se requieran
#Por defecto, si hay grupos físicos definidos, GMSH solo reporta elementos fini-
#tos que pertenezcan a algún grupo físico. En este caso se crearán dos:
#    - Una superficie física que contenga nuestra superficie creada
#    - Una curva física que contenga el borde inferior

# Sintaxis: gmsh.model.addPhysicalGroup(dimensión, lista de entidades, tag)

s = gmsh.model.addPhysicalGroup(2, [1]) # En este caso no se especifica tag
gmsh.model.setPhysicalName(2, s, "Mi superficie")  # Se puede definir un nombre

gmsh.model.addPhysicalGroup(1, [1], 101)  # Puedo especificar tag manualmente 
gmsh.model.setPhysicalName(1, 101, "Borde inferior")

# %% Antes de mallar, se debe sincronizar la representación CAD del GMSH con el
#    modelo actual:

gmsh.model.geo.synchronize()

# %% Ahora sí se procede a crear la malla:

gmsh.model.mesh.generate(2)

gmsh.option.setNumber('Mesh.SurfaceFaces', 1)  # Ver las "caras" de los elementos finitos 2D
gmsh.option.setNumber('Mesh.Points', 1)        # Ver los nodos de la malla


# Y finalmente guardar la malla
filename = 'ejm_1.msh'
gmsh.write(filename)

# Podemos visualizar el resultado en la interfaz gráfica de GMSH
gmsh.fltk.run()

# %% Tras finalizar el proceso se recomienda usar este comando
gmsh.finalize()

# %% Podemos graficar la malla para ver el resultado:

from leer_GMSH import plot_msh  # Funciones para leer y graficar la malla

#plot_msh(filename, '2D', True, True, True)
