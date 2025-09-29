import random
import time
import itertools
import statistics
from collections import Counter

itererations = 50
board_size_n = 8
boards_per_generation = 1000
children_per_generation = 1000
mutation_rate = 40
ignore_failed_attempts = False
max_generations = 2000

#converts the ordered representation into a 2D printed board
def print_board(board):
    for x in range(0,len(board)):
        for y in range(0,len(board)):
            if(board[x] != y):
                print("- ", end="")
            else:
                print("o ", end="")
        print("")

def pop_init(n):
    return [x for x in range(n)]

def select(generations, gen_size):
    new_generation = []
    while len(new_generation) < gen_size or len(generations) == 0:
        new_generation.append(generations.pop(random.randint(0,len(generations)-1)))
    
    return new_generation

def recombine(board_1, board_2):
    new_board = []
    
    #randomly select a idx in first list length
    interval_start_idx = random.randint(0, len(board_1)-1)
    
    #randomly select a idx equal or later in list
    interval_stop_idx = random.randint(interval_start_idx, len(board_1)-1)
    
    #take first part of second list
    new_board.extend(board_2[:interval_start_idx])
    
    #take interval of first list
    new_board.extend(board_1[interval_start_idx:interval_stop_idx])
    
    #take rest of second list
    new_board.extend(board_2[interval_stop_idx:])
    
    return new_board

def recombine_generation(generation, child_gen_size):
    new_generation = []
    while len(new_generation) < child_gen_size:
        new_generation.append(recombine(generation[random.randint(0,len(generation)-1)], generation[random.randint(0,len(generation)-1)]))
    
    return new_generation


def mutate(board, mutation_rate):
    if(random.randint(0, 100) < mutation_rate):
        idx = random.randint(0, len(board)-1)
        
        #add one if within bounds
        if(random.randint(0,1) == 1):
            if(board[idx] + 1 < len(board)):
                board[idx] += 1
                return board
        #subtract one if within bounds
        else:
            if(board[idx] - 1 >= 0):
                board[idx] -= 1
                return board

    #if it either did not select for mutation, or the new idx were to be outside bounds
    return board

## Counts all conflicts
def fitness(board): 
    conflicts = 0
    
    #diagonals
    n = len(board)
    for i in range(n):
        for j in range (i + 1, n):
            # Same diagonal if row diff == column diff
            if abs(i - j) == abs(board[i] - board[j]):
                conflicts += 1
                
    #columns
    counted_boards_nums = Counter(board)
    diction = dict(counted_boards_nums)
    for key, value in diction.items():
        conflicts += int(value-1)

    return conflicts 

def base_n_queen_solver(n, gen_size, child_gen_size, mutation_rate, max_generations):
    solution_Found = False
    solution = []
    generation_num = 0
    
    #pop init
    generation = [pop_init(n) for _ in range(gen_size)]
    
    while not solution_Found and generation_num < max_generations:
        #Runs generation and sorts based on fitness
        generation.sort(reverse=False, key=fitness)
        #Removes duplicate entries
        generation = list(generation for generation,_ in itertools.groupby(generation))
        
        #Checks if goal is met
        if fitness(generation[0]) == 0:
            solution_Found = True
            solution = generation[0]
            break
    
        #recombine()
        generation.extend(recombine_generation(generation, child_gen_size))
        
        #mutate()
        generation = [mutate(board, mutation_rate) for board in generation]
        
        #select()
        generation = select(generation, gen_size)
        
        generation_num += 1
        
    #Returns configuration that solves problem
    return (solution, generation_num)

def info_base_n_queen_solver():
    solutions_found = []
    generations_taken = []
    time_taken = []
    for i in range(itererations):
        start_time = time.process_time()
        solution_found = (base_n_queen_solver(board_size_n, boards_per_generation,children_per_generation, mutation_rate, max_generations))
        end_time = time.process_time()
        
        if ignore_failed_attempts:
            if(solution_found[1] < max_generations):
                solutions_found.append(solution_found[0])
                generations_taken.append(solution_found[1])
                time_taken.append(end_time - start_time)
                print(f"Iteration: {i} - success")
            else:
                print(f"Iteration: {i} - failed to find")
        else:
            solutions_found.append(solution_found[0])
            generations_taken.append(solution_found[1])
            time_taken.append(end_time - start_time)
            if(solution_found[1] < max_generations):
                print(f"Iteration: {i} - success")
            else:
                print(f"Iteration: {i} - failed to find")
        
    if len(solution_found[0]) > 0:
        print_board(solution_found[0])
    print("General info:")
    print(f"Size of board:                    {board_size_n}")
    print(f"Boards selected each generation:  {boards_per_generation}")
    print(f"Children created each generation: {children_per_generation}")
    print(f"Mutation rate:                    {mutation_rate}")
    print(f"Number of iterations:             {itererations}")

    print("Generations summary:")
    print(f"Least generations taken:\t{min(generations_taken)}")
    print(f"Most generations taken: \t{max(generations_taken)}")
    print(f"Average number of generations:\t{sum(generations_taken) / len(generations_taken)}")
    print(f"Median of list: \t\t{statistics.median(generations_taken)}")

    print("Time for whole algorithm summary:")
    print(f"Least time taken:             {min(time_taken)}")
    print(f"Most time taken:              {max(time_taken)}")
    print(f"Average amount of time taken: {sum(time_taken) / len(time_taken)}")
    print(f"Median time taken:            {statistics.median(time_taken)}")
    return


info_base_n_queen_solver()

"""
Result of one run:

failed to find for 1/50

General info:
Size of board:                    8
Boards selected each generation:  1000
Children created each generation: 1000
Mutation rate:                    40
Number of iterations:             50
Generations summary:
Least generations taken:        166
Most generations taken:         2000 #this is the maximum allowed, which means a run has failed
Average number of generations:  620.28
Median of list:                 593.0
Time for whole algorithm summary:
Least time taken:             1.28125
Most time taken:              15.328125
Average amount of time taken: 4.6703125
Median time taken:            4.5703125
"""