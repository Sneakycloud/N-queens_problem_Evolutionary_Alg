import random
from pop_init import population_initliziser_random, population_initliziser_heuristic
from ga_select import fitness, select, tournament_select
from mutation import mutate
from recombine import recombine


def population_initliziser_random(n):
    """"""
    #List of available positions
    Available_coloumn_positions = [x for x in range(0,n)]
    resulting_configuration = []

    #randomly picks a available position to place a queen
    while len(Available_coloumn_positions) > 0:
        resulting_configuration.append(Available_coloumn_positions.pop(random.randint(0,len(Available_coloumn_positions)-1)))

    return resulting_configuration

def print_board(board):
    """Converts the ordered representation into a 2D printed board"""
    for x in range(0,len(board)):
        for y in range(0,len(board)):
            if(board[x] != y):
                print("- ", end="")
            else:
                print("o ", end="")
        print("")

def n_queen_solver(n,gen_size,amount_children,population_init_algorithm):
    """
        Inputs: the size n of the board, generation size, amount of children and ¨
            a number corresponding to which population initlization algorithm to use. 
        Output: 
        - A board (list) that has fitness == 0 (no conflicts), OR
        - The best board found if we stop due to stagnation.
    """
    
    
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
            return board
        
    # Best so far from the start generation  
    best_board, best_fitness = min(scored, key=lambda t: t[1])

    # 3) Stagnation tracking:
    # If fitness does not improve for many generations, we stop.
    stall = 0
    STALL_LIMIT = 500

    # 4) GA main loop: select → recombine → mutate → evaluate → check stop
    while True:
    
        #Select next generation / Check if goal is met
        generation = tournament_select([t[0] for t in scored], tournament_size=3)
        #Recombine
        generation = recombine(generation, n)
        #Printing and testing mutation function
        generation = mutate(generation)

        # Evaluate the NEW generation ONCE
        scored = [(cand, fitness(cand)) for cand in generation]

        # Current best in this generation
        cur_best_board, cur_best_fitness = min(scored, key=lambda t: t[1]) 

        # Early stop: perfect solution found
        if cur_best_fitness == 0:
            return cur_best_board
        
        # Update "best so far" and handle stagnation counter
        if cur_best_fitness < best_fitness:
            best_board = cur_best_board
            best_fitness = cur_best_fitness
            stall = 0
        else:
            stall += 1
            if stall >= STALL_LIMIT:
                return best_board
    
    
solution = n_queen_solver(4, 100, 100, 0)
print_board(solution)
