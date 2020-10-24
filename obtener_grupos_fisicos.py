# -*- coding: utf-8 -*-
"""
Funciones para obtener todos los grupos físicos definidos en una malla, su dimen-
sión y los nodos asociados a cada uno, a partir de un archivo .msh exportado
por GMSH.

Para correr este programa y usar las funciones se requiere tener instalada la API
de GMSH en Python, usar el comando pip install --upgrade gmsh

Por: Alejandro Hincapié G.
"""

import gmsh  # pip install --upgrade gmsh

def grupos_fisicos(archivo, dim=-1):
    ''' Lee un archivo de texto con extensión .msh que contiene los datos de
        una malla generada en GMSH.
        Si se especifica el argumento dim, solo se reportan los grupos físicos
        de tal dimensión, si no, se reportan todos.
        Retorna:
            - Un diccionario en el cual las claves son las ETIQUETAS de los 
              grupos físicos y los valores son tuplas con la DIMENSIÓN y el
              NOMBRE asociados a cada etiqueta.
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
    nombres = [(dim, gmsh.model.getPhysicalName(dim, tag))
                for dim, tag in grupos]

    dict1 = dict(zip(tags, nombres))  # Primer diccionario a reportar

    nodos = [gmsh.model.mesh.getNodesForPhysicalGroup(dims[i], tags[i])[0]
             for i in range(len(dims))]
    dict2 = dict(zip(tags, nodos))  # Segundo diccionario a reportar

    gmsh.finalize()

    return dict1, dict2


def obtener_nodos(archivo, nombre_grupo):
    ''' Lee un archivo de extensión .msh y obtiene los nodos asociados al grupo
        físico de nombre "nombre_grupo".
    '''
    d1, d2 = grupos_fisicos(archivo)
    nombres = [t[1] for t in d1.values()]
    if nombre_grupo in nombres:
        nodos = d2[list(d2.keys())[nombres.index(nombre_grupo)]]
        gmsh.finalize()
        return nodos
    else:
        raise ValueError('El nombre de grupo físico ingresado no existe.')
