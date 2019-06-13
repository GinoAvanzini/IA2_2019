import csv
import numpy as np
from math import inf

from matplotlib import pyplot as plt

from progressBar import printProgressBar

def ritmo_aprendizaje(t, t_alfa=20000, alfa_0=0.7, alfa_f=0.01):
    """Obtener el coeficiente de ritmo de aprendizaje dada la iteración actual

    Parameters
    ----------
    t : int
        El número de iteración actual
    t_alfa : int
        El máximo número de iteraciones para llegar a alfa_f. Por defecto 100
    alfa_0 : float
        Ritmo de aprendizaje inicial abs(alfa_0) < 1.
        Por defecto 0.7
    alfa_f : float
        Ritmo de aprendizaje final. Por defecto 0.01

    Returns
    -------
    float
        El ritmo de aprendizaje para la iteración actual t
    """

    if (t > t_alfa):
        return alfa_f

    alfa = alfa_0 * (alfa_f / alfa_0)**(t / t_alfa)
    return alfa


def radio_vecindad(t, t_r=20000, R_0=3, R_f=1):
    """Obtener el radio de vecindad dada la iteración actual

    Parameters
    ----------
    t : int
        El número de iteración actual
    t_r : int
        El máximo número de iteraciones para llegar a R_f. Por defecto 100
    R_0 : int, float
        Radio de vecindad inicial. Por defecto 100
    R_f : int, float
        Radio de vecindad final. Por defecto 1

    Returns
    -------
    float
        El radio de vecindad para la iteración actual t
    """

    if (t > t_r):
        return R_f

    R = R_0 + (R_f - R_0) * t / t_r
    return R


def vecindad(i, g, t, R=radio_vecindad):
    """Función de vecindad escalón dado un determinado radio de vecindad
    Determina si la neurona en cuestión está dentro del radio

    Parameters
    ----------
    i : list
        Posición en el mapa de la neurona ij.
        La lista es de la forma [i, j], siendo i y j enteros
    g : list
        Posición en el mapa de la neurona ganadora para el vector entrada x.
        Esta neurona ganadora es la de vector de pesos sinápticos más cercanos
        al vector x
        La lista es de la forma [i, j], siendo i y j enteros
    t : int
        El número de iteración actual
    R : function
        Función que define el radio de vecindad a utilizar. 
        Por defecto es la función radio_vecindad definida en este archivo

    Returns
    -------
    int
        Se devuelve un 1 si la neurona en cuestión está dentro del radio
        de vecindad; y un 0 en caso contrario
    """

    aux = np.sqrt((i[0] - g[0])**2 + (i[1] - g[1])**2)
    if (aux > R(t)):
        return 0
    else:
        return 1


def d_euclidean(x, w):
    """Obtener la distancia euclideana entre los dos vectores x y w

    Parameters
    ----------
    x : numpy array shape (dim,)
        Primer vector unidimensional
    w : numpy array shape (dim,)
        Segundo vector unidimensional

    Returns
    -------
    float
        La distancia euclideana entre ambos vectores
    """

    sum = 0
    for i in range(x.shape[0]):
        sum += (x[i] - w[i])**2
    return sum


def update_w(w, x, i, g, t, lvq=1, ritmo_aprendizaje=ritmo_aprendizaje, vecindad=vecindad):
    """Actualización de pesos sinápticos W_ij dado un vector de entrada x

    Parameters
    ----------
    w : numpy array shape (dim,)
        Vector de pesos sinápticos W_ij
    x : numpy array shape (dim,)
        Vector de entrada x
    i : list
        Posición en el mapa de la neurona ij.
        La lista es de la forma [i, j], siendo i y j enteros
    g : list
        Posición en el mapa de la neurona ganadora para el vector entrada x.
        Esta neurona ganadora es la de vector de pesos sinápticos más cercanos
        al vector x
        La lista es de la forma [i, j], siendo i y j enteros
    t : int
        El número de iteración actual
    lvq : int
        Coeficiente entero que puede ser -1 o 1. Puede utilizarse en caso de
        utilizar LVQ (Learning Vector Quantization), e incrementará o 
        decrementará el vector de pesos sinápticos segun sea el caso
    ritmo_aprendizaje : function
        Función que define el ritmo de aprendizaje a utilizar
    vecindad : function
        Función que define la función de vecindad a utilizar

    Returns
    -------
    numpy array shape (dim,)
        Vector de pesos sinápticos W_ij actualizado
    """
    
    w_new = w + lvq * ritmo_aprendizaje(t) * vecindad(i, g, t) * (x - w) 
    # CUIDADO: Ver si la diferencia puede dar negativo, 
    # si es así, calcular valor absoluto. Se utiliza distancia euclideana,
    # por lo que no debería pasar.
    return w_new


