# Ejercicios de planificación con Fast Downward

## Dominio de transporte aéreo de cargas
La consigna consiste en modelar en PDDl el dominio de transporte aéreo de cargas y definir algunas instancias del problema para luego encontrar soluciones con el planificador Fast Downward.

El modelado del problema fue basado en el ejemplo de planificación visto en clase.

En el archivo [domain3a.pddl](planning/domain3a.pddl) se definió el dominio del problema, con los predicados *LOAD*, *PLANE* y *AIRPORT* para definir variables y *in* y *at* para definir estados de las variables. Las acciones definidas fueron:

- *fly*, parámetros *p*, *from* y *to*. Acción en la que el avión *p* vuela del aeropuerto *from* al aeropuerto *to*.
- *load*, parámetros *c*, *p* y *a*. Acción de cargar *c*, en el avión *p*, en el aeropuerto *a*.
- *unload*, parámetros *c*, *p* y *a*. Acción de descargar *c*, en el avión *p*, en el aeropuerto *a*.

En el archivo [task3a.pddl](planning/task3a.pddl) se dan las condiciones iniciales del problema en específico, instanciando dos aviones, dos aeropuertos y dos cargas diferentes; y el estado objetivo donde las cargas deben estar en los aeropuertos diferentes al que comienzan.

### Solución
```
 (load c2 p2 jfk)
 (fly p2 jfk sf0)
 (unload c2 p2 sf0)
 (load c1 p2 sf0)
 (fly p2 sf0 jfk)
 (unload c1 p2 jfk)
 ; cost = 6 (unit cost)
```

### Dificultades
No se pudo lograr que el planificador logre paralelizar el problema para que contemple en la solución el uso de ambos aviones (reduciendo el costo temporal). Se concluyó que dado que el planificador Fast Downward solo soporta hasta PDDL 2, no se puede realizar esto en dicha versión del lenguaje.

## Planificación de Procesos Asistida por Computadora
La consigna consiste en modelar en PDDL y definir una instancia del problema de planificación de Procesos Asistida por Computadora (CAPP, Computer-Aided Process Planning).

En el archivo [domain3b.pddl](planning/domain3b.pddl) se definió el dominio del problema, con los predicados *CUERPO*, *HERRAMIENTA*, *ARMARIO*, *HUSILLO*, *DIRECCIÓN*, *AGUJERO* y *RANURA* para definir variables y *en* y *vinculo* (para relacionar un tipo de operación con determinada herramienta) para definir estados de las variables. Las acciones definidas fueron:

- *cambio-herramienta*, parámetros *h1*, *h2*, *a* y *m*. Acción en la que se reemplaza las herramientas *h1* y *h2* que están en el armario *a* y el husillo de la máquina *m* respectivamente.
- *agujerear*, parámetros *p*, *h*, *m* y *a*. Acción de realizar un agujero tipo *a* en el cuerpo *p* con la herramienta *h* en el husillo de la máquina *m*.
- *fresar*, parámetros *p*, *h*, *m* y *r*. Acción de realizar una ranura tipo *r* en el cuerpo *p* con la herramienta *h* en el husillo de la máquina *m*.

En el archivo [task3b.pddl](planning/task3b.pddl) se dan las condiciones iniciales del problema en específico, instanciando tres herramientas para realizar tres tipos de gujeros diferentes (brocas), tres tipos de herramientas para realizar tres tipos de ranuras (fresas) y la materia prima; y el estado objetivo donde ya se encuentra el producto final con los tres agujeros y ranuras realizados.

### Solución

```
(fresar p f1 m r1)
(cambio-herramienta b1 f1 a m)
(agujerear p b1 m h1)
(cambio-herramienta b2 b1 a m)
(agujerear p b2 m h2)
(cambio-herramienta b3 b2 a m)
(agujerear p b3 m h3)
(cambio-herramienta f2 b3 a m)
(fresar p f2 m r2)
(cambio-herramienta f3 f2 a m)
(fresar p f3 m r3)
; cost = 11 (unit cost)
```

### Dificulatades
Dado que el planificador Fast Downward soporta PDDL solo hasta segunda versión, no se pudo implementar restricciones blandas de precedencia entre las tareas, pero se expresaría de la siguiente manera:

```
(:goal
...
    (preference precendencia
        (sometime-after (en p r2) (en p r1))
        (sometime-after (en p h1) (en p r1))
    )

...
)
```

Explicitando la preferencia de ejecución de dos tareas en un determinado orden, y estableciendo un métrica de la forma:

```
(:metric (minimize (is-violated precedencia)))
```