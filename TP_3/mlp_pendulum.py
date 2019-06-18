import pandas as pd
import numpy as np
from math import sin, cos
from matplotlib import pyplot as plt

from mlp_housing import salida_red, backprop, calc_rendimiento


# Función de actualización del modelo del péndulo invertido 
# Sacada de ../TP_2/fuzzy logic.py
def update(x, dt, F):

    x_t = x

    num = g * sin(x[0]) + cos(x[0]) * (- F - m * l * pow(x[1], 2) * sin(x[0])) / (M + m)
    den = l * (4/3 - m * pow(cos(x[0]), 2) / (M + m))

    x_t[2] = num / den

    x_t[1] = x[1] + x[2]*dt
    x_t[0] = x[0] + x[1]*dt + x[2]*pow(dt, 2)/2

    return x_t


if __name__ == "__main__":

    # ------------------
    # Variables 
    NEURONAS_ENTRADA = 2
    NEURONAS_CAPA_OCULTA = 15
    NEURONAS_SALIDA = 1

    EPS = 0.025
    EPOCHS = 30

    INDEX_TRAIN = 6000
    INDEX_VALID = 8000
    INDEX_TEST = 10000      # Total de ejemplos en el dataset
    # ------------------

    data = pd.read_csv("./datasets/pendulum.csv")

    t = np.asarray(data['Fuerza'], dtype=np.float64)
    t.shape = (NEURONAS_SALIDA, t.size)

    # En data solo guardo las entradas
    data = data.drop(data.columns[2], axis=1)
    data = np.asarray(data)
    
    # Normalización
    media = []
    std_dev = []

    for i in range(0, data[0, :].size):
        media.append(np.mean(data[0:INDEX_TRAIN, i]))
        data[:, i] = data[:, i] - media[i]
        std_dev.append(np.std(data[0:INDEX_TRAIN, i]))
        data[:, i] = data[:, i]/std_dev[i]

    print("media", media)
    print("std_dev", std_dev)

    media_t = []
    std_dev_t = []
    for j in range(0, t[:, 0].size):
        media_t.append(np.mean(t[j, 0:INDEX_TRAIN]))
        t[j, :] = t[j, :] - media_t[j]
        std_dev_t.append(np.std(t[j, 0:INDEX_TRAIN]))
        t[j, :] = t[j, :]/std_dev_t[j]

    print("media_t", media_t)
    print("std_dev_t", std_dev_t)

    x = np.zeros((1, NEURONAS_ENTRADA), dtype=np.float64)
    y = np.zeros((1, NEURONAS_CAPA_OCULTA), dtype=np.float64)
    z = np.zeros((1, NEURONAS_SALIDA), dtype=np.float64)

    # Inicialización de pesos y sesgos
    Wji = np.asarray([[(2*np.random.random_sample() - 1) \
        for i in range(NEURONAS_CAPA_OCULTA)] \
            for j in range(NEURONAS_ENTRADA)], dtype=np.float64)

    theta_j = 0.01*np.ones((1, NEURONAS_CAPA_OCULTA), dtype=np.float64)
    theta_j.shape = (1, theta_j.size)


    Wkj = np.asarray([[(2*np.random.random_sample() - 1) \
        for i in range(NEURONAS_SALIDA)] \
            for j in range(NEURONAS_CAPA_OCULTA)], dtype=np.float64)

    theta_k = 0.01*np.ones((1, NEURONAS_SALIDA), dtype=np.float64)
    theta_k.shape = (1, theta_k.size)


    error_training = []
    error_validation = []

    # ----- TRAINING -----
    for epoch in range(0, EPOCHS):
        k = 0

        t_esperado = []
        t_obtenido = []

        print("EPOCH: ", epoch)
        for j in range(0, INDEX_TRAIN):

            k += 1            
            xbc = data[j, :]
            xbc.shape = (1, NEURONAS_ENTRADA)

            y, ex = salida_red(Wji, Wkj, theta_j, theta_k, xbc, y, z)
            t_obtenido.append(ex[0, 0])
            t_esperado.append(t[0, j])
            backprop(Wji, Wkj, theta_j, theta_k, xbc, y, z, t[0, j], EPS)            

        # ----- error -----
        error_training.append(calc_rendimiento(np.array(t_obtenido), np.array(t_esperado), k))
        print("error training", error_training[-1])

        k = 0
        t_esperado = []
        t_obtenido = []

        # ----- VALIDATION -----
        for j in range(INDEX_TRAIN + 1 , INDEX_VALID):

            k += 1
            xbc = data[j, :]
            xbc.shape = (1, NEURONAS_ENTRADA)

            y, ex = salida_red(Wji, Wkj, theta_j, theta_k, xbc, y, z)
            t_obtenido.append(ex[0, 0])
            t_esperado.append(t[0, j])
            backprop(Wji, Wkj, theta_j, theta_k, xbc, y, z, t[0, j], EPS)            

        # ----- error -----
        error_validation.append(calc_rendimiento(np.array(t_obtenido), np.array(t_esperado), k))
        print("error validation", error_validation[-1])
        
        if (epoch > 1) and (np.abs((error_validation[-1] - error_validation[-2]))/error_validation[-2] < 0.005):
            EPOCHS = epoch + 1
            break;


    plt.plot(range(EPOCHS), error_training, label='Error de training')
    plt.plot(range(EPOCHS), error_validation, label='Error de validation')
    plt.xlabel('Epochs')
    plt.ylabel('Error promedio en desviaciones estándar')
    
    plt.legend()

    # ----- TEST -----
    t_esperado = []
    t_obtenido = []
    
    k = 0
    print("\nTEST: ")
    for j in range(INDEX_VALID + 1, INDEX_TEST):

        k += 1
        xbc = data[j, :]
        xbc.shape = (1, NEURONAS_ENTRADA)

        y, ex = salida_red(Wji, Wkj, theta_j, theta_k, xbc, y, z)
        t_obtenido.append(ex[0, 0])
        t_esperado.append(t[0, j])

    print("error test", calc_rendimiento(np.array(t_obtenido), np.array(t_esperado), k))

    print(t_esperado[-1])
    print(t_obtenido[-1])

    # -----
    # CONTROLADOR NEURONAL
    # -----

    # ---
    # Constantes del modelo
    # ---
    g = 9.81    # [m/s^2]   Aceleración de la gravedad
    F = 0       # [N]       Fuerza externa
    m = 0.2     # [Kg]      Masa del péndulo
    l = 0.5     # [m]       Longitud del péndulo
    M = 2       # [Kg]      Masa del carro
    # ---

    dt = 0.005
    t = 0

    pos = []
    vel = []
    acel = []
    time = []

    cond_inic = [np.pi/6, 0]
    
    x = np.zeros(3)
    x[0] = cond_inic[0]
    x[1] = cond_inic[1]
    x[2] = 0

    Force = np.zeros((1, 1))
    force_hist = []

    plt.show()
    #exit()

    while(t < 20):

        x = update(x, dt, Force[0, 0])

        pos.append(x[0])
        vel.append(x[1])
        acel.append(x[2])
        
        entrada = np.array([x[0], x[1]])
        entrada.shape = (1, entrada.size)

        _, Force = salida_red(Wji, Wkj, theta_j, theta_k, entrada, y, z)

        Force[0, 0] *= std_dev_t[0]
        Force[0, 0] += media_t
        force_hist.append(Force[0, 0])
        time.append(t)

        t += dt

    fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(16, 5))
    ax0.plot(time, pos)
    #ax0.xlabel('Tiempo')
    #ax0.ylabel('Posición angular')
    ax0.grid()
    ax1.plot(time, vel)
    #ax1.xlabel('Tiempo')
    #ax1.ylabel('Velocidad angular')
    ax1.grid()
    ax2.plot(time, acel, label='Aceleración angular')
    #ax2.xlabel('Tiempo')
    #ax2.ylabel('Alpha/Fuerza')
    ax2.grid()
    
    plt.plot(time, force_hist, label='Fuerza')
    plt.legend()
    plt.show()
