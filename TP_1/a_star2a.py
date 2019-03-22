from a_star2b import Node, STEP, a_star
import random

GDL = 6
TOP = 80
STEP = 10
wall = None

# MODELADO DEL problema
# Generación de vecinos
def generate_neighbours(node):
    """
    Un trabajo posterior para poder disminuir el tiempo de ejecución del algoritmo, es podar el árbol en profundidad generando mayor cantidad de vecinos (mayor cantidad de combinaciones posibles).

    Teoría: La complejidad del algoritmo A* es O(b^d) siendo b la cantidad de estados vecinos y d el factor de ramificación o profundidad.
    """

    neighbours = []

    for i in range(0, GDL):

        st = node.config[:]

        # print(node.config)

        if (st[i] == 0):
            st[i] += STEP
            neighbours.append(Node(st))

        elif (st[i] == TOP):
            st[i] -= STEP
            neighbours.append(Node(st))

        else:
            st[i] += STEP
            neighbours.append(Node(st))

            st[i] -= 2 * STEP
            neighbours.append(Node(st))

    node_error = []

    for node in neighbours:
        for obstaculo in wall:
            flag = True
            for i in range(0, GDL):
                if (node.config[i] < obstaculo[i][0] or obstaculo[i][1] < node.config[i]):
                    flag = False

            if (flag):
                # neighbours.remove(node)
                node_error.append(node)
    for node in node_error:
        if (node in neighbours):
            neighbours.remove(node)

    return neighbours


# Generación aleatoria de obstaculos
def obstaculos():
    wall = []
    for i in range(0, random.randint(1, 10)):
        aux = []
        for j in range(0, GDL):
            comp1 = random.randrange(0, TOP, STEP)
            comp2 = random.randrange(0, TOP, STEP)
            if (comp1 < comp2):
                aux.append([comp1, comp2])
            else:
                aux.append([comp2, comp1])
        wall.append(aux)
        print(wall[i])

    # wall.append([[0,50], [10,20]])
    # wall.append([[0,50], [0,50]])

    return wall

# EJECUCIÓN
if __name__ == "__main__":

    initial_state = [0, 0, 0, 0, 0, 0]
    end_state = [TOP, TOP, TOP, TOP, TOP, TOP]

    start = Node(initial_state)
    goal = Node(end_state)

    wall = obstaculos()

    ans = a_star(start, goal, generate_neighbours)

    if ans[1]:
        for node in ans[0]:
            print(node.config)
        print("d = ", len(ans[0]))
    else:
        print("NO SOL")
