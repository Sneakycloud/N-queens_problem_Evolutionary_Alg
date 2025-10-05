import matplotlib.pyplot as plt
from main import info_n_queen_solver
from Base_algorithm.base import info_base_n_queen_solver

def n_queen_plot(itererations, board_sizes_n : list, boards_per_generation, children_per_generation, mutation_rate, max_generations, stall_limit, ignore_failed_attempts, pop_init_algorithm, main_algorithm, print_to_file, txt_file_name):
    #Variable init, these hold the values for each run of n
    avg_time_taken_n = []
    avg_generations_taken_n = []
    probaility_of_success = []
    
    #Run info_n_queen solver for data gathering
    for board_size_n in board_sizes_n:
        print(f"\nStarting iterations for board size {board_size_n}")
        if(main_algorithm == 0):
            _, generations_taken, time_taken, successes = info_base_n_queen_solver(itererations, board_size_n, boards_per_generation, children_per_generation, mutation_rate, ignore_failed_attempts, max_generations, print_to_file, txt_file_name)
        elif (main_algorithm == 1):
            _, generations_taken, time_taken, successes = info_n_queen_solver(itererations, board_size_n, boards_per_generation, mutation_rate, max_generations, stall_limit, ignore_failed_attempts, pop_init_algorithm, print_to_file, txt_file_name)
        avg_generations_taken_n.append(sum(generations_taken) / len(generations_taken))
        avg_time_taken_n.append(sum(time_taken) / len(time_taken))
        probaility_of_success.append(successes / itererations)
        
    #ploting graph
    plt.subplot(311)
    plt.plot(board_sizes_n,avg_time_taken_n)
    plt.ylabel("Avg ime (s)")
    
    plt.subplot(312)
    plt.plot(board_sizes_n,avg_generations_taken_n)
    plt.ylabel("Avg generations taken")
    
    plt.subplot(313)
    plt.plot(board_sizes_n,probaility_of_success)
    plt.axis((0,max(board_sizes_n), 0, 1))
    plt.xlabel("Size of n")
    plt.ylabel("Success rate")
    
    plt.show()
    
    return



#ploting graph manually, the below is based on the plot_results.txt in the "base_algorithm" folder. This took 72 minutes to run
"""
plt.subplot(311)
plt.plot([x for x in range(4,12)],[0.0334375, 0.044375, 0.385, 0.570625, 3.3434375, 11.382291666666667, 15.905133928571429,11.546875])
plt.axis((0,12, 0, 20))
plt.ylabel("Avg time (s)")

plt.subplot(312)
plt.plot([x for x in range(4,12)],[6.79, 8.39, 70.41, 96.61, 530.84, 1686.6933333333334, 2213.4285714285716, 1503.0])
plt.axis((0,12, 0, 2500))
plt.ylabel("Avg generations taken")

plt.subplot(313)
plt.plot([x for x in range(4,13)],[1, 1, 1, 1, 1, 75/100, 14/100, 1/100, 0])
plt.axis((0,12, 0, 1))
plt.xlabel("Size of n")
plt.ylabel("Success rate")

plt.show()
"""



if __name__ == "__main__":
    #Parameters to adjust for plot function
    itererations = 500

    #board_sizes_n = [8, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    board_sizes_n = [x for x in range(4,13)] #[8, 10, 15, 20, 25, 30, 35, 40, 45, 50]
    #board_sizes_n.extend([35,40,45,50])

    boards_per_generation = 768
    children_per_generation = boards_per_generation*2
    mutation_rate = 50
    max_generations = 4000
    stall_limit = 500
    ignore_failed_attempts = False
    #0 makes the solver use a shuffled board from 0 to n-1, while a 1 makes the solver use a heuristic function to generate the initial boards
    pop_init_algorithm = 1 
    #0 makes the algorithm into the simplistic base evolutionary algorithm, while 1 makes the algorithm into the improved version
    main_algorithm = 0
    #if to print to file
    print_to_file = True
    txt_file_name = "plot_results.txt"
        
    #Runs the plot function
    open(txt_file_name, "w").close()
    n_queen_plot(itererations, board_sizes_n, boards_per_generation,children_per_generation, mutation_rate, max_generations, stall_limit, ignore_failed_attempts, pop_init_algorithm, main_algorithm,print_to_file,txt_file_name)