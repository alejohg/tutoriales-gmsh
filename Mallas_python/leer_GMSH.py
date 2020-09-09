# -*- coding: utf-8 -*-
"""
Funciones para leer y graficar una malla creada en GMSH.

Por: Alejandro Hincapié Giraldo
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


# %% Funciones:

def xnod_from_msh(archivo, dim=2):
    ''' Obtiene la matriz de coordenadas de los nodos que contiene la malla de
        EF a trabajar, a partir del archivo .msh exportado por el programa GMSH.
    '''

    # Se lee el archivo y se toman cada una de sus líneas:
    m = open(archivo)
    malla = m.readlines()
    malla = [linea.rstrip('\n') for linea in malla]

    # Se determina en qué lineas comienza y termina el reporte de nodos del
    # archivo:
    inicio_nodos = malla.index('$Nodes')
    fin_nodos = malla.index('$EndNodes')

    # Se toma únicamente la parte del archivo que se requiere:
    malla = malla[inicio_nodos+1:fin_nodos]

    # Se leen los parámetros iniciales:
    nblocks, nnodos = [int(n) for n in malla[0].split()[0:2]]

    # Se inicializan las listas para cada una de las entidades que
    # reporta el archivo:
    nodos_puntos = []; xnod_puntos = []
    nodos_bordes = []; xnod_bordes = []
    nodos_superf = []; xnod_superf = []


    for j in range(1, len(malla)):
        line = malla[j]
        if len(line.split()) == 4:             # Se busca el reporte de cada bloque
            tipo_ent = int(line.split()[0])    # Punto, borde o superf.
    
            nno_bloque = int(line.split()[-1]) # No. de nodos del bloque
            nodos_bloque = malla[j+1:j+1+nno_bloque]  # Lista de nodos del bloque
            nodos_bloque = [int(n) for n in nodos_bloque] # Se convierten a enteros
    
            xnod_b = malla[j+1+nno_bloque:j+1+2*nno_bloque]
    
            # Se reportan las coordenadas como una "matriz":
            xnod_bloque = []
            for l in xnod_b:
                coord = [float(n) for n in l.split()]
                xnod_bloque.append(coord)

            # Finalmente se agregan los datos leídos a la lista corres-
            # pondiente según la entidad (punto, línea o superficie):
            if tipo_ent == 0:
                nodos_puntos.append(nodos_bloque)
                xnod_puntos.append(xnod_bloque)
            elif tipo_ent == 1:
                nodos_bordes.append(nodos_bloque)
                xnod_bordes.append(xnod_bloque)
            elif tipo_ent == 2:
                nodos_superf.append(nodos_bloque)
                xnod_superf.append(xnod_bloque)

    # Se ensambla finalmente la matriz xnod completa:

    xnod = np.empty((nnodos, 3))

    # Primero se adicionan los nodos correspondientes a los puntos:
    for i in range(len(nodos_puntos)):
        idx = np.array(nodos_puntos[i]) - 1
        xnod[idx, :] = np.array(xnod_puntos[i])

    # Luego se agregan los nodos correspondientes a los bordes:
    for i in range(len(nodos_bordes)):
        idx = np.array(nodos_bordes[i]) - 1
        xnod[idx, :] = np.array(xnod_bordes[i])

    # Finalmente se agregan los nodos correspondientes a la superficie:
    for i in range(len(nodos_superf)):
        idx = np.array(nodos_superf[i]) - 1
        xnod[idx, :] = np.array(xnod_superf[i])

    # Se toman las columnas necesarias según la dimensión
    xnod = xnod[:, :dim]

    return xnod

def LaG_from_msh(archivo):
    ''' Obtiene la matriz de interconexión nodal (LaG) que contiene la malla de
        EF a trabajar, a partir del archivo .msh exportado por el programa GMSH.
    '''
    # Se lee el archivo y se toman cada una de sus líneas:
    m = open(archivo)
    malla = m.readlines()
    malla = [linea.rstrip('\n') for linea in malla]

    # Se determina en qué lineas comienza y termina el reporte de nodos del
    # archivo:
    for i in range(len(malla)):
        inicio_elem = malla.index('$Elements')
        fin_elem = malla.index('$EndElements')

    # Se toman solo las líneas necesarias
    malla = malla[inicio_elem+1:fin_elem]

    nblocks, nelem = [int(n) for n in malla[0].split()[0:2]]
    matrices = []  # Guardará las matrices LaG asociadas a cada entidad
    tags = []      # Tag correspondiente a cada entidad
    fila = 1       # Contador de filas recorridas

    for i in range(nblocks):
        linea = malla[fila]
        dim, tag, tipo_ef, nef = [int(n) for n in linea.split()]
        if dim==2:  # solo se toman nodos pertenecientes a superficies
            tags.extend([tag]*nef)
            matrices.append(malla[fila+1:fila+1+nef])
        fila += (1+nef)

    LaG = []  # Se inicializa la matriz LaG

    for matriz in matrices:
        for i in range(len(matriz)):
            linea = [int(n) for n in matriz[i].split()]
            LaG.append(linea)
    LaG = np.array(LaG)-1

    # Se reporta la superficie a la que pertenece cada elemento finito
    LaG[:, 0] = np.array(tags)

    return LaG


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
    LaG = LaG_from_msh(file)
    LaG = LaG[:, 1:]
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
            X = xnod[nodos,0]
            Y = xnod[nodos,1]
            Z = xnod[nodos,2]
            ax.plot3D(X, Y, Z, 'k-', lw=0.5)
            if mostrar_nodos:
                ax.plot3D(xnod[LaG[e],0], xnod[LaG[e],1], xnod[LaG[e],2],
                          'ko', ms=5, mfc='r')
            if mostrar_num_elem:
                # se calcula la posición del centro de gravedad del EF
                cg[e] = np.mean(xnod[LaG[e]], axis=0)
        
                # y se reporta el número del elemento actual
                ax.text(cg[e,0], cg[e,1], cg[e,2], f'{e+1}', horizontalalignment='center',
                        verticalalignment='center',  color='b')
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
            X = xnod[nodos,0]
            Y = xnod[nodos,1]
            ax.plot(X, Y, 'k-', lw=0.5)
            if mostrar_nodos:
                ax.plot(xnod[LaG[e],0], xnod[LaG[e],1], 'ko', ms=5, mfc='r')
            if mostrar_num_elem:
                # se calcula la posición del centro de gravedad del EF
                cg[e] = np.mean(xnod[LaG[e]], axis=0)
        
                # y se reporta el número del elemento actual
                ax.text(cg[e,0], cg[e,1], f'{e+1}', horizontalalignment='center',
                        verticalalignment='center',  color='b')
        if mostrar_num_nodo:
            for i in range(nno):
               ax.text(xnod[i,0], xnod[i,1], f'{i+1}', color='r')
        fig.suptitle(f'Malla de EF 2D ({elem})', fontsize='x-large')
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_aspect('equal', adjustable='box')
    else:
        raise ValueError('El argumento "tipo" introducido no es válido')
