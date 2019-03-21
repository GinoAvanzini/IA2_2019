
from a_star2b import a_star, map, Node, vecinos
from random import random, randint

from math import exp

def update_T(temperature):

    return temperature - 0.5


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


def temple_simulado(productos):

    current = productos

    temp = 50

    while(1):

        if (temp == 0): return current

        next = neighbours_annealing(current)

        delta = energy(next) - energy(current)

        if (delta < 0):
            current = next
        else: # delta is positive -> worse path
            prob = exp(-delta/temp)
            # print(prob)
            if (random() < prob):
                current = next

        temp = update_T(temp)


if __name__ == "__main__":

    n = 5
    pos_pick = []
    coordenadas = []

    # Generacion de picking en posiciones random
    for i in range(0, n):
        pos_pick.append(randint(0, 31))
        # a = pos_pick[-1]
        # almacen[a] = a

    # Obtengo la coordenada del pasillo contiguo a cada uno de los lugares
    # del almacen con objetos.
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

    print(coordenadas)
    print(energy(coordenadas), "\n")

    best_path = temple_simulado(coordenadas)

    print(best_path)
    print(energy(best_path))




#
