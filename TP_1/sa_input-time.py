
from simulated_annealing import temple_simulado, neighbours_annealing, distance, map_to_coord

from time import time
from random import randint
import csv

ITER = 35


if __name__ == "__main__":
    
    # Cantidad de productos en una orden
    inputs = [3, 5, 7, 10, 13, 15, 20, 25, 30]
    #inputs = [3]
    
    # Tiempo promedio de ejecución en función de cada input
    time_exec = []
    
    with open('sa_input-time.csv', mode='w') as input_file:

        for i in inputs:
            time_avg = 0
            pos_pick = []
    
            for j in range(0, ITER):
                pos_pick = [randint(0, 31) for i in range(0, i)]

                coordenadas = map_to_coord(pos_pick)
                
                start = time()
                _ = temple_simulado(coordenadas, 75, neighbours_annealing, distance)
                end = time()
                
                time_avg += end - start
                
            time_avg = time_avg/ITER
            time_exec.append(time_avg)
        
        writer = csv.writer(input_file, quoting=csv.QUOTE_NONE)
        
        writer.writerow(['n_inputs', 'avg_time'])
        
        for i in range(0, len(inputs)):
            writer.writerow([inputs[i], time_exec[i]])


#
