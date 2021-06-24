# -*- coding: utf-8 -*-

import numpy                as np
import matplotlib.pyplot    as plt
import warnings

# %% constantes que ayudaran en la lectura del codigo
X, Y = 0, 1
NL1, NL2, NL3, NL4, NL5, NL6, NL7, NL8 = range(8)

# %% variables globales que se heredarán del programa principal
xnod = None
LaG = None

# %%
def compartir_variables(xnod_, LaG_):
    '''
    Importa variables globales del programa principal a este módulo
    '''
    global xnod, LaG
    xnod, LaG = xnod_, LaG_
        
# %%
def t2ft_R89_axisimetrico(xnod, lado, carga):
    '''Función que convierte las fuerzas superficiales aplicadas a un elemento
    finito rectangular de 8 (serendípito) o 9 (lagrangiano) nodos a sus 
    correspondientes cargas nodales equivalentes ft en el caso AXISIMETRICO   
    
    Recibe:
        xnod:  coordenadas nodales del elemento finito
          SERENDIPITO 8          LAGRANGIANO 9
          xnod = [ x1e y1e       xnod = [ x1e y1e
                  x2e y2e                x2e y2e
                   ... ...                ... ...
                  x8e y8e ]             x9e y9e ]

        lado:  arista en la que se aplica la carga, puede tomar los siguientes
               valores: 123, 345, 567, 781

        carga: fuerza distribuida en los nodos
        
               [ t1x t1y t2x t2y t3x t3y ]; % si carga se aplica sobre lado 123
               [ t3x t3y t4x t4y t5x t5y ]; % si carga se aplica sobre lado 345
               [ t5x t5y t6x t6y t7x t7y ]; % si carga se aplica sobre lado 567
               [ t7x t7y t8x t8y t1x t1y ]; % si carga se aplica sobre lado 781
    '''
    
    # se definen los indices de los lados
    if   lado == 123: idx = np.array([ 1, 2, 3 ]) - 1
    elif lado == 345: idx = np.array([ 3, 4, 5 ]) - 1
    elif lado == 567: idx = np.array([ 5, 6, 7 ]) - 1
    elif lado == 781: idx = np.array([ 7, 8, 1 ]) - 1
    else: 
        raise Exception('Únicamente se permiten los lados 123, 345, 567 o 781')

    nno = xnod.shape[0]
    if nno not in (8, 9):
        raise Exception('Solo para elementos rectangulares de 8 o 9 nodos')

    # parámetros para mejorar la lectura del código
    X, Y = 0, 1
   
    # se define el número de puntos de la cuadratura y se obtienen los puntos
    # de evaluación y los pesos de la cuadratura
    n_gl       = 2
    x_gl, w_gl = np.polynomial.legendre.leggauss(n_gl)
    
    # se definen las funciones de forma unidimensionales y sus derivadas
    NN      = lambda xi: np.array([ xi*(xi-1)/2, (1+xi)*(1-xi), xi*(1+xi)/2 ])
    dNN_dxi = lambda xi: np.array([ xi - 1/2   , -2*xi        , xi + 1/2    ])
       
    # se calcula el vector de fuerzas distribuidas en los nodos
    te = np.zeros(2*nno)
    te[np.c_[2*idx, 2*idx + 1].ravel()] = carga
    
    # cálculo de la integral:
    suma   = np.zeros((2*nno, 2*nno))
    N      = np.zeros(nno)
    dN_dxi = np.zeros(nno)
    for p in range(n_gl):
        # se evalúan las funciones de forma
        N[idx] = NN(x_gl[p])
        matN = np.empty((2,2*nno))
        for i in range(nno):
            matN[:,[2*i, 2*i+1]] = np.array([[N[i], 0   ],
                                             [0,    N[i]]])

        # se calcula el jacobiano
        dN_dxi[idx] = dNN_dxi(x_gl[p])
        r           = np.dot(N,      xnod[:,X])
        dx_dxi      = np.dot(dN_dxi, xnod[:,X])
        dy_dxi      = np.dot(dN_dxi, xnod[:,Y])
        ds_dxi      = np.hypot(dx_dxi, dy_dxi)

        # y se calcula la sumatoria
        suma += r * matN.T @ matN * ds_dxi*w_gl[p]

    # finalmente, se retorna el vector de fuerzas nodales equivalentes
    return suma @ te

