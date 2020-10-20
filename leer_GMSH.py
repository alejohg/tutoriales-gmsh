# -*- coding: utf-8 -*-
"""
Funciones para leer y graficar una malla creada en GMSH.

Por: Alejandro Hincapié G.
"""

import gmsh  # pip install --upgrade gmsh
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import BASE_COLORS, TABLEAU_COLORS

# %% Funciones:

def xnod_from_msh(archivo, dim=2):
    ''' Obtiene la matriz de coordenadas de los nodos que contiene la malla de
        EF a trabajar, a partir del archivo .msh exportado por el programa GMSH.
    '''
    gmsh.initialize()
    gmsh.open(archivo)
    nod, xnod, pxnod = gmsh.model.mesh.getNodes()
    xnod = xnod.reshape((nod.size, -1))
    gmsh.finalize()

    return xnod[:, :dim]


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


def plot_msh(file, tipo, mostrar_nodos=False, mostrar_num_nodo=False, 
             mostrar_num_elem=False):
    ''' Función para graficar la malla contenida en el archivo "file".
        Argumentos:
        - file: str. Debe ser un archivo de extensión .msh exportado por GMSH.
        - tipo: str. 'shell' o '2D'
        - mostrar_nodos: bool. Define si se muestran los nodos en el gráfico.
        - mostrar_num_nodo: bool. Define si se muestra el número de cada nodo
                            en el gráfico.
        - mostrar_num_elem: bool. Define si se muestra el número de cada ele-
                            mento finito en el gráfico.                            
    '''

    LaG_mat = LaG_from_msh(file)
    mat = LaG_mat[:, 0]
    LaG = LaG_mat[:, 1:]
    nef = LaG.shape[0]
    
    # Se determina el tipo de elemento finito
    if LaG.shape[1] == 3:
        elem = 'T3'
    elif LaG.shape[1] == 4:
        elem = 'Q4'
    elif LaG.shape[1] == 6:
        elem = 'T6'
    elif LaG.shape[1] == 8:
        elem = 'Q8'
    elif LaG.shape[1] == 9:
        elem = 'Q9'
    elif LaG.shape[1] == 10:
        elem = 'T10'

    if tipo=='shell':
        xnod = xnod_from_msh(file, 3)
        nno = xnod.shape[0]

        cg = np.empty((nef,3))  # Centro de gravedad del EF
        colores = list(BASE_COLORS.values()) + list(TABLEAU_COLORS.values())

        fig = plt.figure(figsize=(12, 12))
        ax = plt.gca(projection='3d')
        for e in range(nef):
            if elem=='T3' or elem=='Q4':
                nodos = np.r_[LaG[e], LaG[e, 0]]
            elif elem =='T6':
                nodos = LaG[e, [0, 3, 1, 4, 2, 5, 0]]
            elif elem =='Q8' or elem == 'Q9':
                nodos = LaG[e, [0, 4, 1, 5, 2, 6, 3, 7, 0]]
            elif elem == 'T10':
                nodos = LaG[e, [0, 3, 4, 1, 5, 6, 2, 7, 8, 0]]
            color = colores[mat[e]]
            X = xnod[nodos,0]
            Y = xnod[nodos,1]
            Z = xnod[nodos,2]
            
            ax.plot3D(X, Y, Z, '-', lw=0.8, c=color)
            if mostrar_nodos:
                ax.plot3D(xnod[LaG[e],0], xnod[LaG[e],1], xnod[LaG[e],2],
                          'ko', ms=5, mfc='r')
            if mostrar_num_elem:
                # se calcula la posición del centro de gravedad del EF
                cg[e] = np.mean(xnod[LaG[e]], axis=0)
        
                # y se reporta el número del elemento actual
                ax.text(cg[e,0], cg[e,1], cg[e,2], f'{e+1}',
                        horizontalalignment='center',
                        verticalalignment='center',  color=color)
        if mostrar_num_nodo:
            for i in range(nno):
               ax.text(xnod[i,0], xnod[i,1], xnod[i,2], f'{i+1}', color='r')
        fig.suptitle(f'Malla de EF Shell ({elem})', fontsize='x-large')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')
        ax.view_init(45, 45)
        
    elif tipo=='2D':
        xnod = xnod_from_msh(file, 2)
        nno = xnod.shape[0]

        cg = np.empty((nef,2))
        colores = list(BASE_COLORS.values()) + list(TABLEAU_COLORS.values())
        fig = plt.figure(figsize=(12, 12))
        ax = plt.gca()
        for e in range(nef):
            if elem=='T3' or elem=='Q4':
                nodos = np.r_[LaG[e], LaG[e, 0]]
            elif elem =='T6':
                nodos = LaG[e, [0, 3, 1, 4, 2, 5, 0]]
            elif elem =='Q8' or elem == 'Q9':
                nodos = LaG[e, [0, 4, 1, 5, 2, 6, 3, 7, 0]]
            elif elem == 'T10':
                nodos = LaG[e, [0, 3, 4, 1, 5, 6, 2, 7, 8, 0]]
            color = colores[mat[e]]
            X = xnod[nodos,0]
            Y = xnod[nodos,1]
            ax.plot(X, Y, '-', lw=0.8, c=color)
            if mostrar_nodos:
                ax.plot(xnod[LaG[e],0], xnod[LaG[e],1], 'ko', ms=5, mfc='r')
            if mostrar_num_elem:
                # se calcula la posición del centro de gravedad del EF
                cg[e] = np.mean(xnod[LaG[e]], axis=0)
        
                # y se reporta el número del elemento actual
                ax.text(cg[e,0], cg[e,1], f'{e+1}', horizontalalignment='center',
                        verticalalignment='center',  color=color)
        if mostrar_num_nodo:
            for i in range(nno):
               ax.text(xnod[i,0], xnod[i,1], f'{i+1}', color='r')
        fig.suptitle(f'Malla de EF 2D ({elem})', fontsize='x-large')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_aspect('equal', adjustable='box')
    else:
        raise ValueError('El argumento "tipo" introducido no es válido')