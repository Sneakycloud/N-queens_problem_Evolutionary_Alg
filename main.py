import random
from pop_init import population_initliziser_random, population_initliziser_heuristic
from ga_select import fitness, select, tournament_select

#Takes a n-size board and generates a initial state by choosing a random coloumn each row that has not yet been placed in
def population_initliziser_random(n):
    #List of available positions
    Available_coloumn_positions = [x for x in range(0,n)]
    resulting_configuration = []

    #randomly picks a available position to place a queen
    while len(Available_coloumn_positions) > 0:
        resulting_configuration.append(Available_coloumn_positions.pop(random.randint(0,len(Available_coloumn_positions)-1)))

    return resulting_configuration

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
    print("BEFORE | size:", len(generation))
    generation = tournament_select(generation, tournament_size=3)
    print("AFTER  | size:", len(generation), "(expected ≈", max(2, len(generation) // 2), ")")

        #Recombine
        #generation = recombine(generation, amount_children) 
        #Mutate
        #generation = mutate(generation)

    #printing for testing purposes
    print_board(generation[0])
    print(fitness(generation[0]))

    #Returns configuration that solves problem
    return solution
    
    
solution = n_queen_solver(4, 100,100,0)