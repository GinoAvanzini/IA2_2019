
import csv
import numpy as np
from math import inf

from progressBar import printProgressBar


def ritmo_aprendizaje(t, t_alfa=100, alfa_0=0.7, alfa_f=0.01):
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

    alfa = alfa_0 * (alfa_f / alfa_0)**(t / t_alfa)
    return alfa


def radio_vecindad(t, t_r=100, R_0=100, R_f=1):
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



if __name__ == "__main__":
    
    data_raw = []

    with open('train.csv') as csvDataFile:
        csvReader = csv.reader(csvDataFile)
        for i, row in enumerate(csvReader):
            if (i == 0):
                continue
            label = row[0]
            data_raw.append([label, np.array(row[1:], dtype=float)])

    # NORMALIZACIÓN
    data = []

    for i in range(0, len(data_raw)-1):
        # label = img[0]
        label = data_raw[i+1][0]
        np.delete(data_raw[i][0], 0)
        img_as_float = data_raw[i][1] / 255
        data.append([label, img_as_float])

    # MODELO DE LA RED NEURONAL
    x = data_raw[0][1]
    map_kohonen = np.zeros((100, 100)) # Mapa de neuronas
    W = np.zeros((map_kohonen.shape[0], map_kohonen.shape[1], x.shape[0]))  
    
    # k-fold cross validation
    train = data[:28000]
    test = data[28000:]

    print(len(data), len(train), len(test))

    t = 0
    printProgressBar(t, 25200)
    for [_, x] in train[:25200]:
        minim = inf

        for i in range(map_kohonen.shape[0]):
            for j in range(map_kohonen.shape[1]):
                map_kohonen[i, j] = d_euclidean(x, W[i, j, :])
                if (map_kohonen[i, j] < minim):
                    minim = map_kohonen[i, j]
                    g = [i, j]
        
        for i in range(W.shape[0]):
            for j in range(W.shape[1]):
                W[i, j, :] = update_w(W[i, j, :], x, [i, j], g, t, lvq=1, ritmo_aprendizaje, vecindad)
        
        t += 1
        printProgressBar(t, 25200)
    
    # Inicialización del mapa con algoritmo K-Means
    sample = []
    ctrl = list(range(0, 10))
    for [label, x] in train[:25200]:
        if (label in ctrl):
            ctrl.remove(label)
            sample.append(x)
        if not ctrl:
            break
    
    map_labels = np.zeros((100, 100)) # Mapa de labels

    for x in sample:
        minim = inf
        for i in range(map_kohonen.shape[0]):
            for j in range(map_kohonen.shape[1]):
                aux = d_euclidean(x, W[i, j, :])
                if (aux < minim):
                    minim = aux
                    g = [i, j]