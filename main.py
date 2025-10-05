#Eddie Olofsgård, Besan Ewir, Sandra Carlsson, Ebba Brage
import random
import time
import itertools
import statistics
from contextlib import redirect_stdout
from collections import Counter
from pop_init import population_initliziser_random, population_initliziser_heuristic
from ga_select import fitness, select, tournament_select
from mutation import mutate, mutate_extend
from recombine import recombine
from calibration import gen_size_tuner, mutation_rate_tuner, mutation_rate_tuner_2

def print_board(board):
    """Converts the ordered representation into a 2D printed board"""
    for x in range(0,len(board)):
        for y in range(0,len(board)):
            if(board[x] != y):
                print("- ", end="")
            else:
                print("o ", end="")
        print("")

def n_queen_solver(n,gen_size,mutation_rate,max_generations, stall_limit,population_init_algorithm):
    """
        Inputs: the size n of the board, generation size, amount of children and ¨
            a number corresponding to which population initlization algorithm to use. 
        Output:
        - a tuple containing a board, how many generations it took to arrive at that board, how many times the fitness function has not improved 
            - The board (list) has fitness == 0 (no conflicts), OR
            - The best board found if we stop due to stagnation.
    """
    # 0) variable init
    generation_num = 0
    
    # 1) Initilize population
    generation = []
    if population_init_algorithm == 0:
        generation = [population_initliziser_random(n) for x in range(gen_size)]
    elif population_init_algorithm == 1:
        generation = [population_initliziser_heuristic(n) for x in range(gen_size)]
    else:
        raise ValueError("The n-queens_solver function has recived invalid population init algorithm number as argument")

    # 2) Evaluate the first generation ONCE:
    # scored = list of (board, fitness(board)) so we don't recompute fitness twice
    scored = [(cand, fitness(cand)) for cand in generation]

    # Early stop: if any board already has fitness 0, return it
    for board, fit in scored:
        if fit == 0:
            return (board, 0, 0)
        
    # Best so far from the start generation  
    best_board, best_fitness = min(scored, key=lambda t: t[1])

    # 3) Stagnation tracking:
    # If fitness does not improve for many generations, we stop.
    stall = 0

    # 4) GA main loop: select → recombine → mutate → evaluate → check stop
    while generation_num < max_generations:
    
        #Select next generation / Check if goal is met
        generation = tournament_select(scored, 3, gen_size)
        #Recombine
        generation.extend(recombine(generation))
        #Printing and testing mutation function
        generation.extend(mutate_extend(generation, mutation_rate))

        # Evaluate the NEW generation ONCE
        scored = [(cand, fitness(cand)) for cand in generation]

        # Current best in this generation
        cur_best_board, cur_best_fitness = min(scored, key=lambda t: t[1]) 

        # Early stop: perfect solution found
        if cur_best_fitness == 0:
            return (cur_best_board, generation_num, stall)
        
        # Update "best so far" and handle stagnation counter
        if cur_best_fitness < best_fitness:
            best_board = cur_best_board
            best_fitness = cur_best_fitness
            stall = 0
        else:
            stall += 1
            if stall >= stall_limit:
                #return (best_board, generation_num, stall)
                return ([], generation_num, stall)
            
        #Increases the generation counter
        generation_num += 1
        
    #Returns configuration that solves problem
    return ([], generation_num, stall)
    
