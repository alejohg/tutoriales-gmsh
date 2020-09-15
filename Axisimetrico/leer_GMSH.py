# -*- coding: utf-8 -*-
"""
Funciones para leer y graficar una malla creada en GMSH.

Por: Alejandro Hincapié Giraldo
"""
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import get_named_colors_mapping
import pandas as pd
import gmsh


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
    nmat = 1
    for i in range(nblocks):
        linea = malla[fila]

        dim, tag, tipo_ef, nef = [int(n) for n in linea.split()]
        if dim==2:  # solo se toman nodos pertenecientes a superficies
            tags.extend([nmat]*nef)
            nmat += 1
            matrices.append(malla[fila+1:fila+1+nef])
        fila += (1+nef)

    LaG = []  # Se inicializa la matriz LaG

    for matriz in matrices:
        for i in range(len(matriz)):
            linea = [int(n) for n in matriz[i].split()]
            LaG.append(linea)
    LaG = np.array(LaG)

    # Se reporta la superficie a la que pertenece cada elemento finito
    LaG[:, 0] = np.array(tags)

    return LaG - 1


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
        colores = ['k'] + list(get_named_colors_mapping().values())
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
        colores = ['k'] + list(get_named_colors_mapping().values())

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


def grupos_fisicos(archivo, dim=-1):
    ''' Lee un archivo de texto con extensión .msh que contiene los datos de
        una malla generada en GMSH.
        Si se especifica el argumento dim, solo se reportan los grupos físicos
        de tal dimensión, si no, se reportan todos.
        Retorna:
            - Un diccionario en el cual las claves son las ETIQUETAS de los 
              grupos físicos y los valores son los NOMBRES asociados a cada
              etiqueta.
            - Un diccionario en el cual las claves son las etiquetas de los
              grupos físicos y los valores son listas con los nodos asociados
              a cada grupo físico.
    '''
    if archivo[-4:] != '.msh':
        raise ValueError('Solo se admite un archivo de extensión .msh')

    gmsh.initialize()

    gmsh.open(archivo)
    grupos = gmsh.model.getPhysicalGroups(dim)
    dims = [d[0] for d in grupos]
    tags = [d[1] for d in grupos]
    nombres = [gmsh.model.getPhysicalName(dim, tag) for dim, tag in grupos]

    dict1 = dict(zip(tags, nombres))  # Primer diccionario a reportar

    dim_nodos = [(dims[i], gmsh.model.mesh.getNodesForPhysicalGroup(dims[i],
                                                                    tags[i])[0])
                 for i in range(len(dims))]
    dict2 = dict(zip(tags, dim_nodos))  # Segundo diccionario a reportar

    gmsh.finalize()

    return dict1, dict2


def aplicar_fsuperf(LaG, nodos_lado, Fx, Fy):
    ''' Aplica una fuerza superficial de componentes constantes Fx y Fy sobre
        el lado de la malla que contiene los nodos de la lista "nodos_lado".
    '''

    EF   = np.array([], dtype=int)  # Lista de EFs del borde externo
    lado = np.array([], dtype=int)  # Lado en que está aplicada la carga

    for i in range(LaG.shape[0]):
        fila = LaG[i]
        # Se buscan los EF en los cuales 3 nodos pertenecen al borde exterior:
        if fila[np.isin(fila, nodos_lado)].size == 3:
            EF = np.append(EF, i)
    
            # Y se halla el lado que limita con el borde exterior:
            if np.all(np.isin(fila[[0, 1, 2]], nodos_lado)):
                lado = np.append(lado, 123)
            elif np.all(np.isin(fila[[2, 3, 4]], nodos_lado)):
                lado = np.append(lado, 345)
            elif np.all(np.isin(fila[[4, 5, 6]], nodos_lado)):
                lado = np.append(lado, 567)
            elif np.all(np.isin(fila[[6, 7, 0]], nodos_lado)):
                lado = np.append(lado, 781)
            else:
                raise ValueError('Hay un problema con los lados')

    # Se almacenan los datos en un DataFrame de Pandas:

    df = pd.DataFrame(columns=['elemento', 'lado', 'tix', 'tiy', 'tjx', 'tjy',
                               'tkx', 'tky'])

    df['elemento'] = np.array(EF) + 1
    df['lado'] = lado
    df.iloc[:, [2, 4, 6]] = Fx
    df.iloc[:, [3, 5, 7]] = Fy
    
    return df
    