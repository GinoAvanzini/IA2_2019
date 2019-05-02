from random import choice

N = 5 # Número de tareas
DLINE = 150 # Tiempo en que se debe finalizar el proceso en minutos
STEP = 5 # Discretización del tiempo

T = {"d0": 40, "d1":5, "d2":15, "d3":10, "d4":30}

def selection(D, assign):
    """
    Selección de variable con heurística *variable más restringida*. La función recibe el diccionario de dominio de las distintas variables "D" y un diccionario con las variables ya asignadas "assign".
    La función devuelve el key de diccionario asociado a la variable elegida.
    """
    k_D = list(D.keys())
    k_A = list(assign.keys())

    k = list(set(k_D)^set(k_A))

    return choice(k)


def consistent(var, value, assign, R2, M):
    """
    Función para comprobar la consistencia de una posible asignación de valor a una variable. Dentro de esta función se verifica que la asignación respete todas las restricciones posibles con las variables ya asignadas, devolviendo verdadero; o no haya consistencia en la asignación, devolviendo falso.
    Recibe como parámetros la variable a asignar "var", el valor a asignar a dicha variable "value", el diccionario con todas las asignaciones ya realizadas "assign" y un diccionario con las restricciones asociadas a cada variable "R2".
    """

    for v in assign.keys():
        if ((v, var) in R2[var]):
            if (assign[v] + T[v] > value):
                return False

        if ((var, v) in R2[var]):
            if (value + T[var] > assign[v]):
                return False

        for m in M[var]:
            cond = (value < assign[v] + T[v]) and (assign[v] <= value)
            if ((m in  M[v]) and cond):
                return False

    return True


def backtrack(assign, D, R2, M):
    """
    Función principal del algoritmo. Es una búsqueda hacia atrás o backtracking-search, por lo tanto, basicamente es un algoritmo de búsqueda primero en profundidad.
    Recibe como parámetros un diccionario con las asignaciones ya realizadas "assign" (en el primer llamado es un diccionario vacío pero luego se realiza recursión), un diccionario con el dominio de las variables "D" y un diccionario con las restricciones asociadas a las variables "R2".
    Se devuelve la solución del problema si la hay, o un falso si no existe solución.
    """
    if (len(assign) == N): # Condición de salida
        return assign

    var = selection(D, assign) # Falta selecciónar solo entre las no asignadas [SOLUCIONADO?]

    for i in D[var]:
        if (consistent(var, i, assign, R2, M)):
            assign[var] = i
            ans = backtrack(assign, D, R2, M)
            if (ans != False):
                return ans
            assign.pop(var)
    return False


if __name__ == "__main__":

    D = {}
    for i in T.keys():
        D[i] = list(range(0, DLINE-T[i], STEP))

    assign = {}
    
    print(selection(D, assign))
    print(T)
    print(D)

    # Restricciones de precedencia
    R2 = {
        "d0":[("d0", "d1"), ("d0", "d2")],
        "d1":[("d0", "d1"), ("d1", "d3")],
        "d2":[("d0", "d2"), ("d2", "d4")],
        "d3":[("d1", "d3"), ("d3", "d4")],
        "d4":[("d3", "d4"), ("d2", "d4")]
    }

    # Restricción de recursos
    M = {
        "d0":["m0", "m3"],
        "d1":["m0", "m4"],
        "d2":["m0"],
        "d3":["m0", "m2", "m3"],
        "d4":["m0", "m4"]
    }

    print(backtrack(assign, D, R2, M))
