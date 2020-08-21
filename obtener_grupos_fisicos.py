# -*- coding: utf-8 -*-
"""
Función para obtener todos los grupos físicos definidos en una malla, su dimen-
sión y los nodos asociados a cada uno, a partir de un archivo .msh exportado
por GMSH.

Para correr este programa y usar la función se requiere tener instalada la API
de GMSH en Python, usar el comando pip install --upgrade gmsh

Por: Alejandro Hincapié G.
"""

import gmsh  # pip install --upgrade gmsh
import numpy as np

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

# %% Ejemplo de uso:

file = 'scordelis.msh'

d1, d2 = grupos_fisicos(file)

print('Grupos físicos reportados:\n')
for tag in d1.keys():
    nombre = d1[tag]
    dim    = d2[tag][0]
    nodos  = d2[tag][1]
    print(f'Grupo físico: {tag}\nDimensión: {dim}\nNombre: {nombre}\n'
          f'Contiene nodos: {nodos}.\n')
