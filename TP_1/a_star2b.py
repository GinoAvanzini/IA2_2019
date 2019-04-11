import math

STEP = 1


almacen = list(range(32))


map = [  [-1, -1, -1, -1, -1, -1, -1],
         [-1, almacen[0], almacen[1], -1, almacen[16], almacen[17], -1],
         [-1, almacen[2], almacen[3], -1, almacen[18], almacen[19], -1],
         [-1, almacen[4], almacen[5], -1, almacen[20], almacen[21], -1],
         [-1, almacen[6], almacen[7], -1, almacen[22], almacen[23], -1],
         [-1, -1, -1, -1, -1, -1, -1],
         [-1, almacen[8], almacen[9], -1, almacen[24], almacen[25], -1],
         [-1, almacen[10], almacen[11], -1, almacen[26], almacen[27], -1],
         [-1, almacen[12], almacen[13], -1, almacen[28], almacen[29], -1],
         [-1, almacen[14], almacen[15], -1, almacen[30], almacen[31], -1],
         [-1, -1, -1, -1, -1, -1, -1] ]



class Node:
    """
    Clase para crear los nodos objetos del árbol de búsqueda. Se inicializa con un parámetro state, que da la configuración de estado de n dimensiones. El resto de los parámetros son internos a la implementación: costo de camino (gScore), costo heurístico (hScore), costo total (fScore) y nodo padre (cameFrom).
    """
    def __init__(self, state):
        self.fScore = math.inf
        self.gScore = math.inf
        self.hScore = math.inf
        self.cameFrom = None
        self.config = state[:]


# [PARCIALMENTE INDEPENDIENTE DEL PROBLEMA]
def distance(node1, node2):
    """
    Válido solo si se elige como función heurística la distancia en línea recta de un nodo a otro.
    Se recibe los dos nodos a analizar (clase Node), y se calcula la distancia euclidiana (n dimensional) entre las dos propiedades node.config de los nodos. La función devuelve el valor numérico de la distancia.
    """
    sum = 0
    for i in range(0, 2):
        sum += math.pow((node1.config[i] - node2.config[i]), 2)

    return math.sqrt(sum)


# [INDEPENDIENTE DEL PROBLEMA]
def reconstruct_path(ans):
    """
    Función interna de la implementación del algoritmo. Recibe como parámetro un nodo clase Node, objetivo del problema; y la función vuelve hacia atrás con la propiedad node.cameFrom, construyendo la respuesta.
    La función devuelve la solución del problema: una lista con la secuencia de nodos.
    """

    total_path = [ans]

    while (ans.cameFrom != None):
        total_path.append(ans.cameFrom)
        ans = ans.cameFrom

    return total_path


# [INDEPENDIENTE DEL PROBLEMA]
def check_list(node, list):
    """
    Función interna de implementación del algoritmo. Recibe un nodo de clase Node (node) y una lista (list). Verifica la presencia de un nodo con igual configuración (node.config) en la lista.
    En específico, las listas que se utilizan son openSet y closedSet.
    La función devuelve True si la configuración del nodo se encuentra en la lista, y False en caso contrario.
    """
    ans = False
    for item in list:
        if (node.config == item.config):
            ans = True
    return ans


# Función principal de algoritmo A*
# [INDEPENDIENTE DEL PROBLEMA]
def a_star(start, goal, generate_neighbours, heuristica=distance):
    """
    Función principal de algoritmo A estrella. Recibe como parámetros el nodo
    inicial (start) y objetivo del problema (goal), clase Node ,con toda su información; y una función con el modo en que se generarán los vecinos (modelado del problema).
    La función devuelve como primer parámetro la lista de nodos con la solución, el camino encontrado; y el segundo parámetro si encontró (True) o no (False) solución.
    """

    closedSet = []

    openSet = [start]

    start.gScore = 0
    start.hScore = heuristica(start, goal)
    start.fScore = start.hScore

    while (len(openSet) != 0):

        current = openSet[0]

        for i in range(1, len(openSet)):
            if (openSet[i].fScore < current.fScore):
                current = openSet[i]

        if (current.config == goal.config):
            #print("TERMINO")
            return reconstruct_path(current), True

        openSet.remove(current)
        closedSet.append(current)

        # Dependiente del modelo del problema
        neighbours = generate_neighbours(current)

        for vecino in neighbours:

            if check_list(vecino, closedSet):
                continue

            # Si no está en el openSet, lo agrego
            if not check_list(vecino, openSet):
                openSet.append(vecino)
                vecino.cameFrom = current
                vecino.gScore = current.gScore + STEP
                vecino.hScore = heuristica(vecino, goal)
                vecino.fScore = vecino.fScore + vecino.gScore
            else: # Está en el openSet
                tentative_gScore = current.gScore + STEP
                for i in openSet:
                    if (i.config == vecino.config):
                        if (tentative_gScore < i.gScore):
                            i.cameFrom = current # Cambio el padre
                            i.gScore = tentative_gScore # y uso el nuevo g
                            i.fScore = i.gScore + i.hScore
    print("NO SOL")
    return None, False # No se encontró solución


#-------------------------------------------------------------------------------
#   MODELADO DEL PROBLEMA
#-------------------------------------------------------------------------------

# [DEPENDIENTE DEL PROBLEMA]
def vecinos(node):

    neighbours = []

    for i in range(0, 2):

        st = node.config[:]

        st[i] += 1
        if verify_position(st):
            neighbours.append(Node(st))

        st[i] -= 2
        if verify_position(st):
            neighbours.append(Node(st))

    return neighbours


# Verifica si la coordenada corresponde a un punto válido del espacio y no
# es un obstáculo (almacén)
def verify_position(position):

    if (position[0] < 0 or position[0] > 10) :
        return False
    if (position[1] < 0 or position[1] > 6):
        return False

    if (map[position[0]][position[1]] != -1):
        return False

    return True # Coordenada válida


# EJECUCIÓN
if __name__ == "__main__":

    initial_state = [1, 0]

    end_state = [2, 2]

    start = Node(initial_state)
    goal = Node(end_state)

    # Devuelve en una tupla la list con el path y si fue exitoso o no
    ans = a_star(start, goal, vecinos)

    if ans[1]:
        for node in ans[0]:
            print(node.config)
        print(len(ans[0]))
    else:
        print("Error")
