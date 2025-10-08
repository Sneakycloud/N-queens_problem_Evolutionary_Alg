import random

def mutate(generation, mutation_rate):
    """Mutates the generation by swapping two random positions"""
    # Loop through each individual in the generation
    for i in range(len(generation)):
        # Decide whether to mutate this individual
        rand_num : int = random.randint(0, 100)
        if rand_num <= mutation_rate:
            # Swap two random positions in the individual
            one = random.randint(0, len(generation[i]) - 1)
            two = random.randint(0, len(generation[i]) - 1)
            generation[i][one], generation[i][two] = generation[i][two], generation[i][one]
    # Return the mutated generation
    return generation

def mutate_extend(generation, mutation_rate):
    """Mutates the generation by swapping two random positions"""
    mutated_boards = []
    
    # Loop through each individual in the generation
    for i in range(len(generation)):
        # Decide whether to mutate this individual
        rand_num : int = random.randint(0, 100)
        if rand_num <= mutation_rate:
            new_board = generation[i].copy()
            
            # Swap two random positions in the individual
            one = random.randint(0, len(generation[i]) - 1)
            two = random.randint(0, len(generation[i]) - 1)
            new_board[one], new_board[two] = new_board[two], new_board[one]
            
            mutated_boards.append(new_board)
            
    # Return the mutated generation
    return mutated_boards