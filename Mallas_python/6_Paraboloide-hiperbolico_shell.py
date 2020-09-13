# -*- coding: utf-8 -*-
"""
Ejemplo 6: Malla de elementos Shell de un paraboloide hiperbólico

Por: Alejandro Hincapié G.
"""

import gmsh

def obtener_pc_bezier(a, b, c, p1, p2):
    ''' Obtiene el punto de control de la curva de Bezier que permite interpolar
        la parábola f(x) = ax^2 + bx + c o f(y) = ay^2 + by + c
    '''
    x1, y1 = p1
    x2, y2 = p2
    f = lambda x: a*x**2 + b*x + c
    
    Cx = (x1+x2)/2
    Cy = (x2-x1)/2 * (2*a*x1 + b) + f(x1)
    
    return Cx, Cy

# %% Se inicializa el módulo

gmsh.initialize()
gmsh.option.setNumber("General.Terminal", 1)
gmsh.model.add("modelo_6")

geom = gmsh.model.geo

N = 8  # La malla será estructurada de 2N x N elementos

f = lambda x, y: y**2 - x**2  # Función que define el paraboloide hiperb.


# %% Lado AB (parábola z = y^2 - 1/4):
a = 1; b = 0; c = -1/4
x = 1/2 # Esta parábola está sobre el plano x=1/2

pA = geom.addPoint(x, -1/2, f(x, -1/2))
pB = geom.addPoint(x,  1/2, f(x,  1/2))

# Obtenemos las coordenadas del pto de control de la Curva de Bezier que per-
# mite trazar la parábola z = y^2 - 1/4:
cy, cz = obtener_pc_bezier(a, b, c, [-1/2, f(x, -1/2)], [1/2, f(x, 1/2)])
pc1 = geom.addPoint(x, cy, cz) # Punto de control de la curva de Bezier

b1 = geom.addBezier([pA, pc1, pB])  # Se crea la parábola como una curva de
                                    # Bezier con pto inicial, final y de control

# %% Lado BC (parábola z = 1/4 - x^2)
a = -1; b = 0; c = 1/4
y = 1/2 # Esta parábola está sobre el plano y = 1/2

pC = geom.addPoint(0, y, f(0, y))

cx, cz = obtener_pc_bezier(a, b, c, [1/2, f(1/2, y)], [0, f(0, y)])
pc2 = geom.addPoint(cx, y, cz)

b2 = geom.addBezier([pB, pc2, pC])


# %% Lado CD (parábola z = y^2)
a = 1; b = 0; c = 0
x = 0 # Esta parábola está sobre el plano x=0

pD = geom.addPoint(x, -1/2, f(x, -1/2))
cy, cz = obtener_pc_bezier(a, b, c, [-1/2, f(x, 1/2)], [1/2, f(x, -1/2)])
pc3 = geom.addPoint(x, cy, cz)

b3 = geom.addBezier([pC, pc3, pD])


# %% Lado AD (parábola z = 1/4-x^2)
a = -1; b = 0; c = 1/4
y = -1/2 # Esta parábola está sobre el plano y = 1/2

cx, cz = obtener_pc_bezier(a, b, c, [0, f(0, y)], [1/2, f(1/2, y)])
pc4 = geom.addPoint(cx, y, cz)

b4 = geom.addBezier([pD, pc4, pA])


# %% Se define malla estructurada:

for curva in [b1, b3]:
    geom.mesh.setTransfiniteCurve(curva, 2*N+1)
for curva in [b2, b4]:
    geom.mesh.setTransfiniteCurve(curva, N+1)

# %% Se define curve loop y superficie:

geom.addCurveLoop([b1, b2, b3, b4], 1)
s = geom.addSurfaceFilling([1])

geom.mesh.setTransfiniteSurface(s) # Se define malla estructurada en superf.

gmsh.model.addPhysicalGroup(2, [s], 101)
gmsh.model.setPhysicalName(2, 101, "ABCD")

# %% Finalmente se crea la malla y se guarda:

geom.synchronize()
gmsh.model.mesh.generate(2)

filename = 'paraboloide.msh'
gmsh.write(filename)

gmsh.option.setNumber('General.Axes', 1)  # 1 para "ejes simples"
gmsh.option.setNumber('Mesh.SurfaceFaces', 1)

# Visualizamos el resultado en la interfaz gráfica de GMSH
gmsh.fltk.run()

# Se finaliza el programa
gmsh.finalize()

# %% Graficamos la malla:

from leer_GMSH import plot_msh  # Funciones para leer y graficar la malla

#plot_msh(filename, 'shell', True)
