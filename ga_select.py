import random

## Count diagonal conflicts only (rows/cols are unique by representation)
def fitness(board): 
    conflicts = 0
    n = len(board)
    for i in range(n):
        for j in range (i + 1, n):
            # Same diagonal if row diff == column diff
            if abs(i - j) == abs(board[i] - board[j]):
                conflicts += 1
    return conflicts 


def select(generation):
    # Elitism: sort by fitness (lower is better)
    rank = sorted(generation, key = fitness)
    # Keep best 50% (at least 2)
    parents = rank[:max(2, len(rank)//2)]
    return parents

def tournament_select(generation, tournament_size=3, parents_count=None):
    # Default: keep half (at least 2)
    if parents_count is None:
        parents_count = max(len(generation)//2,2)

        parents = []
        for _ in range(parents_count):
            # Pick random candidates (no repeats within the tournament)
            candidates = random.sample(generation, min(tournament_size, len(generation)))
            # Winner = lowest fitness
            winner = min(candidates, key=fitness)
            parents.append(winner)
        return parents
    


