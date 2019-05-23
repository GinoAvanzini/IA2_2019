
from math import sin, cos, pow, pi
from numpy import arange, searchsorted, zeros
from matplotlib import pyplot as plt

from binary_search import binary_search


def generate_profile(center, var, min=None, max=None):
    """
    
    """

    index_center = var.searchsorted(center)
    if (min is not None):
        index_min = var.searchsorted(min)
        prof1 = [0] * index_center
        for i in range(index_min, index_center):
            prof1[i] = (i - index_min) / (index_center - index_min)
    else:
        prof1 = [1] * index_center

    if (max is not None):
        index_max = var.searchsorted(max)
        prof2 = [0] * (len(var) - index_center)
        for i in range(index_center, index_max+1):
            prof2[i - index_center] = 1 - (i - index_center) / (index_max - index_center)
    else:
        prof2 = [1] * (len(var) - index_center)

    return prof1+prof2


def fuzzifier(value, fuzzy_set):

    ans = {}
    for magnitud in fuzzy_set[1]:
        ans[magnitud] = fuzzy_set[1][magnitud][fuzzy_set[0].searchsorted(value)]

    return ans


# Defuzzifier usando centro de gravedad (COG)
def defuzzifier(F_out, F):

    num = 0
    den = 0
    for pert, pos in zip(F_out, F):
        num += pos*pert
        den += pert

    return F[F.searchsorted(num/den)]


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
    F_out = zeros(len(F[0]))

    for i in F[1].keys():
        for j in range(0, len(F[0])):

            min_temp = min(F[1][i][j], v_antec[i])

            if (min_temp > F_out[j]):
                F_out[j] = min_temp            

    # plt.plot(F[0], F_out)

    force = defuzzifier(F_out, F[0])

    return force    


def update(x, dt, F):

    x_t = x

    num = g * sin(x[0]) + cos(x[0]) * (- F - m * l * pow(x[1], 2) * sin(x[0])) / (M + m)
    den = l * (4/3 - m * pow(cos(x[0]), 2) / (M + m))

    x_t[2] = num / den

    x_t[1] = x[1] + x[2]*dt
    x_t[0] = x[0] + x[1]*dt + x[2]*pow(dt, 2)/2

    return x_t


if __name__ == "__main__":

    T_STEP = 0.001      # [rad]
    V_STEP = 0.005      # [rad/s]
    A_STEP = 0.01
    F_STEP = 0.05


    #--------------------------------------------------
    # Constantes del modelo
    #--------------------------------------------------
    g = 9.81    # [m/s^2]   Aceleración de la gravedad
    F = 0       # [N]       Fuerza externa
    m = 0.2     # [Kg]      Masa del péndulo
    l = 0.5     # [m]       Longitud del péndulo
    M = 2       # [Kg]      Masa del carro
    #--------------------------------------------------

    dt = 0.05
    t = 0

    pos = []
    vel = []
    acel = []
    time = []

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
    #   - U: rango de -2*pi a 2*pi grados sexagesimales
    theta = []
    v = []

    ang_vel = 15
    force_mag = 10
    
    theta.append(arange(-2*pi, 2*pi+T_STEP, T_STEP))
    v.append(arange(-ang_vel, ang_vel+V_STEP, V_STEP))
    for i in range(0, len(v[0])):
        v[0][i] = round(v[0][i], 3)

    # Generación de conjuntos borrosos de entradas

    # Conjunto borroso de theta:
    theta.append({})
    theta[1]['MN'] = generate_profile(-pi/4, theta[0], max=-pi/6)
    theta[1]['N'] = generate_profile(-pi/9, theta[0], min=-pi/3, max=0)
    theta[1]['Z'] = generate_profile(0, theta[0], min=-pi/6, max=pi/6)
    theta[1]['P'] = generate_profile(pi/9, theta[0], min=0, max=pi/3)
    theta[1]['MP'] = generate_profile(pi/4, theta[0], min=pi/6)

    # Conjunto borroso de velocidad angular:
    v.append({})
    v[1]['MN'] = generate_profile(-9, v[0], max=-3.75)
    v[1]['N'] = generate_profile(-3.5, v[0], min=-6.5, max=-0.03*pi)
    v[1]['Z'] = generate_profile(0, v[0], min=-3, max=3)
    v[1]['P'] = generate_profile(3.5, v[0], min=0.03*pi, max=6.5)
    v[1]['MP'] = generate_profile(9, v[0], min=3.75)
    
    fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(16, 5))
    for i in theta[1].values():
        ax0.plot(theta[0], i)
    ax0.grid()

    for i in v[1].values():
        ax1.plot(v[0], i)
    ax1.grid()

    plt.show()

    F = []
    F.append(arange(-7*force_mag, 7*force_mag+F_STEP, F_STEP))

    # Generación de conjuntos borrosos de salida
    F.append({})
    F[1]['MN'] = generate_profile(-5*force_mag, F[0], max=-3.5*force_mag)
    F[1]['N'] = generate_profile(-1.25*force_mag, F[0], min=-3.75*force_mag, max=0)
    F[1]['Z'] = generate_profile(0, F[0], min=-1.5*force_mag, max=1.5*force_mag)
    F[1]['P'] = generate_profile(1.25*force_mag, F[0], min=0, max=3.75*force_mag)
    F[1]['MP'] = generate_profile(5*force_mag, F[0], min=3.5*force_mag)

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


    cond_inic = [pi/4, pi/8]
    
    x = zeros(3)
    x[0] = cond_inic[0]
    x[1] = cond_inic[1]
    x[2] = 0

    Force = 0
    force_hist = []

    print(x)

    while(t < 8):

        x = update(x, dt, Force)

        pos.append(x[0])
        vel.append(x[1])
        acel.append(x[2])
        
        Force = fuzzy_control([x[0], x[1]], theta, v, R, F)
        force_hist.append(Force)
        time.append(t)

        t += dt

    fig, (ax0, ax1, ax2) = plt.subplots(1, 3, figsize=(16, 5))
    ax0.plot(time, pos)
    ax0.grid()
    ax1.plot(time, vel)
    ax1.grid()
    ax2.plot(time, acel)
    ax2.grid()
    
    
    plt.plot(time, force_hist)
    plt.show()


#
