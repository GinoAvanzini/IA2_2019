
import pandas as pd
import numpy as np

from math import sqrt


def factiv_oc(yvec):
    return 1/(1 + np.exp(-yvec)) 


def fdotactiv_oc(yvec):

    sigm = factiv_oc(yvec)
    res = np.multiply(sigm, 1 - sigm)

    return res


def factiv_sal(zvec):
    # Identidad
    return zvec


def fdotactiv_sal(zvec):
    return np.ones(zvec.shape)


def backprop(Wji, Wkj, theta_j, theta_k, x, y, z, t, eps):
    
    # Pesos oculta-salida
    h_mu_k = np.zeros(z.shape)
    h_mu_k = (np.matmul(y, Wkj)) - theta_k

    delta_mu_k = np.multiply( (t - factiv_sal(h_mu_k)),\
        fdotactiv_sal(h_mu_k) )

    Wkj += eps*(np.matmul(y.T, delta_mu_k))

    theta_k += eps*(-1*delta_mu_k)

    # Pesos entrada-oculta
    h_mu_j = np.zeros(y.shape)
    h_mu_j = (np.matmul(x, Wji)) - theta_j

    delta_mu_j = np.multiply((np.matmul(delta_mu_k, Wkj.T)),\
        fdotactiv_oc(h_mu_j))

    Wji += eps*(np.matmul(x.T, delta_mu_j))
    theta_j += eps*(-1*delta_mu_j)

    return


def salida_red(Wji, Wkj, theta_j, theta_k, x, y, z):

    y_temp = np.zeros(y.shape)
    z_temp = np.zeros(z.shape)
    y_temp = (np.matmul(x, Wji)) - theta_j

    y = factiv_oc(y_temp)
    
    z_temp = (np.matmul(y, Wkj)) - theta_k

    z = factiv_sal(z_temp)

    return y, z


# def calc_rendimiento(t_obtenido, t_esperado, media_t):
def calc_rendimiento(t_obtenido, t_esperado, n):

    # num = np.sum(np.square(t_obtenido - t_esperado))
    # den = np.sum(np.square(t_esperado - media_t))

    # return sqrt(num/den)

    num = np.sum(np.abs(t_obtenido - t_esperado))

    return num/k


if __name__ == "__main__":

    # ------------------
    # Variables 
    NEURONAS_ENTRADA = 5
    NEURONAS_CAPA_OCULTA = 15
    NEURONAS_SALIDA = 1

    EPS = 0.1
    EPOCHS = 10

    EJEMPLOS = 1
    # ------------------

    data = pd.read_csv("./USA_Housing.csv")
    data = data.drop(data.columns[6], axis=1)

    t = np.asarray(data['Price'], dtype=np.float64)
    t.shape = (NEURONAS_SALIDA, t.size)

    data = data.drop(data.columns[5], axis=1)

    data = np.asarray(data);

    # Normalización
    media = []
    std_dev = []

    for i in range(0, data[0, :].size):
        media.append(np.mean(data[:, i]))
        data[:, i] = data[:, i] - media[i]
        std_dev.append(np.std(data[:, i]))
        data[:, i] = data[:, i]/std_dev[i]

    media_t = []
    std_dev_t = []
    for j in range(0, t[:, 0].size):
        media_t.append(np.mean(t[j, :]))
        t[j, :] = t[j, :] - media_t[j]
        std_dev_t.append(np.std(t[j, :]))
        t[j, :] = t[j, :]/std_dev_t[j]

    data_train = data[0:3500]
    t_train = t[0:3500]
    INDEX_TRAIN = 3500

    data_valid = data[3501:4200]
    t_valid = t[3501:4200]
    INDEX_VALID = 4200

    data_test = data[4201:-1]
    t_test = t[4201:-1]

    print(t_train.shape, t_valid.shape, t_test.shape, t.shape)

    # x = np.zeros((EJEMPLOS, NEURONAS_ENTRADA), dtype=np.float64)
    x = np.zeros((1, NEURONAS_ENTRADA), dtype=np.float64)
    y = np.zeros((1, NEURONAS_CAPA_OCULTA), dtype=np.float64)
    z = np.zeros((1, NEURONAS_SALIDA), dtype=np.float64)

    # Inicialización de pesos y sesgos
    Wji = np.asarray([[(2*np.random.random_sample() - 1) \
        for i in range(NEURONAS_CAPA_OCULTA)] \
            for j in range(NEURONAS_ENTRADA)], dtype=np.float64)
    # theta_j = np.asarray([(2*np.random.random_sample() - 1) \
    #     for i in range(NEURONAS_CAPA_OCULTA)], dtype=np.float64)
    # theta_j = np.asarray(0.01 for i in range(NEURONAS_CAPA_OCULTA), dtype=np.float64)
    theta_j = 0.01*np.ones((1, NEURONAS_CAPA_OCULTA), dtype=np.float64)
    theta_j.shape = (1, theta_j.size)


    Wkj = np.asarray([[(2*np.random.random_sample() - 1) \
        for i in range(NEURONAS_SALIDA)] \
            for j in range(NEURONAS_CAPA_OCULTA)], dtype=np.float64)

    # theta_k = np.asarray([(2*np.random.random_sample() - 1) \
    #     for i in range(NEURONAS_SALIDA)], dtype=np.float64)
    theta_k = 0.01*np.ones((1, NEURONAS_SALIDA), dtype=np.float64)
    theta_k.shape = (1, theta_k.size)

    xprueba = data_train[1, :]
    xprueba.shape = (1, NEURONAS_ENTRADA)


    tprueba = t_train[0, 1]
    print(tprueba)

    y, ex = salida_red(Wji, Wkj, theta_j, theta_k, xprueba, y, z)
    
    print(tprueba, ex)

    backprop(Wji, Wkj, theta_j, theta_k, xprueba, y, z, tprueba, EPS)
    
    
    y, ex = salida_red(Wji, Wkj, theta_j, theta_k, xprueba, y, z)
    
    print(tprueba, ex)



    # ----- TRAINING -----
    for epoch in range(0, EPOCHS):
        k = 0

        t_esperado = []
        t_obtenido = []

        print("EPOCH: ", epoch)
        for j in range(0, INDEX_TRAIN):

            k += 1            
            # if (k > BATCHSIZE):
            #     k = 0
            #     # backprop
            # print(t[0, j])
            xbc = data[j, :]
            xbc.shape = (1, NEURONAS_ENTRADA)

            y, ex = salida_red(Wji, Wkj, theta_j, theta_k, xbc, y, z)
            t_obtenido.append(ex)
            t_esperado.append(t[0, j])
            
            backprop(Wji, Wkj, theta_j, theta_k, xbc, y, z, t[0, j], EPS)
        

        # ----- VALIDATION -----
        print("error", 1 - calc_rendimiento(np.asarray(t_obtenido), np.asarray(t_esperado), k))
        # shufleo
        # print(t_esperado)
        # print(t_obtenido)




    # ----- TEST -----