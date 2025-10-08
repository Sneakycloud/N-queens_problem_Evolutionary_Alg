import random

def fitness(board): 
    """Count diagonal conflicts only (rows/cols are unique by representation)"""
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

def tournament_select(scored, tournament_size=3, parents_count=None):
    """
    Select parents via tournament using precomputed fitness.

    Args:
        scored: list of (candidate, fitness) pairs.
        tournament_size: competitors per tournament.
        parents_count: number of parents to return (default: half the population, min 2).

    Returns:
        List of selected candidates.
    """
    # Default: keep half (at least 2)
    n = len(scored)
    if parents_count is None:
        parents_count = max(n// 2, 2)

    parents = []
    for _ in range(parents_count):
        # Pick random candidates (no repeats within the tournament)
        candidate_idxs = random.sample(range(n), min(tournament_size, n))
        # Winner = lowest fitness
        winner_idx = min(candidate_idxs, key= lambda i: scored[i][1])
        # Store only the candidate (genotype), not its fitness
        parents.append(scored[winner_idx][0])
    return parents
    


