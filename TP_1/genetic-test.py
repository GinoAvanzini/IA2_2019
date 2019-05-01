#!/usr/bin/env python

from genetic import genetic, generate_ind
from simulated_annealing import map_to_coord, temple_simulado, neighbours_annealing, distance
from matplotlib import pyplot as plt
from random import randint, choices

import csv

N_POB = 10 # Cantidad de individuos en la población
MAX_LENGHT = 32 # Cantidad de estanterías
T_0 = 200 # Temperatura inicial a la que inicia el algoritmo de temple simulado
MAX_GEN = 50 # Máxima cantidad de iteraciones a la que corta el algoritmo genético

conjunto = []

prob = []

estant = [i for i in range(0, MAX_LENGHT)]

for i in range(0, 25):
    prob.append(0.1)

for i in range(25, MAX_LENGHT):
    prob.append(0.5)

for i in range(0, 8):
    conjunto.append(choices(population=estant, k=randint(3, 7), weights=prob))

print(conjunto)


start = []
for i in range(0, N_POB):
    start.append(generate_ind())

best, history = genetic(start, conjunto, hist=True)
print(best)
print("DONE")

with open('../tests/fitness-test.csv', mode='w') as temp_file:
    writer = csv.writer(temp_file, quoting=csv.QUOTE_NONE)

    writer.writerow(['GEN', 'fitness'])

    for i in range(0, N_POB):
        writer.writerow([i, history[i]])

cost0 = []
cost1 = []

for orden in conjunto:
    coordenadas = map_to_coord(orden)
    _, costo = temple_simulado(coordenadas, 200, neighbours_annealing, distance)
    cost0.append(costo)

    # Generación de población inicial
    start = []
    for i in range(0, N_POB):
        start.append(generate_ind())

    new_layout, _ = genetic(start, [orden])

    orden_estant = []
    for prod in orden:
        orden_estant.append(new_layout.index(prod))

    coordenadas = map_to_coord(orden_estant)
    _, costo = temple_simulado(coordenadas, 200, neighbours_annealing, distance)
    cost1.append(costo)


fig, ax = plt.subplots(1, 2)
ax[0].plot(cost0, label="costo con layout sin optimizar")
ax[0].plot(cost1, label="costo con layout optimizado")
ax[0].grid()

avg = 0
for i, j in zip(cost0, cost1):
    avg += (i - j) / i
avg = avg * 100 / len(cost0)

# print(avg)

ans = []

mut_prob = list(range(0, 70, 10))

for m in mut_prob:
    cost0 = []
    cost1 = []

    for orden in conjunto:
        coordenadas = map_to_coord(orden)
        _, costo = temple_simulado(coordenadas, 200, neighbours_annealing, distance)
        cost0.append(costo)

        # Generación de población inicial
        start = []
        for i in range(0, N_POB):
            start.append(generate_ind())

        new_layout, _ = genetic(start, [orden], mut=m)

        orden_estant = []
        for prod in orden:
            orden_estant.append(new_layout.index(prod))

        coordenadas = map_to_coord(orden_estant)
        _, costo = temple_simulado(coordenadas, 200, neighbours_annealing, distance)
        cost1.append(costo)

    avg = 0
    for i, j in zip(cost0, cost1):
        avg += (i - j) / i
    avg = avg * 100 / len(cost0)

    ans.append(avg)

ax[1].plot(mut_prob, ans)
ax[1].grid()

plt.savefig("genetic_test.png")
