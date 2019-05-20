
from math import sin, cos, pow, pi
from numpy import arange, searchsorted, zeros
from matplotlib import pyplot as plt

from binary_search import binary_search


def generate_profile(center, var, min=None, max=None):
    """
    
    """

    index_center = binary_search(var, center)
    if (min is not None):
        index_min = binary_search(var, min)
        prof1 = [0] * index_center
        for i in range(index_min, index_center):
            prof1[i] = (i - index_min) / (index_center - index_min)
    else:
        prof1 = [1] * index_center

    if (max is not None):
        index_max = binary_search(var, max)
        prof2 = [0] * (len(var) - index_center)
        for i in range(index_center, index_max+1):
            prof2[i - index_center] = 1 - (i - index_center) / (index_max - index_center)
    else:
        prof2 = [1] * (len(var) - index_center)

    return prof1+prof2


# def fuzzifier(value, var, T):
#     ans = []
#     for profile in T:
#         ans.append(profile[var.index(value)])
#     return ans

# def defuzzifier(G, var):
#     for i in enumerate(G)
#     return value


def fuzzifier(value, fuzzy_set):

    ans = {}
    for magnitud in fuzzy_set[1]:
        ans[magnitud] = fuzzy_set[1][magnitud][fuzzy_set[0].searchsorted(value)]

    return ans


# Value es un array con los valores de theta y thetadot
def fuzzy_control(value, theta, v, R, F):

    mu_theta = fuzzifier(value[0], theta)
    mu_thetadot = fuzzifier(value[1], v)

    v_antec = {'MN': 0, 'N': 0, 'Z':0, 'P': 0, 'MP': 0}

    for theta_r in R.keys():
        for thetadot_r in R[theta_r].keys():
            if (mu_thetadot[thetadot_r] == 0) or (mu_theta[theta_r] == 0):  # Usar isclose() para eliminar error de float
                continue
            
            antec = min(mu_theta[theta_r], mu_thetadot[thetadot_r])

            if (antec > v_antec[R[theta_r][thetadot_r]]):
                v_antec[R[theta_r][thetadot_r]] = antec
            
    # Implicación/truncado de conjuntos de salida:
    print(v_antec)
    
    F_out = zeros(len(F[0]))

    for i in F[1].keys():
        for j in range(0, len(F[0])):

            min_temp = min(F[1][i][j], v_antec[i])

            if (min_temp > F_out[j]):
                F_out[j] = min_temp            

    
    plt.plot(F[0], F_out)

    plt.show()

    return F_out 



# def fuzzy_control(value, theta, v, T):
#     # Borrosificación
#     mu = fuzzifier(value, theta, T)

#     # Cálculo de antecedentes
#     # Por ahora es relación directa

#     # Truncado de conjuntos borrosos de salida 
#     # (RECORDAR: Por ahora los conjuntos de entrada y salida son los mismos,
#     # por eso se utiliza la misma variable)
#     newT = list(T)
#     for i, profile in enumerate(T):
#         for j, value in enumerate(profile):
#             if (mu[i] < value):
#                 newT[i][j] = mu[i]
#             else:
#                 newT[i][j] = value

#     for i in newT:
#         plt.plot(theta, i)
#     plt.grid()
#     plt.show()

#     # Disyunción/Unión de los conjuntos borrosos de salida
#     G = []
#     for i in range(0, len(theta)):
#         max_value = 0
#         for profile in T:
#             if (max_value < profile[i]):
#                 max_value = profile[i]
#         G.append(max_value)

#     print(G, len(theta), len(G))
#     plt.plot(theta, G)
#     plt.grid()
#     plt.show()

    # Desborrosificación
    


def update(x, dt):

    x_t = x
    
    num = g * sin(x[0]) + cos(x[0]) * (- F - m * l * pow(x[1], 2) * sin(x[0])) / (M + m)
    den = l * (4/3 - m * pow(cos(x[0]), 2) / (M + m))

    x_t[2] = num / den

    x_t[1] = x[1] + x[2]*dt
    x_t[0] = x[0] + x[1]*dt + x[2]*pow(dt, 2)/2

    return x_t