def winner(W, x, similarity=d_euclidean):

    minim = inf
    for i in range(W.shape[0]):
        for j in range(W.shape[1]):
            aux = similarity(x, W[i, j, :])
            if (aux < minim):
                minim = aux
                g = [i, j]
    return g


def get_data(data_file):
    data_raw = []

    with open(data_file) as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for i, row in enumerate(csvReader):
            if (i == 0):
                continue
            # if (i > 100):
            #     break
            label = row[0]
            data_raw.append([label, np.array(row[1:], dtype=float)])

    # NORMALIZACIÓN
    data = []

    for i in range(0, len(data_raw)-1):
        label = data_raw[i+1][0]
        # label = data_raw[i][0]
        np.delete(data_raw[i][0], 0)
        img_as_float = data_raw[i][1] / 255
        data.append([label, img_as_float])

    return data


def kmeans(map_kohonen, W, sample):

    # Asignación de centroides iniciales
    means = []
    for [label, x] in sample:
        g = winner(W, x)
        means.append([label, g])

    # Actualización de centroides
    iter = 0
    printProgressBar(iter, 50)
    while (iter < 15):
        minim = inf
        for i in range(W.shape[0]):
            for j in range(W.shape[1]):
                for [label, mean] in means:
                    aux = d_euclidean(W[mean[0], mean[1], :], W[i, j, :])
                    if (aux < minim):
                        minim = aux
                        map_kohonen[i, j] = label

        sum = np.zeros((10, W.shape[2]))
        dim = np.zeros((10,))
        for i in range(map_kohonen.shape[0]):
            for j in range(map_kohonen.shape[1]):
                label = int(map_kohonen[i, j])
                sum[label, :] += W[i, j, :]
                dim[label] += 1

        means = []
        for [label, mean] in means:
            x = sum[label, :] / dim[label]
            means.append(winner(W, x))

        iter += 1
        printProgressBar(iter, 50)
    
    return map_kohonen


def printMap(map_kohonen):
    """Plotear el mapa de kohonen marcando las diferentes clases

    Parameters
    ----------
    map_kohonen : numpy array shape(i, j, k)
        Mapa de kohonen a plotear
    """
    
    map_data = {}
    
    for i in range(0, 10):
        map_data[i] = []
    
    for i in range(map_kohonen.shape[0]):
        for j in range(map_kohonen.shape[1]):
            if (map_kohonen[i, j] < 0):
                continue
            index = int(map_kohonen[i, j])
            map_data[index].append([i, j])
    
    for i in map_data:
        for arr in map_data[i]:
            plt.plot(arr[0], arr[1], label=str(i))
    
    return


if __name__ == "__main__":

    data = get_data('train.csv')

    map_kohonen = np.zeros((20, 20)) # Mapa de neuronas
    for i in range(map_kohonen.shape[0]):
        for j in range(map_kohonen.shape[1]):
            map_kohonen[i, j] = -1

    W = np.zeros((map_kohonen.shape[0], map_kohonen.shape[1], data[0][1].shape[0]))

    mu = 0
    sigma = 1

    for i in range(W.shape[0]):
        for j in range(W.shape[1]):
            W[i, j, :] = abs(0.01 * np.random.normal(mu, sigma, W.shape[2]))

    MAX = int(0.66 * len(data))
    train = data[:MAX]
    test = data[MAX:]

    print(len(data), len(train), len(test))

    t = 0
    printProgressBar(t, len(train))
    for [_, x] in train:

        g = winner(W, x)

        for i in range(W.shape[0]):
            for j in range(W.shape[1]):
                W[i, j, :] = update_w(W[i, j, :], x, [i, j], g, t, lvq=1)

        t += 1
        printProgressBar(t, len(train))


    sample = []
    ctrl = list(range(0, 10))
    for [label, x] in train:
        label = int(label)
        if (label in ctrl):
            ctrl.remove(label)
            sample.append([label, x])
        if not ctrl:
            break


    # def r_aux(a):
    #     return 2

    # for [label, x] in sample:
    #     g = winner(W, x)
    #     for i in range(W.shape[0]):
    #         for j in range(W.shape[1]):
    #             if (vecindad([i, j], g, 0, R=r_aux)):
    #                 map_kohonen[i, j] = int(label)

    map_kohonen = kmeans(map_kohonen, W, sample)


    t = 0
    printProgressBar(t, len(train))

    for [label, x] in train:

        label = int(label)
        [i, j] = winner(W, x)

        if (map_kohonen[i, j] == label):
            lvq_c = 1
        else:
            lvq_c = -1

        W[i, j, :] +=  W[i, j, :] + lvq_c * 0.01 * (x - W[i, j, :])

        t += 1
        printProgressBar(t, len(train))

    print(map_kohonen)

    t = 0
    printProgressBar(t, len(test))

    for [label, x] in test:

        label = int(label)
        [i, j] = winner(W, x)

        if (map_kohonen[i, j] == label):
            t +=1

        printProgressBar(t, len(test))

    print(t)

    len(test)

