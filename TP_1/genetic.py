from random import randint
from numpy.random import choice

from simulated_annealing import temple_simulado, map_to_coord, neighbours_annealing, distance

N_POB = 20
MAX_LENGHT = 31
T_0 = 300


# [INDEPENDIENTE DEL PROBLEMA]
def crossover(ind1, ind2):
    """
    Función de crossover entre individuos. Recibe las lista del estado de cada indiviuo y el modo en que se desea realizar el crossover:
    Cruce de orden.
    """

    dim = len(ind1)

    c1 = randint(1, dim-2)
    c2 = randint(1, dim-2)

    while (c2 == c1): # Verificación para que sean distintos los puntos de cruce
        c2 = randint(1, dim-2)

    if (c2 < c1): # Ordenar los puntos de cruce de menor a mayor
        aux = c1
        c1 = c2
        c2 = aux

    ans1 = [-1] * c1 + ind2[c1:c2+1] + [-1] * (dim - c2 - 1)
    ans2 = [-1] * c1 + ind1[c1:c2+1] + [-1] * (dim - c2 - 1)

    j = -dim+c2+1
    n = j
    for i in range(0, dim):

        if (not (ind1[i] in ans1)):
            ans1[j] = ind1[i]
            j += 1

        if (not (ind2[i] in ans2)):
            ans2[n] = ind2[i]
            n += 1

    return ans1, ans2


def genetic(init):
    pass


# [DEPENDIENTE DEL PROBLEMA]
def fitness(ind):
    """
    Función de fitness. Recibe como parámetro el estado y devuelve el valor de fitness absoluto.
    Depende del problema, en este caso lo da el algoritmo de recocido simulado.
    """
    path, cost = temple_simulado(map_to_coord(ind), T_0, neighbours_annealing, distance)
    return cost/len(ind)


def generate_ind():
    individuo = {}
    aux = list(range(0, MAX_LENGHT))
    for i in range(0, MAX_LENGHT):
        item = choice(aux)
        aux.remove(item)
        individuo[i] = item

    return individuo


if __name__ == "__main__":
    start = []
    for i in range(0, N_POB):
        start.append(generate_ind())
        # print(start[i])

    print(start[0].values())
    print(start[1].values())
    ans1, ans2 = crossover(list(start[0].values()), list(start[1].values()))
    print(ans1, fitness(list(ans1)))
    print(ans2, fitness(list(ans2)))
