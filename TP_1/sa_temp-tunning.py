
from simulated_annealing import temple_simulado, neighbours_annealing, distance, map_to_coord

from time import time
from random import randint
import csv

ITER = 50
N = 15  # Cant de productos por orden


if __name__ == "__main__":
    
    t0 = [10, 25, 50, 100, 150, 200, 250, 300, 350, 400, 450, 500]
    
    #t0 = [10, 25, 50]
    
    improvement = []
    time_exec = []
    
    
    with open('sa_temp-tunning.csv', mode='w') as temp_file:
    
        for temp in t0:
            improvement_avg = 0
            time_avg = 0
            
            for i in range(0, ITER):
                pos_pick = [randint(0, 31) for i in range(0, N)]
                
                coordenadas = map_to_coord(pos_pick)
                
                energy_start = distance(coordenadas)
                
                start = time()
                _, energy_end = temple_simulado(coordenadas, temp, neighbours_annealing, distance)
                end = time()
                
                time_avg += end - start
                improvement_avg += (energy_start - energy_end)/energy_start
                
            improvement_avg = improvement_avg/ITER
            improvement.append(improvement_avg)
            
            time_avg = time_avg/ITER
            time_exec.append(time_avg)
            
        
        writer = csv.writer(temp_file, quoting=csv.QUOTE_NONE)
        
        writer.writerow(['temp', 'avg_time', 'rel_delta'])
                
        for i in range(0, len(t0)):
            writer.writerow([t0[i], time_exec[i], improvement[i]])

        
    print(t0)
    print(improvement)
    print(time_exec)
    #print(coordenadas)
    #print(distance(coordenadas), "\n")

    
    #print(best_path[0],"\n",best_path[1])
