
from a_star2b import a_star, map, Node, vecinos
from random import random, randint

from math import exp


# [INDEPENDIENTE DEL PROBLEMA]
def update_T(temp):
    """
    Función interna del algoritmo de recocido simulado. Recibe como parámetro la temperatura actual en la que se encuentra el sistema (temp), y se devuelve el valor de temperatura para la siguiente iteración.
    Se utiliza un perfil de temperatura lineal, donde la actualización solo es una reducción del valor en una constante (1). Esto podría modificarse para obtener distintos perfiles.
    """
    return temp - 1


# [INDEPENDIENTE DEL PROBLEMA]
def temple_simulado(productos, t_inicial, neighbour, energy):
    """
    Función principal del algoritmo de recocido simulado. Recibe como parámetro la temperatura inicial del sistema (t_inicial) y un determinado estado inicial del sistema (productos). Como parámetros opcionales se considera una función para generar el próximo estado (neighbour) y una función para calcular la energía del estado (energy), ambas dependen del modelo del problema.
    Se devuelve el mejor estado encontrado, en forma de lista (historic_best), donde la primer componente es la descripción del estado y la segunda la energía del mismo.
    """
    current = productos

    temp = t_inicial

    historic_best = [current, energy(current)]

    while(1):

        if (temp == 0): return historic_best

        next = neighbour(current)

        current_energy = energy(current)
        next_energy = energy(next)

        # Guardo el mejor camino histórico
        if (next_energy <= historic_best[1]):
            historic_best[0] = next
            historic_best[1] = next_energy

        delta = next_energy - current_energy

        if (delta < 0): # Mejor camino (menos distancia recorrida)
            current = next
        else: # delta is positive -> worse path
            prob = exp(-delta/temp)
            # print(prob)
            if (random() < prob):
                current = next

        temp = update_T(temp)


#-------------------------------------------------------------------------------
#   MODELADO DEL PROBLEMA
#-------------------------------------------------------------------------------

# [DEPENDIENTE DEL PROBLEMA]
def neighbours_annealing(current):
    """
    Generación de un estado vecino aleatorio. La función recibe como parámetro el estado actual del sistema, y devuelve el vecino de dicho estado.
    """
    pos = []

    # Generacion de posicion de componentes a intercambiar
    i = 0
    while(i < 2):
        pos.append(randint(1, len(current) - 2)) # Para no tomar el end o start
        if (i != 0 and pos[i] == pos[i-1]):
            # Verifico que no sean iguales. Si no podría no haber intecambio
            i -= 1
            pos.pop()
        i += 1

    # Swap de componentes
    vecino = list(current)

    temp = vecino[pos[0]]
    vecino[pos[0]] = vecino[pos[1]]
    vecino[pos[1]] = temp

    return vecino


# [DEPENDIENTE DEL PROBLEMA] Es la heurística del algoritmo???
def distance(path):
    """
    Cálculo de la energía de un determinado estado. Depende del modelado del problema. Recibe como parámetro el estado al que se le desea calcular la energía y devuelve el valor de esta.
    """

    distance = 0

    for i in range(1, len(path)):
        distance += len(a_star(Node(path[i]), Node(path[i - 1]), vecinos)[0]) - 1

    return distance


def map_to_coord(pos_pick):
    """
    Función parte del modelo del problema. Recibe la lista de productos, donde cada item se encuentra en un estante numerado entre 0 y 31. Devuelve una lista con los mismos productos pero esta vez descriptos en coordenadas cartesianas del depósito. A la lista se agregan el inicio y el final, donde se supone que el picking comienza y finaliza en la coordenada (0, 0).
    """

    coordenadas = []

    for i in pos_pick:
        for fila in range(0, len(map)):
            if i in map[fila]:
                coordenadas.append([fila, map[fila].index(i)])

                if (map[coordenadas[-1][0]][coordenadas[-1][1]] % 2 == 0):
                    coordenadas[-1][1] -= 1
                else:
                    coordenadas[-1][1] += 1

    # Entrar y salir por el mismo punto
    start = [0, 0]
    end = start
    coordenadas.insert(0, start)
    coordenadas.append(end)

    return coordenadas


if __name__ == "__main__":

    n = 10

    # Generacion de picking en posiciones random
    pos_pick = [randint(0, 31) for i in range(0, n)]

    # Obtengo la coordenada del pasillo contiguo a cada uno de los lugares
    # del almacen con objetos.
    coordenadas = map_to_coord(pos_pick)

    print(coordenadas)
    print(distance(coordenadas), "\n")

    best_path = temple_simulado(coordenadas, 200, neighbours_annealing, distance)

    print(best_path[0],"\n",best_path[1])

#
