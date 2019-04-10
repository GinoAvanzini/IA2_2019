
N = 5 # Número de tareas
DLINE = 100 # Tiempo en que se debe finalizar el proceso en minutos
STEP = 5 # Discretización del tiempo

T = {"d0": 40, "d1":5, "d2":15, "d3":10, "d4":30}

def selection(D, assign):
    """
    Selección de variable con heurística *variable más restringida*.
    """
    k_D = list(D.keys())
    k_A = list(assign.keys())

    k = list(set(k_D)^set(k_A))
    mvr = k[0]

    for i in k:
        # if (i in k_A):
        #     continue

        if (len(D[i]) < len(D[mvr])):
            mvr = i

    return mvr


def consistent(var, value, assign, R2):
    flag = True
    for v in assign.keys():
        if ((v, var) in R2[var]):
            if (assign[v] + T[v] > value):
                flag = False
        if ((var, v) in R2[var]):
            if (value + T[var] > assign[v]):
                flag = False
    print(flag)
    return flag


def backtrack(assign, D, R2):

    if (len(assign) == N): # Condición de salida
        print("SOL")
        return assign

    var = selection(D, assign) # Falta selecciónar solo entre las no asignadas [SOLUCIONADO?]

    for i in D[var]:
        if (consistent(var, i, assign, R2)):
            assign[var] = i
            print(assign)
            print("LEVEL")
            ans = backtrack(assign, D, R2)
            if (ans != False):
                return ans
            assign.pop(var)

    print("FALSE")
    return False


class Node:
    def __init__(self):
        self.prev = []
        self.next = []

if __name__ == "__main__":

    D = {}
    for i in T.keys():
        D[i] = list(range(0, DLINE-T[i], STEP))

    assign = {}

    print(selection(D, assign))
    print(T)
    print(D)

    R2 = {
        "d0":[("d0", "d1"), ("d0", "d2")],
        "d1":[("d0", "d1"), ("d1", "d3")],
        "d2":[("d0", "d2"), ("d2", "d4")],
        "d3":[("d1", "d3"), ("d3", "d4")],
        "d4":[("d3", "d4"), ("d2", "d4")]
    }

    print(backtrack(assign, D, R2))
