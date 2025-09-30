import matplotlib.pyplot as plt
from main import info_n_queen_solver
from Base_algorithm.base import info_base_n_queen_solver

def n_queen_plot(itererations, board_sizes_n : list, boards_per_generation, children_per_generation, mutation_rate, max_generations, stall_limit, ignore_failed_attempts, pop_init_algorithm, main_algorithm):
    #Variable init, these hold the values for each run of n
    avg_time_taken_n = []
    avg_generations_taken_n = []
    
    #Run info_n_queen solver for data gathering
    for board_size_n in board_sizes_n:
        print(f"\nStarting iterations for board size {board_size_n}")
        if(main_algorithm == 0):
            _, generations_taken, time_taken = info_base_n_queen_solver(itererations, board_size_n, boards_per_generation, children_per_generation, mutation_rate, ignore_failed_attempts, max_generations)
        elif (main_algorithm == 1):
            _, generations_taken, time_taken = info_n_queen_solver(itererations, board_size_n, boards_per_generation, mutation_rate, max_generations, stall_limit, ignore_failed_attempts, pop_init_algorithm)
        avg_generations_taken_n.append(sum(generations_taken) / len(generations_taken))
        avg_time_taken_n.append(sum(time_taken) / len(time_taken))
        
    #ploting graph
    plt.subplot(211)
    plt.plot(board_sizes_n,avg_time_taken_n)
    plt.xlabel("Size of n")
    plt.ylabel("Average time (s)")
    
    plt.subplot(212)
    plt.plot(board_sizes_n,avg_generations_taken_n)
    plt.xlabel("Size of n")
    plt.ylabel("Average generations taken")
    
    plt.show()
    
    return


#Parameters to adjust for plot function
itererations = 50

#board_sizes_n = [8, 10, 15, 20, 25, 30, 35, 40, 45, 50]
board_sizes_n = [x for x in range(4,13)] #[8, 10, 15, 20, 25, 30, 35, 40, 45, 50]
#board_sizes_n.extend([35,40,45,50])

boards_per_generation = 1000
children_per_generation = 1000
mutation_rate = 60
max_generations = 4000
stall_limit = 500
ignore_failed_attempts = False
#0 makes the solver use a shuffled board from 0 to n-1, while a 1 makes the solver use a heuristic function to generate the initial boards
pop_init_algorithm = 1 
main_algorithm = 0
    
#Runs the plot function
n_queen_plot(itererations, board_sizes_n, boards_per_generation,children_per_generation, mutation_rate, max_generations, stall_limit, ignore_failed_attempts, pop_init_algorithm, main_algorithm)