if __name__ == "__main__":

    T_STEP = 5
    V_STEP = 0.005
    A_STEP = 0.01

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
    #   - A: Nombre de la variable
    #   - T(A): MN, N, Z, P, MP
    #   - U: rango de -90 a 90 grados sexagesimales
    theta = []
    v = []
    
    theta.append(arange(-90, 90+T_STEP, T_STEP))
    v.append(arange(-0.05, 0.05+V_STEP, V_STEP))
    # a = arange(-0.2, 0.2+A_STEP, A_STEP)
    for i in range(0, len(v[0])):
        v[0][i] = round(v[0][i], 3)
    # print(v[0])

    # Generación de conjuntos borrosos de entradas
    # Conjunto borroso de theta:
    theta.append({})
    theta[1]['MN'] = generate_profile(-60, theta[0], max=-30)
    theta[1]['N'] = generate_profile(-30, theta[0], min=-60, max=0)
    theta[1]['Z'] = generate_profile(0, theta[0], min=-30, max=30)
    theta[1]['P'] = generate_profile(30, theta[0], min=0, max=60)
    theta[1]['MP'] = generate_profile(60, theta[0], min=30)
    # Conjunto borroso de velocidad angular:
    v.append({})
    v[1]['MN'] = generate_profile(-0.04, v[0], max=-0.025)
    v[1]['N'] = generate_profile(-0.02, v[0], min=-0.04, max=0)
    v[1]['Z'] = generate_profile(0, v[0], min=-0.025, max=0.025)
    v[1]['P'] = generate_profile(0.02, v[0], min=0, max=0.04)
    v[1]['MP'] = generate_profile(0.04, v[0], min=0.025)
    
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(16, 5))
    for i in theta[1].values():
        ax0.plot(theta[0], i)
        # print(i)
    ax0.grid()

    for i in v[1].values():
        ax1.plot(v[0], i)
        # print(i)
    ax1.grid()

    plt.show()

    F_STEP = 0.25
    F = []
    F.append(arange(-5, 5+F_STEP, F_STEP))

    # Generación de conjuntos borrosos de salida
    F.append({})
    F[1]['MN'] = generate_profile(-4, F[0], max=-2.5)
    F[1]['N'] = generate_profile(-2, F[0], min=-4, max=0)
    F[1]['Z'] = generate_profile(0, F[0], min=-2.5, max=2.5)
    F[1]['P'] = generate_profile(2, F[0], min=0, max=4)
    F[1]['MP'] = generate_profile(4, F[0], min=2.5)

    # Reglas de inferencia. R['MN']['P'] indica la magnitud de la fuerza 
    # para theta MN y theta_dot P
    R = {
        'MN': {'MN': 'MN', 'N': 'MN', 'Z': 'MN', 'P': 'N', 'MP': 'Z'},
        'N': {'MN': 'MN', 'N': 'MN', 'Z': 'N', 'P': 'Z', 'MP': 'P'},
        'Z': {'MN': 'MN', 'N': 'N', 'Z': 'Z', 'P': 'P', 'MP': 'MP'},
        'P': {'MN': 'N', 'N': 'Z', 'Z': 'P', 'P': 'MP', 'MP': 'MP'},
        'MP': {'MN': 'Z', 'N': 'P', 'Z': 'MP', 'P': 'MP', 'MP': 'MP'}
        }
    for i in theta[1]:
        plt.plot(F[0], F[1][i], label=i)
    plt.grid()
    plt.legend(loc="upper right")

    # print(theta[0])

    # print(fuzzifier(20, theta))
    # fuzzy_control(value, theta, v, R, F):
    value = [20, -0.02]
    fuzzy_control(value, theta, v, R, F)

    # fuzzy_control(20, theta, T)
