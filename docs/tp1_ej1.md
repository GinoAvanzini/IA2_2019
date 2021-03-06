 
---
title:  'Trabajo práctico N°1: Búsqueda y Optimización'
author:
- Gino Avanzini
- Emiliano Cabrino
- Adrián Cantaloube
- Gonzalo Fernández


...

# Análisis y selección de algoritmos según el tipo de problema

En los problemas enunciados abajo
- Qué algoritmo/s utilizaría en cada caso. Justifique.
- Defina el problema (estado inicial, modelo de transición, prueba de meta, funciones heurísticas si
aplican, función de costo/calidad)
- Estime la complejidad del problema y del algoritmo


## Diseño de un proceso de manufactura

Es un problema de satisfacción de restricciones: necesitamos encontrar el plan de manufactura. La resolución del problema nos permite crear dicho plan describiendo un estado inicial y un objetivo, siendo ambos fijados por el encargado de la manufactura, y las tareas que se podrán llevar a cabo. Un estado está definido por el instante de tiempo en que cada tarea debe comenzar a realizarse. Cada tarea lleva consigo precondiciones que se deberán cumplir para que esta tarea se lleve a cabo y el planificador deberá diseñar el plan para que la manufactura sea correcta y lo mas fluida posible describiendo el modelo de transición. Al finalizar el algoritmo se calcularán costos de dinero y tiempo de manufactura y se comprobará si la planificación cumple con las expectativas. De otra forma se deberá reconstruir para buscar una mejor solución.
  
Para encontrar la solución podemos recurrir a algoritmos genéticos o a un algoritmo como el de backtracking. 

## Planificación de órdenes de fabricación

Es un problema de planificación. Cuando las empresas trabajan con pedidos es común que estos lleguen todos los días de forma desorganizada. Es necesario agruparlos para que la producción se lleve a cabo de forma simultánea. Por ejemplo: llegaron pedidos de un mismo modelo, de clientes diferentes, ellos pueden ser cortados y fabricados al mismo tiempo. Con ese agrupamiento se estará elaborando una única orden de fabricación. Ahorrando tiempo al evitar un seccionamiento innecesario.

El orden del plan y el ahorro a la hora de planificar se pueden basar según el valor de facturación o según el plazo y cantidad de productos.
  
Para poder resolver este problema podemos usar un algoritmo de temple simulado. Un estado sería una asignación completa de tiempos en los que deben comenzar los procesos de manufactura de cada orden. Además verificamos que las asignaciones sean válidas mediante algoritmos de consistencia de arco y nodo. Como función de energía se puede tener en cuenta el tiempo total de ejecución de todas las órdenes, los tiempos muertos, etc. Se buscaría minimizar esta función de energía, premiando los trabajos que se realizan en paralelo y penando aquellas asignaciones que implican mayor tiempo total de ejecución.

## Encontrar la ubicación óptima de aerogeneradores en un parque eólico

Es un problema de optimización: Se busca maximizar la energía generada por un determinado número de aerogeneradores en un campo eólico dada la información sobre el viento en la zona. Para lograrlo hay que determinar la mejor disposición de los generadores en el parque.
  
La resolución del problema se puede encasillar dentro de la familia de algoritmos de búsqueda continua. Además se puede discretizar el espacion y convertir el problema a uno de búsqueda clásico. Entre ellos se encuentran, por ejemplo, los algoritmos genéticos y de recocido simulado. El estado inicial del problema es obtener un configuración aleatoria de los generadores en el espacio del campo. El modelo de transición consiste en reubicar alguno de los aerogeneradores en otra posición del campo y proseguir con el algoritmo, evaluando si el nuevo estado produce una mejora o no con la función objetivo.

La función de energía (en el caso del temple) es una función que dada la información del viento en la zona, valora qué tan buena es la distribución de generadores. Para generar estados vecinos se puede reubicar cierta cantidad de generadores y evaluar la nueva configuración. 

Además, si se quisiera, se podría fraccionar el campo eólico en sectores y hacer optimizaciones locales en esos sectores. De esta forma se podría paralelizar el problema y obtener una solución más rápidamente. 

## Planificar trayectorias de un brazo robótico con 6 grados de libertad

Es un problema de planificación y/o optimización: Se busca una combinación entre ambas, planificación para conocer las acciones que debe tomar, y optimización para llegar del estado inicial al final con el menor gasto posible. Ambas nos ayudarán a tomar decisiones en tiempo real ya que trabajan en conjunto. 

El estado inicial y final son descriptas por el operario y no generadas aleatoriamente. Con el modelo de transición vemos el movimiento de los eslabones del robot para llegar al próximo estado (punto discretizado de la trayectoria). Podríamos usar la heurística del ejercicio 2)a de este práctico (A*) para llegar al objetivo. En este caso no podríamos usar algoritmos de búsqueda local ya que no solo debemos llegar al estado final, sino que necesitamos seguir una trayectoria establecida.

## Diseño de un generador

Los problemas de diseño generalmente son de optimización. Esto significa que debemos encontrar la forma de diseñar el generador maximizando el ahorro de recursos y el rendimiento del mismo. Para que el generador cumpla con las especificaciones deseadas, habrá que implementar un algoritmo relacionando las propiedades y cantidades de los materiales a utilizar para saber que tanta eficiencia aportarán al generador. La combinación mas optima es la que utilizaremos como meta.

Para la resolución de este problema podemos utilizar un algoritmo genético. Cada individuo estaría caracterizado por, por ejemplo, cantidad de polos del rotor, tipo de polos, cantidad de vueltas por bobina, material del núclo del estator y el rotor, potencia de salida, etc. Para cada configuración habrá un valor de fitness que será función del costo de construcción, rendimiento estimado y peso, entre otros. 

## Definición de una secuencia de ensamblado óptima

Es un problema de búsqueda. Se quiere encontrar la secuencia óptima de partes a colocar en, por ejemplo, una placa electrónica. 

Para esto podríamos utilizar un algoritmo como el A* en el cual partimos de un componente inicial y queremos buscar la mejor secuencia para colocar todos los componentes, considerando que puede haber varios unidades del mismo tipo en distintos lugares de la placa. 

La heurística sería la distancia en línea recta entre un componente y otro. El costo aumenta al realizar cada viaje a un punto de la placa y al realizar un cambio en el tipo de componente.

Dado que buscamos optimalidad con un A* obtendremos la mejor secuencia. 

## Planificación del proyecto de una obra

Es un problema de planificación. Se busca encontrar un orden en las tareas a realizar (algunas de forma paralela o simultanea) de manera que se cumplan los ordenes de precedencia de cada una de ellas. Se inicia con las tareas de la obra que no requieren requisitos previos para ser ejecutadas. Se procederá con las tareas que requieran la finalización de la/s primera/s y así sucesivamente hasta concluir la obra. Cada tarea conlleva cierto tiempo, parámetro que utilizaremos para calcular las ganancias y estimar el rango de tiempo que nos llevará a cabo realizar la obra.

Se puede utilizar un algoritmo de backtracking junto con un algoritmo para verificación la consistencia de las asignaciones (AC3, etc.)

