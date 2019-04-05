# Inteligencia Artificial 2

Repositorio incluyendo los trabajos prácticos de la cátedra Inteligencia Artificial 2 de la carrera Ingeniería en Mecatrónica

Facultad de Ingeniería
Universidad Nacional de Cuyo 

# Integrantes

Gonzalo Fernández, Emiliano Cabrino, Gino Avanzini y Adrián Cantaloube

# Desarrollo

## Implementación del algoritmo A* para trayectoria de robot de 6 grados de libertad
El problema del robot con 6 grados de libertad fue modelado en el espacio articular, donde cada estado del problema es el valor angular de cada articulación con una discretización de ángulos sexagecimales enteros, es decir, un vector de estado es una lista de 6 componentes enteros.

La función heurística adoptada en el modelo es la raíz cuadrada de la suma del cuadrado de cada componente, distancia euclidiana del espacio de estados, desde el estado en cuestión al estado objetivo.

El estado inicial es sencillamente la configuración inicial del brazo robótico. La prueba de meta es la comprobación de si el estado actual es igual al estado objetivo, es decir, comprobar si el valor angular de cada articulación es igual el objetivo.


2019 UNCuyo
