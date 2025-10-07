import matplotlib.pyplot as plt
import math
from main import info_n_queen_solver
from Base_algorithm.base import info_base_n_queen_solver

def n_queen_plot(itererations, board_sizes_n : list, boards_per_generation, children_per_generation, mutation_rate, max_generations, stall_limit, ignore_failed_attempts, pop_init_algorithm, main_algorithm, print_to_file, txt_file_name):
    #Variable init, these hold the values for each run of n
    avg_time_taken_n = []
    avg_generations_taken_n = []
    probaility_of_success = []
    max_board_size = 0
    last_idx_used = 0
    
    #Run info_n_queen solver for data gathering
    for i, board_size_n in enumerate(board_sizes_n):
        print(f"\nStarting iterations for board size {board_size_n}")
        if(main_algorithm == 0):
            _, generations_taken, time_taken, successes = info_base_n_queen_solver(itererations, board_size_n, boards_per_generation, children_per_generation, mutation_rate, ignore_failed_attempts, max_generations, print_to_file, txt_file_name)
        elif (main_algorithm == 1):
            _, generations_taken, time_taken, successes = info_n_queen_solver(itererations, board_size_n, boards_per_generation, mutation_rate, max_generations, stall_limit, ignore_failed_attempts, pop_init_algorithm, print_to_file, txt_file_name)
        avg_generations_taken_n.append(sum(generations_taken) / len(generations_taken))
        avg_time_taken_n.append(sum(time_taken) / len(time_taken))
        probaility_of_success.append(successes / itererations)
        
        max_board_size = board_size_n
        last_idx_used = i
        if successes == 0:
            break

    #if we used all board sizes and did fail all cases
    smallest_board_size = 4

    #ploting graph
    plt.subplot(311)
    plt.plot(board_sizes_n[:last_idx_used+1],avg_time_taken_n)
    plt.axis((smallest_board_size,max_board_size, 0, math.ceil(max(avg_time_taken_n))))
    plt.ylabel("Avg time (s)")
    
    plt.subplot(312)
    plt.plot(board_sizes_n[:last_idx_used+1],avg_generations_taken_n)
    plt.axis((smallest_board_size,max_board_size, 0, math.ceil(max(avg_generations_taken_n))))
    plt.ylabel("Avg generations taken")

    plt.subplot(313)
    plt.plot(board_sizes_n[:last_idx_used+1],probaility_of_success)
    plt.axis((smallest_board_size,max_board_size, 0, 1))
    plt.xlabel("Size of n")
    plt.ylabel("Success rate")
    
    plt.show()
    
    return


"""
#ploting graph manually, the below is based on the plot_results.txt in the "base_algorithm" folder. This took 72 minutes to run
plt.subplot(311)
plt.plot([x for x in range(4,13)],[0.00296875, 0.0034375, 0.0146875, 0.00453125, 0.69875, 8.13171875, 26.0378125, 33.10421875, 33.164375])
plt.axis((0,14, 0, 40))
plt.ylabel("Avg time (s)")

plt.subplot(312)
plt.plot([x for x in range(4,13)],[0,0,1.77,0,94.84,1014.24,3103.22,3771.98,3880.0])
plt.axis((0,14, 0, 4000))
plt.ylabel("Avg generations taken")

plt.subplot(313)
plt.plot([x for x in range(4,14)],[1, 1, 1, 1, 1, 86/100, 27/100, 7/100, 3/100, 0])
plt.axis((0,14, 0, 1))
plt.xlabel("Size of n")
plt.ylabel("Success rate")

plt.show()
"""


if __name__ == "__main__":
    #Parameters to adjust for plot function
    itererations = 5

    #board_sizes_n = [8, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    board_sizes_n = [x for x in range(8,11)] #[8, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    #board_sizes_n.extend([35,40,45,50])

    boards_per_generation = 768
    children_per_generation = 1000
    mutation_rate = 92
    max_generations = 4000
    stall_limit = 500
    ignore_failed_attempts = False
    #0 makes the algorithm into the simplistic base evolutionary algorithm, while 1 makes the algorithm into the improved version
    main_algorithm = 0
    #Only for main algorithm: 0 makes the solver use a shuffled board from 0 to n-1, while a 1 makes the solver use a heuristic function to generate the initial boards
    pop_init_algorithm = 0 
    #if to print to file
    print_to_file = False
    txt_file_name = "plot_results.txt"
        
    #Runs the plot function
    open(txt_file_name, "w").close()
    n_queen_plot(itererations, board_sizes_n, boards_per_generation,children_per_generation, mutation_rate, max_generations, stall_limit, ignore_failed_attempts, pop_init_algorithm, main_algorithm,print_to_file,txt_file_name)