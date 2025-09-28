import random
from collections import Counter
import itertools


def pop_init(n):
    return [x for x in range(n)]

def select(generations, gen_size):
    new_generation = []
    while len(new_generation) < gen_size or len(generations) == 0:
        new_generation.append(generations.pop(random.randint(len(generations)-1)))
    
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
        new_generation.append(recombine(generation[random.randint(len(generation))], generation[random.randint(len(generation))]))
    
    return new_generation


def mutate(board, mutation_rate):
    if(random.randint(0, 100) < mutation_rate):
        idx = random.randint(0, len(board))
        
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
    for key, value in dict(counted_boards_nums):
        conflicts += value-1

    return conflicts 

def base_n_queen_solver(n, gen_size, child_gen_size, mutation_rate):
    solution_Found = False
    generation_num = 0
    
    #pop init
    generation = [pop_init(n) for _ in range(gen_size)]
    
    while not solution_Found:
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
        
        generation += 1
        
    #Returns configuration that solves problem
    return (solution, generation_num)