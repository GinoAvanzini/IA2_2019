from random import randint, choices
from numpy.random import choice
from progressBar import printProgressBar

from simulated_annealing import temple_simulado, map_to_coord, neighbours_annealing, distance

N_PEDIDO = 5

N_POB = 5
MAX_LENGHT = 31
T_0 = 50
MAX_GEN = 5

MUT_PROB = 30


# [INDEPENDIENTE DEL PROBLEMA]
def cross_points(dim):
    """
    Función interna de la implementación del algoritmo genético. Recibe la dimensión del individuo (cantidad de componentes) y devuelve dos índices aleatorios ordenados de menor a mayor.
    """

    c1 = randint(1, dim-2)
    c2 = randint(1, dim-2)

    while (c2 == c1): # Verificación para que sean distintos los puntos de cruce
        c2 = randint(1, dim-2)

    if (c2 < c1): # Ordenar los puntos de cruce de menor a mayor
        aux = c1
        c1 = c2
        c2 = aux

    return c1, c2


# [INDEPENDIENTE DEL PROBLEMA]
def crossover(ind1, ind2):
    """
    Función de crossover entre individuos. Recibe las lista del estado de cada indiviuo. Crossover por *cruce de orden*.
    """

    dim = len(ind1)

    c1, c2 = cross_points(dim)

    # Construcción del individuo
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


# [INDEPENDIENTE DEL PROBLEMA]
def mutacion(ind):
    """
    Función de mutación de individuos. Recibe las lista del estado del indiviuo. Mutación por *inserción*.
    """

    dim = len(ind)

    c1, c2 = cross_points(dim)

    aux = ind[c2]
    ind.remove(ind[c2])
    ind.insert(c1+1, aux)

    return ind


# [INDEPENDIENTE DEL PROBLEMA]
def genetic(pob, conjunto):

    count = 0
    printProgressBar(0, MAX_GEN)
    while (count < MAX_GEN):

        # Cálculo de fitness de cada individuo de la población
        fit = []
        total_fit = 0

        for ind in pob:
            value = fitness(ind, conjunto)
            fit.append(value)
            total_fit += value

            weight = []

        for item in fit:
            weight.append(1 - (item / total_fit))

        new_pob = []
        while (len(new_pob) < N_POB):

            # Selección de padres por peso de fitness: https://en.wikipedia.org/wiki/Fitness_proportionate_selection
            [ind1, ind2] = choices(population=pob, k=2, weights=weight)

            s1, s2 = crossover(ind1, ind2)


            if (randint(0, 100) < MUT_PROB):
                s1 = mutacion(s1)

            if (randint(0, 100) < MUT_PROB):
                s2 = mutacion(s1)

            new_pob.append(s1)
            new_pob.append(s2)

        pob = new_pob

        count += 1
        printProgressBar(count, MAX_GEN)

    # Selección del mejor de la población
    fit = []

    for ind in pob:
        value = fitness(ind, conjunto)
        fit.append(value)

    max_index = 0
    for i in range(0, len(pob)):
        if (fit[i] < fit[max_index]):
            max_index = i

    return pob[max_index]


#-------------------------------------------------------------------------------
#   MODELADO DEL PROBLEMA
#-------------------------------------------------------------------------------

# [DEPENDIENTE DEL PROBLEMA]
def fitness(ind, conjunto):
    """
    Función de fitness. Recibe como parámetro el estado y devuelve el valor de fitness absoluto.
    Depende del problema, en este caso lo da el algoritmo de recocido simulado.
    """

    for orden_prod in conjunto:
        orden_estant = []

        for prod in orden_prod:
            orden_estant.append(ind.index(prod))

        path, cost = temple_simulado(map_to_coord(orden_estant), T_0, neighbours_annealing, distance)

    return cost


# [DEPENDIENTE DEL PROBLEMA]
def generate_ind():
    """
    Función para generar un individuo de forma aleatoria para incorporar a la población inicial. Devuelve el individuo, en este caso, una lista de números que corresponden a la ubicación de cada producto.
    """

    individuo = []
    aux = list(range(0, MAX_LENGHT))
    for i in range(0, MAX_LENGHT):
        item = choice(aux)
        aux.remove(item)
        individuo.append(item)

    return individuo


if __name__ == "__main__":

    # Generar un conjunto de órdenes
    # conjunto = []
    # for i in range(0, N_PEDIDO):
    #     dim = randint(2, MAX_LENGHT-1)
    #     aux = []
    #     for j in range(0, dim):
    #         aux.append(randint(0, MAX_LENGHT-1))
    #     conjunto.append(aux)
    #     print(aux)

    conjunto = []
    for i in range(0, 10):
        conjunto.append(list(range(0, 30)))
        print(conjunto[i])

    start = []
    for i in range(0, N_POB):
        start.append(generate_ind())

    best = genetic(start, conjunto)
    print(best)
