from random import randint, choices
from numpy.random import choice
from progressBar import printProgressBar

from simulated_annealing import temple_simulado, map_to_coord, neighbours_annealing, distance

# N_PEDIDO = 1 # Cantidad de pedidos para los que se desea optimizar el layout del almacen

N_POB = 10 # Cantidad de individuos en la población
MAX_LENGHT = 32 # Cantidad de estanterías
T_0 = 200 # Temperatura inicial a la que inicia el algoritmo de temple simulado
MAX_GEN = 50 # Máxima cantidad de iteraciones a la que corta el algoritmo genético

MUT_PROB = 10 # Probabilidad de mutar de un individuo, de 0 a 100%

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
    Función de crossover entre individuos. Recibe las lista del estado de cada indiviuo. Crossover por *cruce de orden*. Devuelve los dos individuos "hijos" generados.
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
    Función de mutación de individuos. Recibe las lista del estado del indiviuo. Mutación por *inserción*. Devuelve al individuo mutado.
    """

    dim = len(ind)

    c1, c2 = cross_points(dim)

    aux = ind[c2]
    ind.remove(ind[c2])
    ind.insert(c1+1, aux)

    return ind


# [INDEPENDIENTE DEL PROBLEMA]
def seleccion(pob, weight):
    """
    Función para la selección de padres dentro de la población. Recibe una lista con los individuos de la población, y un segundo parámetro con una lista de los "pesos" (o fitness relativo) de los respectivos individuos.
    La forma de elección es estilo roulette wheel selection, donde los individuos tienen mayor probabilidad de ser elegidos (distribución de probabilidad uniforme) cuanto mayor sea su peso.
    La función devuelve los dos individuos elegidos.
    """
    flag = True
    while (flag):
        [ind1, ind2] = choices(population=pob, k=2, weights=weight)
        if (ind1 != ind2):
            flag = False

    return [ind1, ind2]


#-------------------------------------------------------------------------------
#   MODELADO DEL PROBLEMA
#-------------------------------------------------------------------------------

# [PARCIALMENTE DEPENDIENTE DEL PROBLEMA]
def genetic(pob, conjunto, hist=False):
    """
    Función principal de la implementación del algoritmo genético. Recibe como parámetros la población inicial y una variable "conjunto", exclusiva del modelado, que es el conjunto de pedidos para los que se desea optimizar el layout del almacen.
    La función devuelve el mejor indiviuo luego de MAX_GEN generaciones.
    """

    history = []

    aux_fit = fitness(pob[0], conjunto)
    best = [pob[0], aux_fit]

    count = 0
    printProgressBar(0, MAX_GEN)
    while (count < MAX_GEN):

        # Cálculo de fitness de cada individuo de la población. La lista fit tendrá el valor absoluto de fitness, y la lista weight el valor relativo de fitness al resto de la población.
        fit = []
        # total_fit = 0
        max_fit = 0
        for ind in pob:
            value = fitness(ind, conjunto)
            fit.append(value)
            # total_fit += value
            if (max_fit < value):
                max_fit = value

        total_fit = 0
        for item in fit:
            total_fit += (max_fit - item)

        weight = []
        for item in fit:
            # print(item / total_fit)
            weight.append((max_fit - item)/total_fit)

        # Evolución de la población
        new_pob = []
        while (len(new_pob) < N_POB):

            # Selección de padres por peso de fitness: https://en.wikipedia.org/wiki/Fitness_proportionate_selection
            [ind1, ind2] = seleccion(pob, weight)

            s1, s2 = crossover(ind1, ind2) # Crossover

            # Mutación
            if (randint(0, 100) < MUT_PROB):
                s1 = mutacion(s1)

            if (randint(0, 100) < MUT_PROB):
                s2 = mutacion(s1)

            new_pob.append(s1)
            new_pob.append(s2)

        pob = new_pob # Actualización de la población

        count += 1
        printProgressBar(count, MAX_GEN)

        # Selección del mejor de la población
        # Esto podría realizarse para cada generación, y no solo quedarse con el último mejor. SImilar a lo que se hizo en el temple simulado.
        fit = []

        for ind in pob:
            value = fitness(ind, conjunto)
            fit.append(value)

        max_index = 0
        for i in range(0, len(pob)):
            if (fit[i] < fit[max_index]):
                max_index = i

        history.append(fit[max_index])
        
        # print(pob[max_index])
        if (fit[max_index] < best[1]):
            best = [pob[max_index], fit[max_index]]

    if hist:
        return best, history
    else:
        return best
    


# [DEPENDIENTE DEL PROBLEMA]
def fitness(ind, conjunto):
    """
    Función de fitness. Recibe como parámetro el individuo cuyo fitness se desea calcular, y un segundo parámetro "conjunto" que corresponde al conjunto de ordenes para las cuales se desea optimizar el layout del almacen. La función devuelve el valor de fitness absoluto.
    Depende del modelo del problema, en este caso lo da el algoritmo de recocido simulado.
    """

    for orden_prod in conjunto:
        orden_estant = []
        sum = 0
        for prod in orden_prod:
            orden_estant.append(ind.index(prod))

        _, cost = temple_simulado(map_to_coord(orden_estant), T_0, neighbours_annealing, distance)
        sum += cost

    return sum / len(conjunto)


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

    conjunto = []

    prob = []
    
    estant = [i for i in range(0, MAX_LENGHT)]
    
    for i in range(0, 25):
        prob.append(0.1)
    
    for i in range(25, MAX_LENGHT):
        prob.append(0.5)
    
    for i in range(0, 8):
        conjunto.append(choices(population=estant, k=randint(3, 7), weights=prob))

    # conjunto = [[20,21,22,30,27,31,27,31,18,23]]

    start = []
    for i in range(0, N_POB):
        start.append(generate_ind())

    best = genetic(start, conjunto)
    print(best)
