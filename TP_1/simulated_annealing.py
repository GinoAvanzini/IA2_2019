
from a_star2b import a_star, map, Node, vecinos
from random import random, randint

from math import exp

def update_T(temperature):

    return temperature - 1


def neighbours_annealing(current):

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


def energy(path):

    distance = 0

    for i in range(1, len(path)):
        distance += len(a_star(Node(path[i]), Node(path[i - 1]), vecinos)[0]) - 1

    return distance


def temple_simulado(productos, t_inicial):

    current = productos

    temp = t_inicial

    historic_best = [current, energy(current)]

    while(1):

        if (temp == 0): return historic_best

        next = neighbours_annealing(current)

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

def map_to_coord(pos_pick):
    for i in pos_pick:
        for fila in range(0, len(map)):
            if i in map[fila]:
                coordenadas.append([fila, map[fila].index(i)])

                if (map[coordenadas[-1][0]][coordenadas[-1][1]] % 2 == 0):
                    coordenadas[-1][1] -= 1
                else:
                    coordenadas[-1][1] += 1

    return coordenadas

if __name__ == "__main__":

    n = 10
    pos_pick = []
    coordenadas = []

    # Generacion de picking en posiciones random
    for i in range(0, n):
        pos_pick.append(randint(0, 31))
        # a = pos_pick[-1]
        # almacen[a] = a

    # Obtengo la coordenada del pasillo contiguo a cada uno de los lugares
    # del almacen con objetos.
    coordenadas = map_to_coord(pos_pick)

    # Entrar y salir por el mismo punto
    start = [0, 0]
    end = start
    coordenadas.insert(0, start)
    coordenadas.append(end)

    print(coordenadas)
    print(energy(coordenadas), "\n")

    best_path = temple_simulado(coordenadas, 200)

    print(best_path[0],"\n",best_path[1])






#