def info_n_queen_solver(itererations, board_size_n, boards_per_generation, mutation_rate, max_generations, stall_limit, ignore_failed_attempts, pop_init_algorithm, print_to_file, txt_file_name):
    solutions_found = []
    generations_taken = []
    time_taken = []
    exceeded_max_generation_count = 0
    exceeded_stall_limit_count = 0
    success_counter = 0
    
    for i in range(itererations):
        start_time = time.process_time()
        solution_found = (n_queen_solver(board_size_n, boards_per_generation, mutation_rate, max_generations, stall_limit, pop_init_algorithm))
        end_time = time.process_time()
        
        #If the function should include runs which failed to find a solution when gathering data about time and generations taken.
        if ignore_failed_attempts:
            if(solution_found[1] < max_generations and solution_found[2] < stall_limit):
                solutions_found.append(solution_found[0])
                generations_taken.append(solution_found[1])
                time_taken.append(end_time - start_time)
                print(f"Iteration: {i} - success")
                success_counter += 1
            else:
                if(solution_found[1] >= max_generations and solution_found[2] >= stall_limit):
                    print(f"Iteration: {i} - Stopped search due to exceeding both max generations and stall limit")
                    exceeded_max_generation_count += 1
                    exceeded_stall_limit_count += 1
                elif(solution_found[1] >= max_generations):
                    print(f"Iteration: {i} - Stopped search due to exceeding max generations")
                    exceeded_max_generation_count += 1
                else:
                    print(f"Iteration: {i} - Stopped search due to fitness function not improving for {stall_limit} generations")
                    exceeded_stall_limit_count += 1
        else:
            #only add solution candidate if it actually contains a solution
            if len(solution_found[0]) > 0:
                solutions_found.append(solution_found[0])
                
            generations_taken.append(solution_found[1])
            time_taken.append(end_time - start_time)
            if(solution_found[1] < max_generations and solution_found[2] < stall_limit):
                print(f"Iteration: {i} - success")
                success_counter += 1
            else:
                if(solution_found[1] >= max_generations and solution_found[2] >= stall_limit):
                    print(f"Iteration: {i} - Stopped search due to exceeding both max generations and stall limit")
                    exceeded_max_generation_count += 1
                    exceeded_stall_limit_count += 1
                elif(solution_found[1] >= max_generations):
                    print(f"Iteration: {i} - Stopped search due to exceeding max generations")
                    exceeded_max_generation_count += 1
                else:
                    print(f"Iteration: {i} - Stopped search due to fitness function not improving for {stall_limit} generations")
                    exceeded_stall_limit_count += 1
        
    if len(solution_found[0]) > 0:
        print_board(solution_found[0])
    print("General info:")
    print(f"Size of board:                    {board_size_n}")
    print(f"Boards selected each generation:  {boards_per_generation}")
    print(f"Children created each generation: {boards_per_generation}")
    print(f"Mutation rate:                    {mutation_rate}")
    print(f"Number of iterations:             {itererations}")
    print(f"Pop initilization algorithm:      {pop_init_algorithm}")
    print(f"Max generations:                  {max_generations}")
    print(f"Times max generation was reached: {exceeded_max_generation_count}")
    print(f"Stall limit:                      {stall_limit}")
    print(f"Times stall limit was exceeded:   {exceeded_stall_limit_count}")
    print(f"Succeded {success_counter} / {itererations} times\n")

    print("Generations summary:")
    print(f"Least generations taken:\t{min(generations_taken)}")
    print(f"Most generations taken: \t{max(generations_taken)}")
    print(f"Average number of generations:\t{sum(generations_taken) / len(generations_taken)}")
    print(f"Median of list: \t\t{statistics.median(generations_taken)}\n")

    print("Time for whole algorithm summary:")
    print(f"Least time taken:             {min(time_taken)}")
    print(f"Most time taken:              {max(time_taken)}")
    print(f"Average amount of time taken: {sum(time_taken) / len(time_taken)}")
    print(f"Median time taken:            {statistics.median(time_taken)}")
    
    #prints to file
    if print_to_file:
        with open(txt_file_name, "a") as f:
            with redirect_stdout(f):
                if len(solution_found[0]) > 0:
                    print_board(solution_found[0])
                print("General info:")
                print(f"Size of board:                    {board_size_n}")
                print(f"Boards selected each generation:  {boards_per_generation}")
                print(f"Children created each generation: {boards_per_generation}")
                print(f"Mutation rate:                    {mutation_rate}")
                print(f"Number of iterations:             {itererations}")
                print(f"Pop initilization algorithm:      {pop_init_algorithm}")
                print(f"Max generations:                  {max_generations}")
                print(f"Times max generation was reached: {exceeded_max_generation_count}")
                print(f"Stall limit:                      {stall_limit}")
                print(f"Times stall limit was exceeded:   {exceeded_stall_limit_count}")
                print(f"Succeded {success_counter} / {itererations} times\n")

                print("Generations summary:")
                print(f"Least generations taken:\t{min(generations_taken)}")
                print(f"Most generations taken: \t{max(generations_taken)}")
                print(f"Average number of generations:\t{sum(generations_taken) / len(generations_taken)}")
                print(f"Median of list: \t\t{statistics.median(generations_taken)}\n")

                print("Time for whole algorithm summary:")
                print(f"Least time taken:             {min(time_taken)}")
                print(f"Most time taken:              {max(time_taken)}")
                print(f"Average amount of time taken: {sum(time_taken) / len(time_taken)}")
                print(f"Median time taken:            {statistics.median(time_taken)}")
        
        
        
    
    if len(solutions_found) > 0:
        return (solutions_found, generations_taken, time_taken, success_counter)
    else:
        return ([], generations_taken, time_taken, success_counter)
    


if __name__ == "__main__":
    #Parameters
    itererations = 500
    board_size_n = 50
    boards_per_generation = 768
    mutation_rate = 50
    max_generations = 2000
    #used for calibration to check if two values are close enough to be considered equal if the difference is less than the stop tolerance
    stop_tolerence = 0.01
    #if the fitness function does not improve within the stall_limit then the algorithm will halt
    stall_limit = 500
    #If the info_n_queen_solver() should count failed attempts at reaching a solution when printing and returning the time and generational values
    ignore_failed_attempts = False
    #0 makes the solver use a shuffled board from 0 to n-1, while a 1 makes the solver use a heuristic function to generate the initial boards
    pop_init_algorithm = 1 
    #if to tune the initial variables to call info_n_queen_solver() with
    tuning = False
    #if to print to file
    print_to_file = False
    txt_file_name = "results.txt"


    if tuning:
        #calibration
        print("\nBeginning tuning")
        boards_per_generation   = gen_size_tuner(board_size_n, boards_per_generation,pop_init_algorithm, mutation_rate, max_generations, stall_limit, stop_tolerence, itererations, ignore_failed_attempts, n_queen_solver)
        mutation_rate           = mutation_rate_tuner_2(board_size_n, boards_per_generation,pop_init_algorithm, mutation_rate, max_generations, stall_limit, stop_tolerence*10, itererations, ignore_failed_attempts, n_queen_solver)
        print("Tuning finished")
    
    #solution = n_queen_solver(4, 100, 100, 0)
    open(txt_file_name, "w").close()
    solution = info_n_queen_solver(itererations, board_size_n, boards_per_generation, mutation_rate, max_generations, stall_limit, ignore_failed_attempts, pop_init_algorithm, print_to_file, txt_file_name)