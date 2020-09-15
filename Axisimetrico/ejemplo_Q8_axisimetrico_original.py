# -*- coding: utf-8 -*-

#%%
'''
-------------------------------------------------------------------------------
NOTA: este código SOLO es apropiado para el caso AXISIMÉTRICO usando elementos
      rectangulares serendípitos de 8 nodos
-------------------------------------------------------------------------------

DEFINICIÓN DEL PROBLEMA:
Calcule los desplazamientos y las reacciones en los empotramientos, las
deformaciones y los esfuerzos de la estructura mostrada en la figura adjunta
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from funciones import t2ft_R89_axisimetrico, compartir_variables, plot_esf_def

# %% constantes que ayudarán en la lectura del código
X, Y = 0, 1
NL1, NL2, NL3, NL4, NL5, NL6, NL7, NL8 = range(8)
g = 9.81 # [m/s²]   aceleración de la gravedad

# %% seleccione la malla a emplear:
nombre_archivo = 'boussinesq'
df = pd.read_excel(f'{nombre_archivo}.xlsx', sheet_name=None)

# %% posición de los nodos:
# xnod: fila=número del nodo, columna=coordenada X=0 o Y=1
xnod = df['xnod'][['x', 'y']].to_numpy()
nno  = xnod.shape[0]    # número de nodos (número de filas de la matriz xnod)

# %% definición de los grados de libertad
ngdl = 2*nno            # número de grados de libertad por nodo = [X, Y]
gdl  = np.reshape(np.arange(ngdl), (nno, 2)) # nodos vs grados de libertad

# %% definición de elementos finitos con respecto a nodos
# LaG: fila=número del elemento, columna=número del nodo local
LaG = df['LaG_mat'][['NL1', 'NL2', 'NL3', 'NL4', 'NL5', 'NL6', 'NL7', 'NL8']].to_numpy() - 1
# se carga el número del material
mat = df['LaG_mat']['material'].to_numpy() - 1
nef = LaG.shape[0]      # número de EFs (número de filas de la matriz LaG)

# %% material
Ee   = df['prop_mat']['E'].to_numpy()   # [Pa]     módulo de elasticidad del sólido
nue  = df['prop_mat']['nu'].to_numpy()  # [-]      coeficiente de Poisson
rhoe = df['prop_mat']['rho'].to_numpy() # [kg/m³]  densidad
nmat = Ee.shape[0]                      # número de materiales

# %% relación de cargas puntuales
cp  = df['carga_punt']
ncp = cp.shape[0]       # número de cargas puntuales
f   = np.zeros(ngdl)    # vector de fuerzas nodales equivalentes global
for i in range(ncp):
   f[gdl[cp['nodo'][i]-1, cp['dirección'][i]-1]] = cp['fuerza puntual'][i]

# %% Se dibuja la malla de elementos finitos
cg = np.zeros((nef,2))  # almacena el centro de gravedad de los EF
plt.figure()
for e in range(nef):
    # se dibujan las aristas
    nod_ef = LaG[e, [NL1, NL2, NL3, NL4, NL5, NL6, NL7, NL8, NL1]]
    plt.plot(xnod[nod_ef, X], xnod[nod_ef, Y], 'b')
    # se calcula la posición del centro de gravedad
    cg[e] = np.mean(xnod[LaG[e]], axis = 0)
    # y se reporta el número del elemento actual
    plt.text(cg[e,X], cg[e,Y], f'{e+1}', horizontalalignment='center',
                                         verticalalignment='center',  color='b')

# en todos los nodos se dibuja un marcador y se reporta su numeración
plt.plot(xnod[:, X], xnod[:, Y], 'r*')
for i in range(nno):
    plt.text(xnod[i, X], xnod[i, Y], f'{i+1}', color = 'r')

plt.gca().set_aspect('equal', adjustable = 'box')
plt.tight_layout()
plt.title('Malla de elementos finitos')
plt.show()

#%% Funciones de forma (serendípitas) y sus derivadas del elemento rectangular
#   de 8 nodos:
Nforma = lambda xi,eta: np.array(
                        [-((eta - 1)*(xi - 1)*(eta + xi + 1))/4,    # N1
                          ((xi**2 - 1)*(eta - 1))/2,                # N2
                          ((eta - 1)*(xi + 1)*(eta - xi + 1))/4,    # N3
                         -((eta**2 - 1)*(xi + 1))/2,                # N4
                          ((eta + 1)*(xi + 1)*(eta + xi - 1))/4,    # N5
                         -((xi**2 - 1)*(eta + 1))/2,                # N6
                          ((eta + 1)*(xi - 1)*(xi - eta + 1))/4,    # N7
                          ((eta**2 - 1)*(xi - 1))/2              ]) # N8

# derivadas de las funciones de forma con respecto a xi
dN_dxi = lambda xi,eta: np.array(
                        [-((eta + 2*xi)*(eta - 1))/4,    # dN1_dxi
                          eta*xi - xi,                   # dN2_dxi
                          ((eta - 2*xi)*(eta - 1))/4,    # dN3_dxi
                          1/2 - eta**2/2,                # dN4_dxi
                          ((eta + 2*xi)*(eta + 1))/4,    # dN5_dxi
                         -xi*(eta + 1),                  # dN6_dxi
                         -((eta - 2*xi)*(eta + 1))/4,    # dN7_dxi
                          eta**2/2 - 1/2              ]) # dN8_dxi

# derivadas de N con respecto a eta
dN_deta = lambda xi,eta: np.array(
                         [-((2*eta + xi)*(xi - 1))/4,    # dN1_deta
                           xi**2/2 - 1/2,                # dN2_deta
                           ((xi + 1)*(2*eta - xi))/4,    # dN3_deta
                          -eta*(xi + 1),                 # dN4_deta
                           ((2*eta + xi)*(xi + 1))/4,    # dN5_deta
                           1/2 - xi**2/2,                # dN6_deta
                          -((xi - 1)*(2*eta - xi))/4,    # dN7_deta
                           eta*(xi - 1)               ]) # dN8_deta

#%% Cuadratura de Gauss-Legendre
# NOTA: se asumirá aquí el mismo orden de la cuadratura tanto en la dirección
#       de xi como en la dirección de eta
n_gl       = 2                       # orden de la cuadratura de Gauss-Legendre
x_gl, w_gl = np.polynomial.legendre.leggauss(n_gl)

# %% Ensamblaje la matriz de rigidez global y el vector de fuerzas másicas
#    nodales equivalentes global

# se inicializan la matriz de rigidez global y los espacios en memoria que
#  almacenarán las matrices de forma y de deformación
K = np.zeros((ngdl, ngdl))          # matriz de rigidez global
N = np.empty((nef,n_gl,n_gl,2,2*8)) # matriz de forma en cada punto de GL
B = np.empty((nef,n_gl,n_gl,4,2*8)) # matriz de deformaciones en cada punto de GL
idx = nef * [None]                  # indices asociados a los gdl del EF e

# matriz constitutiva del elemento para el caso AXISIMETRICO
De = nmat * [ None ]
be = nmat * [ None ]
for i in range(nmat):
    De[i] = (Ee[i]/((1+nue[i])*(1-2*nue[i])))*\
        np.array([[1 - nue[i],  nue[i],    nue[i],    0             ],
                  [nue[i],      1-nue[i],  nue[i],    0             ],
                  [nue[i],      nue[i],    1-nue[i],  0             ],
                  [0,           0,         0,         (1-2*nue[i])/2]])
    be[i] = np.array([0, -rhoe[i]*g])  # [kgf/m³] vector de fuerzas másicas

# para cada elemento finito en la malla:
for e in range(nef):
    # se calculan con el siguiente ciclo las matrices de rigidez y el vector de
    # fuerzas nodales equivalentes del elemento usando las cuadraturas de GL
    Ke = np.zeros((16, 16))
    fe = np.zeros(16)
    det_Je = np.empty((n_gl, n_gl))      # matriz para almacenar los jacobianos

    for p in range(n_gl):
        for q in range(n_gl):
            # en cada punto de la cuadratura de Gauss-Legendre se evalúan las
            # funciones de forma y sus derivadas
            xi_gl, eta_gl = x_gl[p], x_gl[q]

            NNforma  = Nforma (xi_gl, eta_gl)
            ddN_dxi  = dN_dxi (xi_gl, eta_gl)
            ddN_deta = dN_deta(xi_gl, eta_gl)

            # se llaman las coordenadas nodales del elemento para calcular las
            # derivadas de la función de transformación
            xe, ye = xnod[LaG[e], X], xnod[LaG[e], Y]

            dx_dxi  = np.sum(ddN_dxi  * xe);    dy_dxi  = np.sum(ddN_dxi  * ye)
            dx_deta = np.sum(ddN_deta * xe);    dy_deta = np.sum(ddN_deta * ye)

            # se calcula el radio del punto de Gauss
            r = np.sum(NNforma * xe)

            # con ellas se ensambla la matriz Jacobiana del elemento y se
            # calcula su determinante
            Je = np.array([[dx_dxi,  dy_dxi ],
                           [dx_deta, dy_deta]])
            det_Je[p, q] = np.linalg.det(Je)

            # las matrices de forma y de deformación se evalúan y se ensamblan
            # en el punto de Gauss
            Npq = np.empty((2, 2*8))
            Bpq = np.empty((4, 2*8))
            for i in range(8):
                Npq[:,[2*i, 2*i+1]] = np.array([[NNforma[i], 0         ],
                                                [0,          NNforma[i]]])

                dNi_dx = (+dy_deta*ddN_dxi[i] - dy_dxi*ddN_deta[i])/det_Je[p,q]
                dNi_dy = (-dx_deta*ddN_dxi[i] + dx_dxi*ddN_deta[i])/det_Je[p,q]
                Bpq[:,[2*i, 2*i+1]] = np.array([[dNi_dx,       0     ],
                                                [0,            dNi_dy],
                                                [NNforma[i]/r, 0     ],
                                                [dNi_dy,       dNi_dx]])
            N[e,p,q] = Npq
            B[e,p,q] = Bpq

            # se ensamblan la matriz de rigidez del elemento y el vector de
            # fuerzas nodales equivalentes del elemento
            Ke += Bpq.T @ De[mat[e]] @ Bpq * det_Je[p,q]*r*w_gl[p]*w_gl[q]
            fe += Npq.T @ be[mat[e]]       * det_Je[p,q]*r*w_gl[p]*w_gl[q]
    Ke *= 2*np.pi
    fe *= 2*np.pi

    # se determina si hay puntos con jacobiano negativo, en caso tal se termina
    # el programa y se reporta
    if np.any(det_Je <= 0):
        raise Exception(f'Hay puntos con det_Je negativo en el elemento {e+1}')

    # y se añaden la matriz de rigidez del elemento y el vector de fuerzas
    # nodales del elemento a sus respectivos arreglos de la estructura
    idx[e] = gdl[LaG[e]].flatten() # se obtienen los grados de libertad
    K[np.ix_(idx[e], idx[e])] += Ke
    f[np.ix_(idx[e])]         += fe

# %% Muestro la configuración de la matriz K (K es rala)
plt.figure()
plt.spy(K)
plt.title('Los puntos representan los elementos diferentes de cero')
plt.show()

#%% Cálculo de las cargas nodales equivalentes de las cargas distribuidas:
cd   = df['carga_distr']
nlcd = cd.shape[0]     # número de lados con carga distribuida
ft   = np.zeros(ngdl)  # fuerzas nodales equivalentes de cargas superficiales

# por cada lado cargado se obtienen las fuerzas nodales equivalentes en los
# nodos y se añaden al vector de fuerzas superficiales
for i in range(nlcd):
   e     = cd['elemento'][i] - 1
   lado  = cd['lado'][i]
   carga = cd[['tix', 'tiy', 'tjx', 'tjy', 'tkx', 'tky']].loc[i].to_numpy()
   fte   = t2ft_R89_axisimetrico(xnod[LaG[e,:],:], lado, carga)

   ft[np.ix_(idx[e])] += fte

# %% agrego al vector de fuerzas nodales equivalentes las fuerzas
# superficiales calculadas
f += ft

# %% restricciones y los grados de libertad del desplazamiento conocidos (c)
restric = df['restric']
nres = restric.shape[0]
c    = np.empty(nres, dtype=int)
for i in range(nres):
   c[i] = gdl[restric['nodo'][i]-1, restric['dirección'][i]-1]

# desplazamientos conocidos
ac = restric['desplazamiento'].to_numpy()

# grados de libertad del desplazamiento desconocidos
d = np.setdiff1d(range(ngdl), c)

# %% extraigo las submatrices y especifico las cantidades conocidas
# f = vector de fuerzas nodales equivalentes
# q = vector de fuerzas nodales de equilibrio del elemento
# a = desplazamientos

#| qd |   | Kcc Kcd || ac |   | fd |  # recuerde que qc=0 (siempre)
#|    | = |         ||    | - |    |
#| qc |   | Kdc Kdd || ad |   | fc |
Kcc = K[np.ix_(c,c)];  Kcd = K[np.ix_(c,d)]; fd = f[c]
Kdc = K[np.ix_(d,c)];  Kdd = K[np.ix_(d,d)]; fc = f[d]

# %% resuelvo el sistema de ecuaciones
ad = np.linalg.solve(Kdd, fc - Kdc@ac) # desplazamientos desconocidos
qd = Kcc@ac + Kcd@ad - fd              # fuerzas de equilibrio desconocidas

# armo los vectores de desplazamientos (a) y fuerzas (q)
a = np.zeros(ngdl); q = np.zeros(ngdl) # separo la memoria
a[c] = ac;          a[d] = ad          # desplazamientos
q[c] = qd         # q[d] = qc = 0      # fuerzas nodales de equilibrio

# %% Dibujo la malla de elementos finitos y las deformada de esta
delta  = np.reshape(a, (nno,2))
escala = 1000                   # factor de escalamiento de la deformada
xdef   = xnod + escala*delta    # posición de la deformada

plt.figure()
for e in range(nef):
   nod_ef = LaG[e, [NL1, NL2, NL3, NL4, NL5, NL6, NL7, NL8, NL1]]
   plt.plot(xnod[nod_ef, X], xnod[nod_ef, Y], 'r',
                        label='Posición original'  if e == 0 else "", lw=0.5)
   plt.plot(xdef[nod_ef, X], xdef[nod_ef, Y], 'b',
                        label='Posición deformada' if e == 0 else "")
plt.gca().set_aspect('equal', adjustable='box')
plt.legend()
plt.xlabel('$r$ [m]')
plt.ylabel('$z$ [m]')
plt.title(f'Deformada escalada {escala} veces')
plt.tight_layout()
plt.show()

#%% Deformaciones y los esfuerzos en los puntos de Gauss
deform = np.zeros((nef,n_gl,n_gl,4)) # deformaciones en cada punto de GL
esfuer = np.zeros((nef,n_gl,n_gl,4)) # esfuerzos en cada punto de GL

for e in range(nef):
    ae = a[idx[e]]    # desplazamientos nodales del elemento e
    for pp in range(n_gl):
        for qq in range(n_gl):
            deform[e,pp,qq] = B[e,pp,qq] @ ae              # calculo las deformaciones
            esfuer[e,pp,qq] = De[mat[e]] @ deform[e,pp,qq] # calculo los esfuerzos

#%% Esfuerzos y deformaciones en los nodos:
num_elem_ady = np.zeros(nno)
sr  = np.zeros(nno);        er  = np.zeros(nno)
sz  = np.zeros(nno);        ez  = np.zeros(nno)
st  = np.zeros(nno);        et = np.zeros(nno)
trz = np.zeros(nno);        grz = np.zeros(nno)

# matriz de extrapolación
A = np.array([
    [  3**(1/2)/2 + 1,             -1/2,             -1/2,   1 - 3**(1/2)/2],
    [3**(1/2)/4 + 1/4, 1/4 - 3**(1/2)/4, 3**(1/2)/4 + 1/4, 1/4 - 3**(1/2)/4],
    [            -1/2,   1 - 3**(1/2)/2,   3**(1/2)/2 + 1,             -1/2],
    [1/4 - 3**(1/2)/4, 1/4 - 3**(1/2)/4, 3**(1/2)/4 + 1/4, 3**(1/2)/4 + 1/4],
    [  1 - 3**(1/2)/2,             -1/2,             -1/2,   3**(1/2)/2 + 1],
    [1/4 - 3**(1/2)/4, 3**(1/2)/4 + 1/4, 1/4 - 3**(1/2)/4, 3**(1/2)/4 + 1/4],
    [            -1/2,   3**(1/2)/2 + 1,   1 - 3**(1/2)/2,             -1/2],
    [3**(1/2)/4 + 1/4, 3**(1/2)/4 + 1/4, 1/4 - 3**(1/2)/4, 1/4 - 3**(1/2)/4]])

# se hace la extrapolación de los esfuerzos y las deformaciones en cada elemento
# a partir de las lecturas en los puntos de Gauss
for e in range(nef):
    #sr[LaG[e]]  += A @ np.array([esfuer[e,0,0,0],   # I   = (p=0, q=0)
    #                             esfuer[e,0,1,0],   # II  = (p=0, q=1)
    #                             esfuer[e,1,0,0],   # III = (p=1, q=0)
    #                             esfuer[e,1,1,0]])  # IV  = (p=1, q=1)
    sr [LaG[e]] += A @ esfuer[e,:,:,0].ravel()
    sz [LaG[e]] += A @ esfuer[e,:,:,1].ravel()
    st [LaG[e]] += A @ esfuer[e,:,:,2].ravel()
    trz[LaG[e]] += A @ esfuer[e,:,:,3].ravel()
    er [LaG[e]] += A @ deform[e,:,:,0].ravel()
    ez [LaG[e]] += A @ deform[e,:,:,1].ravel()
    et [LaG[e]] += A @ deform[e,:,:,2].ravel()    
    grz[LaG[e]] += A @ deform[e,:,:,3].ravel()

    # se lleva un conteo de los elementos adyacentes a un nodo
    num_elem_ady[LaG[e]] += 1

# en todos los nodos se promedia los esfuerzos y las deformaciones de los
# elementos, se alisa la malla de resultados
sr  /= num_elem_ady;   er  /= num_elem_ady
sz  /= num_elem_ady;   ez  /= num_elem_ady
st  /= num_elem_ady;   et  /= num_elem_ady
trz /= num_elem_ady;   grz /= num_elem_ady
trt = 0
ttz = 0


# %% Se calculan para cada nodo los esfuerzos principales y sus direcciones
s1 = np.zeros(nno);  n1 = np.zeros((nno, 3))
s2 = np.zeros(nno);  n2 = np.zeros((nno, 3))
s3 = np.zeros(nno);  n3 = np.zeros((nno, 3))
for i in range(nno):
    esfppales, dirppales = np.linalg.eigh(
                             [[sr[i],   trt,    trz[i]],  # matriz de esfuerzos
                              [trt,     st[i],  ttz   ],  # de Cauchy para 
                              [trz[i],  ttz,    sz[i] ]]) # theta = grados

    idx_esf = esfppales.argsort()[::-1] # ordene de mayor a menor
    s1[i], s2[i], s3[i] = esfppales[idx_esf]
    n1[i] = dirppales[:,idx_esf[0]]
    n2[i] = dirppales[:,idx_esf[1]]
    n3[i] = dirppales[:,idx_esf[2]]

# Esfuerzo cortante máximo
tmax = (s1-s3)/2                               # esfuerzo cortante máximo
   
# %% Calculo de los esfuerzos de von Mises
sv   = np.sqrt(((s1-s2)**2 + (s2-s3)**2 + (s1-s3)**2)/2)

# %% Gráfica del post-proceso:
# las matrices xnod y LaG se vuelven variables globales por facilidad
compartir_variables(xnod, LaG)

# deformaciones
plot_esf_def(er,   r'$\epsilon_r$')
plot_esf_def(ez,   r'$\epsilon_z$')
plot_esf_def(et,   r'$\epsilon_\theta$')
plot_esf_def(grz,  r'$\gamma_{rz}$ [rad]')

# esfuerzos
plot_esf_def(sr,   r'$\sigma_r$ [Pa]')
plot_esf_def(sz,   r'$\sigma_z$ [Pa]')
plot_esf_def(st,   r'$\sigma_\theta$ [Pa]')
plot_esf_def(trz,  r'$\tau_{rz}$ [Pa]')

# esfuerzos principales con sus orientaciones
# plot_esf_def(s1,   r'$\sigma_1$ [Pa]',     ang                       )
# plot_esf_def(s2,   r'$\sigma_2$ [Pa]',     ang+np.pi/2               )
# plot_esf_def(tmax, r'$\tau_{máx}$ [Pa]', [ ang-np.pi/4, ang+np.pi/4 ])

# esfuerzos de von Mises
# plot_esf_def(sv,   r'$\sigma_{VM}$ [Pa]')

# %% Reporte de los resultados:

# se crean tablas para reportar los resultados nodales de: desplazamientos (a),
# fuerzas nodales equivalentes (f) y fuerzas nodales de equilibrio (q)
tabla_afq = pd.DataFrame(
    data=np.c_[a.reshape((nno,2)), f.reshape((nno,2)), q.reshape((nno,2))],
    index=np.arange(nno)+1,
    columns=['ur [m]', 'w [m]', 'fr [N]', 'fz [N]', 'qr [N]', 'qz [N]'])
tabla_afq.index.name = '# nodo'

# deformaciones
tabla_def = pd.DataFrame(data    = np.c_[er, ez, et, grz],
                         index   = np.arange(nno) + 1,
                         columns = ['er', 'ez', 'et', 'grz [rad]'])
tabla_def.index.name = '# nodo'

# esfuerzos
tabla_esf = pd.DataFrame(data    = np.c_[sr, sz, st, trz],
                         index   = np.arange(nno) + 1,
                         columns = ['sr [Pa]', 'sz [Pa]', 'st [Pa]', 'trz [Pa]'])
tabla_esf.index.name = '# nodo'

# esfuerzos principales y de von Misses:
tabla_epv = pd.DataFrame(
       data    = np.c_[s1, s2, s3, tmax, sv, n1, n2, n3],
       index   = np.arange(nno) + 1,
       columns = ['s1 [Pa]', 's2 [Pa]', 's3 [Pa]', 'tmax [Pa]', 'sv [Pa]',
                  'n1x', 'n1y', 'n1z',
                  'n2x', 'n2y', 'n2z', 
                  'n3x', 'n3y', 'n3z'])
tabla_epv.index.name = '# nodo'

# se crea un archivo de MS EXCEL
writer = pd.ExcelWriter(f"resultados_{nombre_archivo}.xlsx", engine = 'xlsxwriter')

# cada tabla hecha previamente es guardada en una hoja del archivo de Excel
tabla_afq.to_excel(writer, sheet_name = 'afq')
tabla_def.to_excel(writer, sheet_name = 'deformaciones')
tabla_esf.to_excel(writer, sheet_name = 'esfuerzos')
tabla_epv.to_excel(writer, sheet_name = 'esf_ppales')
writer.save()

print(f'Cálculo finalizado. En "resultados_{nombre_archivo}.xlsx" se guardaron los resultados.')

# %% Se genera un archivo .VTK para visualizar en Paraview
# Instale meshio (https://github.com/nschloe/meshio) con:
# ! pip install meshio[all] --user

import meshio
meshio.write_points_cells(
    f"resultados_{nombre_archivo}.vtk",
    points = xnod,
    cells = {"quad8": LaG[:,[0,2,4,6,1,3,5,7]] },
    point_data = {
        'er':er, 'ez':ez, 'et':et, 'grz':grz,
        'sr':sr, 'sz':sz, 'st':st, 'trz':trz,
        's1':s1, 's2':s2, 's3':s3, 'tmax':tmax, 'sv':sv,
        'uv'  : a.reshape((nno,2)),
        'n1'  : n1, 
        'n2'  : n2, 
        'n3'  : n3
        },
#    cell_data = {"quad8" : {"material" : mat}}
    # field_data=field_data
)
# %% Resultados en punto de referencia
a1 = tabla_afq.loc[4].to_numpy()
d1 = tabla_def.loc[4].to_numpy()
s1 = tabla_esf.loc[4].to_numpy()

np.savetxt('a1.csv', a1)
np.savetxt('d1.csv', d1)
np.savetxt('s1.csv', s1)

# %%bye, bye!
