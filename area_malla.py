# -*- coding: utf-8 -*-
'''
Programa para calcular el área de una malla creada en GMSH usando la API de
GMSH en Python.

Por: Alejandro Hincapié G.
'''

import gmsh  # pip install --upgrade gmsh
import numpy as np

def xnod_from_msh(archivo):
    ''' Obtiene la matriz de coordenadas de los nodos que contiene la malla de
        EF a trabajar, a partir del archivo .msh exportado por el programa GMSH.
        Argumentos:
        - archivo: Nombre del archivo que contiene la malla
        - dim: 2 si la malla es 2D (valor por defecto), 3 si la malla es 3D.
    '''
    gmsh.initialize()
    gmsh.open(archivo)
    nod, xnod, pxnod = gmsh.model.mesh.getNodes()
    xnod = xnod.reshape((nod.size, -1))
    gmsh.finalize()

    return xnod

def LaG_from_msh(archivo):
    ''' Obtiene la matriz de interconexión nodal (LaG) que contiene la malla de
        EF a trabajar, a partir del archivo .msh exportado por el programa GMSH.
        
        Retorna: Matriz LaG_mat, donde la primera columna representa la super-
        ficie a la que pertenece cada elemento finito (ordenadas de forma
        ascendente desde 0), de tal manera que diferencie elementos finitos con
        propiedades distintas
    '''
    gmsh.initialize()
    gmsh.open(archivo)

    LaG   = np.array([]) # Matriz de interconexión nodal
    elems = np.array([]) # vector de elementos finitos
    mats  = np.array([]) # Vector de materiales al que pertenece cada EF
    material = 0  # Se inicializa el material

    for ent in gmsh.model.getEntities(2):
        dim, tag = ent
        tipo, efs, nodos = gmsh.model.mesh.getElements(dim, tag)
        if tipo.size == 1:
            nodos = nodos[0]
            elems = np.append(elems, efs[0]).astype(int)
            LaG = np.append(LaG, nodos).astype(int)
            mats = np.append(mats, np.tile(material, efs[0].size)).astype(int)
            material += 1
        else:
            raise ValueError('La malla tiene varios tipos de elementos '
                             'finitos 2D.')

    nef = elems.size
    LaG = LaG.reshape((nef, -1)) - 1
    LaG_mat = np.c_[mats, LaG]
    gmsh.finalize()

    return LaG_mat

def area_triangulo(coord):
    ''' Calcula el área de un elemento finito triangular dadas sus coordenadas.
        Argumentos:
        coord: Es un vector de coordenadas de la forma: [XY1, XY2, XY3], donde:
        XY1, XY2 y XY3 son los vectores de coordenadas de cada nodo, así:
        XY1 = [x1, y1, z1] son las coordenadas del nodo 1, y así para los otros
        nodos.
    '''
    c1, c2, c3 = coord
    u = c2 - c1
    v = c3 - c1

    return np.linalg.norm(np.cross(u, v))/2


def area_malla(coord):
    ''' Calcula el área de la malla dado el array de coordenadas de todos los
        elementos finitos que la componen.
    '''
    return np.array(list(map(area_triangulo, coord))).sum()
    
    
malla = './malla.msh' # Nombre del archivo .msh que contiene la malla

# Se obtienen las coordenadas de los nodos y la matriz de nodos:

coord = xnod_from_msh(malla) # Coordenadas de cada nodo
nodos = LaG_from_msh(malla)[:, 1:] # Nodos correspondientes a cada elemento finito
nef = nodos.shape[0] # Número de elementos finitos de la malla
dim = coord.shape[1] # Dimensión de los elementos finitos usados

coord_triangulos = np.empty((nef, 3, dim))
for i in range(nef):
    coord_triangulos[i] = coord[nodos[i]] # Obtiene las coordenadas de los 3
                                          # vértices de cada triángulo

A = area_malla(coord_triangulos)

print(f"El area de la malla es: {A}")
