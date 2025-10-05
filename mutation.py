import random

# Mutates the generation by swapping two random positions
def mutate(generation, mutation_rate):
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
