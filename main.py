import random
from pop_init import population_initliziser_random, population_initliziser_heuristic

#converts the ordered representation into a 2D printed board
def print_board(board):
    for x in range(0,len(board)):
        for y in range(0,len(board)):
            if(board[x] != y):
                print("O", end="")
            else:
                print("X", end="")
        print("")



#Inputs: the size n of the board, generation size, amount of children and a number corresponding to which population initlization algorithm to use
#Output: a solution to the n-queens problem
def n_queen_solver(n,gen_size,amount_children,population_init_algorithm):
    solution_Found = False

    #consider if solution and rank should be combined into a tuple?
    solution = []
    rank = []
    
    #Initilize population
    generation = []
    if population_init_algorithm == 0:
        generation = [population_initliziser_random(n) for x in range(gen_size)]
    elif population_init_algorithm == 1:
        generation = [population_initliziser_heuristic(n) for x in range(gen_size)]
    else:
        raise ValueError("The n-queens_solver function has recived invalid population init algorithm number as argument")

    #Check if goal is met with initial population

    #Generational loop
    #while not solution_Found:
        #evalutate fittness function and test  
        #Select next generation / Check if goal is met
        generation = select(generation)
        #Recombine
        generation = recombine(generation, amount_children) 
        #Mutate
        generation = mutate(generation)

    #printing for testing purposes
    print_board(generation[0])


    #Returns configuration that solves problem
    return solution
    
    
solution = n_queen_solver(15, 100,100,0)