#%%
def plot_esf_def(variable, titulo, angulo = None):
    '''
    Grafica variable para la malla de EFs especificada.

    Uso:
        variable: es la variable que se quiere graficar
        titulo:   título del gráfico
        angulo:   opcional para los esfuerzos principales s1 y s2 y tmax
    '''
    
    # Para propósitos de graficación el EF se divide en 6 triángulos así: 
    #     
    #                             7 -------6--------5
    #                             |       /|\       |
    #                             | EFT6 / | \ EFT3 |
    #                             |     /  |  \     |
    #                             |    /   |   \    |
    #                             |   /    |    \   |
    #                             |  /     |     \  |
    #                             | /      |      \ |
    #                             8/  EFT5 | EFT4  \4
    #                             |\       |       /|
    #                             | \      |      / |
    #                             |  \     |     /  |
    #                             |   \    |    /   |
    #                             |    \   |   /    |
    #                             |     \  |  /     |
    #                             | EFT1 \ | / EFT2 |
    #                             |       \|/       |
    #                             1--------2--------3
        
    nef = LaG.shape[0]    # número de elementos finitos en la malla original
    
    # se arma la matriz de correspondencia (LaG) de la nueva malla triangular
    LaG_t = np.zeros((6*nef, 3), dtype = int)
    for e in range(nef):
        LaG_t[6*e + 0, :] = LaG[e, [NL1, NL2, NL8]]
        LaG_t[6*e + 1, :] = LaG[e, [NL2, NL3, NL4]]
        LaG_t[6*e + 2, :] = LaG[e, [NL4, NL5, NL6]]
        LaG_t[6*e + 3, :] = LaG[e, [NL2, NL4, NL6]]
        LaG_t[6*e + 4, :] = LaG[e, [NL2, NL6, NL8]]
        LaG_t[6*e + 5, :] = LaG[e, [NL6, NL7, NL8]]
    
    # se inicializa el lienzo
    fig, ax = plt.subplots() 

    # se encuentra el máximo en valor absoluto para ajustar el colorbar()
    val_max = np.max(np.abs(variable))    

    # se grafica la malla de EFS, los colores en cada triángulo y las curvas 
    # de nivel
    for e in range(nef):
        # se dibujan las aristas
        nod_ef = LaG[e, [NL1, NL2, NL3, NL4, NL5, NL6, NL7, NL8, NL1]]
        plt.plot(xnod[nod_ef, X], xnod[nod_ef, Y], lw = 0.5, color = 'gray')

    im = ax.tripcolor(xnod[:, X], xnod[:, Y], LaG_t, variable, cmap = 'bwr',
                      shading = 'gouraud', vmin = -val_max, vmax = val_max)
    ax.tricontour(xnod[:, X], xnod[:, Y], LaG_t, variable, 20)
    
    # a veces sale un warning, simplemente porque no existe la curva 0
    warnings.filterwarnings("ignore")
    ax.tricontour(xnod[:, X], xnod[:, Y], LaG_t, variable, levels=[0], linewidths=3)
    warnings.filterwarnings("default")

    fig.colorbar(im, ax = ax, format = '%6.3g')
                
    # para los esfuerzos principales se grafican las líneas que indiquen las
    # direcciones de los esfuerzos en cada nodo de la malla
    if angulo is not None:
       if type(angulo) is np.ndarray: 
           angulo = [ angulo ]
       for ang in angulo:
           ax.quiver(xnod[:, X], xnod[:, Y], 
                variable*np.cos(ang), variable*np.sin(ang), 
                headwidth=0, headlength=0, headaxislength=0, pivot='middle')
    
    # se especifican los ejes y el título, y se colocan los ejes iguales
    ax.set_xlabel('$r$ [m]')
    ax.set_ylabel('$z$ [m]')
    ax.set_title(titulo, fontsize=20)

    ax.set_aspect('equal')
    ax.autoscale(tight=True)    
    plt.tight_layout()
    plt.show()