from random import randint
from numpy.random import choice

from simulated_annealing import temple_simulado, map_to_coord, neighbours_annealing, distance

N_POB = 20
MAX_LENGHT = 16
T_0 = 300


# [INDEPENDIENTE DEL PROBLEMA]
def crossover(ind1, ind2):
    """
    Función de crossover entre individuos. Recibe las lista del estado de cada indiviuo y el modo en que se desea realizar el crossover:
    Cruce de orden.
    """
    c1 = randint(1, len(ind1)-2)
    c2 = randint(1, len(ind1)-2)

    while (c2 == c1): # Verificación para que sean distintos los puntos de cruce
        c2 = randint(1, len(ind1)-2)

    if (c2 < c1): # Ordenar los puntos de cruce de menor a mayor
        aux = c1
        c1 = c2
        c2 = aux

    ans1 = [-1] * c1 + ind2[c1:c2] + [-1] * (len(ind1) - c2)
    ans2 = [-1] * c1 + ind1[c1:c2] + [-1] * (len(ind1) - c2)

    for i in range(-c2+1, c1):
        if (ind1[i] in ans1):
            continue
        else:
            ans1[i] = ind1[i]

        if (ind2[i] in ans2):
            continue
        else:
            ans2[i] = ind2[i]

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
    aux = list(range(0, 31))
    for i in range(0, MAX_LENGHT):
        item = choice(aux)
        aux.remove(item)
        individuo[i] = item

    # fit = fitness(individuo)

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
