
# Implementación de algoritmo de satisfacción de restricciones
---

Se implementó un algoritmo de *backtracking* para resolver el problema de satisfacción de restricciones, más especificamente, de *scheduling*.

## Modelado del problema

El problema consiste en una determinada cantidad de tareas que deben realizarse, donde cada una demanda un determinado tiempo:


```python
T = {"d0": 40, "d1":20, "d2":25, "d3":10, "d4":30}
```

Como restricción global a la hora de asignar valores, se considera desde un principio (acotando el dominio de las variables) que el proceso total debe finalizarse en un tiempo menor a *DLINE*. Además, el tiempo se discretizó en intervalos con valor *STEP*.


```python
DLINE = 150
STEP = 5
```

Por lo tando, la asignación de los valores en el dominio de cada variable es de la forma:


```python
D = {}
for i in T.keys():
    D[i] = list(range(0, DLINE-T[i], STEP))
```

Luego se crea un diccionario vacío que contendra las futuras asignaciones del algoritmo, y se elige una variable aleatoria no asignada (por ser la inicial se elige aleatoriamente de entre todo el conjunto de variables).


```python
from backtracking import selection

assign = {}
print(selection(D, assign))
```

    d0


Es importante tener en cuenta que a la hora de elegir una variable no asignada se puede implementar alguna heurística como *mínimos valores restantes*. En la práctica esto no se realizó.

### Restricciones binarias de precedencia
Las restricciones binarias se describen *harcodeando* la relación de precedencia entre las distintas variables, teniendo en cuenta el orden. 

A continuación se plantea un grafo de restricciones sencillos para que puede verificarse visualmente la solución.


```python
R2 = {
    "d0":[("d0", "d1"), ("d0", "d2")],
    "d1":[("d0", "d1"), ("d1", "d3")],
    "d2":[("d0", "d2"), ("d2", "d4")],
    "d3":[("d1", "d3"), ("d3", "d4")],
    "d4":[("d3", "d4"), ("d2", "d4")]
}
```

### Restricciones binarias de recursos
Cada tarea ocupa máquinas que están disponibles en cantidad limitada, por lo tanto no pueden ejecutarse tareas que requieren de la misma máquina en paralelo. 

Este tipo de restricciones se describen asignando una lista de máquinas requeridas a cada tarea.


```python
M = {
    "d0":["m1", "m3"],
    "d1":["m2", "m4"],
    "d2":["m0"],
    "d3":["m0", "m2", "m3"],
    "d4":["m0", "m4"]
}
```

### Solución
La solución será el diccionario de tareas, con el valor de tiempo inicial en el que se ejecutará cada una.


```python
from backtracking import backtrack

print(backtrack(T, assign, D, R2, M))
```

    {'d4': 75, 'd3': 60, 'd2': 40, 'd0': 0, 'd1': 40}


### Conclusión

El algoritmo por ser *backtracking* básico, sin la implementación de algún otro algoritmo para analizar arco consistencia como *AC-3*, es muy ineficiente pero da soluciones correctas.
