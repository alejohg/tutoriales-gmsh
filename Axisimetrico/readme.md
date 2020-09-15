# Modificación de un programa de análisis por MEF para el caso axisimétrico, usando elementos finítos serendípitos de 8 nodos.

## Objetivo: 
Modificar el programa dado [ejemplo_Q8_axisimetrico_original.py](/ejemplo_Q8_axisimetrico_original.py) (por: Diego A. Álvarez) de tal manera los datos de entrada puedan ser leídos directamente desde una malla creada en GMSH, haciendo uso de los grupos físicos.

El programa con todas las modificaciones respectivas es el siguiente: [ejemplo_Q8_axisimetrico_modificado.py](/ejemplo_Q8_axisimetrico_modificado.py).

## Descripción de modificaciones realizadas:

### Lectura de propiedades de material
Cada superficie distinta creada en GMSH corresponderá en esencia a un "material diferente", incluso si sus propiedades fuesen iguales, ya que GMSH reportará los elementos finitos como pertenecientes a una entidad distinta.
Para cada superficie se debe asignar un grupo físico con la sintaxis *mat_E_$\nu$_$\rho$*, por ejemplo: Si se trata de un material con E = 2e8 Pa, $\nu$ = 0.3 y $\rho$ = 2400 kg/m³, la superficie física asociada debería llamarse *mat_1e8_0.3_2400*, el programa leerá los números entre guiones bajos en ese orden, siempre y cuando estén escritos de tal modo que Python los pueda convertir a flotantes.

### Condiciones de frontera:
Se aplican sobre
