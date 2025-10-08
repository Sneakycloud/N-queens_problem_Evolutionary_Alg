import random

def recombine(gen):
    """Devide and recombine boards"""
    gen2 = []
    size = len(gen[0])

    # Combine with next board
    for i in range(0, len(gen)):
        # Last combine with first
        if i < len(gen)-1:
            next = i+1
        else:
            next = 0
        
        # Combine and repair boards and add them to gen2
        gen2.append(repair(gen[i][0:round((size/2))], gen[next][round((size/2)):size], size))
        gen2.append(repair(gen[next][0:round((size/2))], gen[i][round((size/2)):size], size))

    return gen2

def repair(first, second, size):
    """Repair reocuring numbers with missing numbers"""
    missing = list(set(range(0, size)) - set(first + second))
    repeating = list(set(second) - (set(range(0, size)) - set(first)))

    # Replace
    for index, value in enumerate(repeating):
        second[second.index(value)] = missing[index]

    return first + second