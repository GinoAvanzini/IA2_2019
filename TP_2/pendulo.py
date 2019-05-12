
from math import sin, cos, pow, pi
from matplotlib import pyplot as plt


def generate_profile(center, step, theta, min=None, max=None):
    """
    
    """

    index_center = theta.index(center)

    if (min is not None):
        index_min = theta.index(min)
        prof1 = [0] * index_center
        for i in range(index_min, index_center):
            prof1[i] = (i - index_min) / (index_center - index_min)
    else:
        prof1 = [1] * index_center

    if (max is not None):
        index_max = theta.index(max)
        prof2 = [0] * (len(theta) - index_center)
        for i in range(index_center, index_max+1):
            prof2[i - index_center] = 1 - (i - index_center) / (index_max - index_center)
    else:
        prof2 = [1] * (len(theta) - index_center)

    return prof1+prof2


def fuzzifier(value, var, T):
    ans = []
    for profile in T:
        ans.append(profile[var.index(value)])
    return ans


def update(x, dt):

    x_t = x
    
    num = g * sin(x[0]) + cos(x[0]) * (- F - m * l * pow(x[1], 2) * sin(x[0])) / (M + m)
    den = l * (4/3 - m * pow(cos(x[0]), 2) / (M + m))

    x_t[2] = num / den

    x_t[1] = x[1] + x[2]*dt
    x_t[0] = x[0] + x[1]*dt + x[2]*pow(dt, 2)/2

    return x_t


if __name__ == "__main__":

    STEP = 5

    #--------------------------------------------------
    # Constantes del modelo
    #--------------------------------------------------
    g = 9.81    # [m/s^2]   Aceleración de la gravedad
    F = 0       # [N]       Fuerza externa
    m = 0.2     # [Kg]      Masa del péndulo
    l = 0.5     # [m]       Longitud del péndulo
    M = 2       # [Kg]      Masa del carro
    #--------------------------------------------------

    # dt = 0.001
    # t = 0

    # x = [-pi + 0.01, 0, 0]

    # pos = []
    # vel = []
    # acel = []
    # time = []

    # while(t < 2000):

    #     pos.append(x[0])
    #     vel.append(x[1])
    #     acel.append(x[2])
        
    #     x = update(x, dt)
        
    #     time.append(t)

    #     t += dt


    # fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(16, 5))
    # ax0.plot(time, pos)
    # ax0.grid()
    # ax1.plot(time, vel)
    # ax1.grid()
    # ax2.plot(time, acel)
    # ax2.grid()
    
    # plt.show()

    # Variable linguística: (theta, T(theta), U)
    #   - theta: Nombre de la variable
    #   - T(theta): MN, N, Z, P, MP
    #   - U: rango de -90 a 90 grados sexagesimales
    theta = list(range(-90, 90+STEP, STEP))

    # Generación de conjuntos borrosos
    MN = generate_profile(-60, STEP, theta, max=-30)
    N = generate_profile(-30, STEP, theta, min=-60, max=0)
    Z = generate_profile(0, STEP, theta, min=-30, max=30)
    P = generate_profile(30, STEP, theta, min=0, max=60)
    MP = generate_profile(60, STEP, theta, min=30)
    
    T = (MN, N, Z, P, MP)
    for i in T:
        plt.plot(theta, i)
    plt.grid()
    plt.show()

    print(fuzzifier(-45, theta, T))