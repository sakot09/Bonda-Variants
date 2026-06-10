import random
from itertools import permutations, combinations

def getCombinations(candidates):
    labels = [chr(65 + i) for i in range(candidates)]  
    all_combos = []

    for winner in labels:
        others = [c for c in labels if c != winner]
        for slots in range(0, candidates - 1):
            if slots == 0:
                all_combos.append(winner)
            else:
                for subset in combinations(others, slots):
                    for perm in permutations(subset):
                        all_combos.append(winner + "".join(perm))

    return all_combos

def numCombinations(candidates):
    others = candidates - 1
    total = 0
    
    for slots in range(0, candidates - 1):
        ways = 1
        for i in range(others, others - slots, -1):
            ways *= i
        total += ways
    
    return total*candidates

def sample_integer_simplex(n, k):
    bars = sorted(random.sample(range(n + k - 1), k - 1))
    extended = [-1] + bars + [n + k - 1]
    return [extended[i+1] - extended[i] - 1 for i in range(k)]

def compute_borda_scores(candidates, combos, voter_counts):
    
    labels = [chr(65 + i) for i in range(candidates)]
    
    om_scores  = {c: 0 for c in labels}
    pm_scores  = {c: 0 for c in labels}
    avg_scores = {c: 0.0 for c in labels}

    for ballot, count in zip(combos, voter_counts):
        if count == 0:
            continue

        ranked = list(ballot)  
        unranked = [c for c in labels if c not in ranked]
        num_ranked = len(ranked)
        num_unranked = len(unranked)
        om_unranked_pts = (candidates - 1) - num_ranked  

        for i, c in enumerate(ranked):
            om_scores[c] += count * ((candidates - 1) - i)
        for c in unranked:
            om_scores[c] += count * om_unranked_pts

        
        for i, c in enumerate(ranked):
            pm_scores[c] += count * ((candidates - 1) - i)

        remaining_pts = sum((candidates - 1) - (num_ranked + j) for j in range(num_unranked))
        avg_unranked_pts = (remaining_pts / num_unranked) if num_unranked > 0 else 0

        for i, c in enumerate(ranked):
            avg_scores[c] += count * ((candidates - 1) - i)
        for c in unranked:
            avg_scores[c] += count * avg_unranked_pts

    return om_scores, pm_scores, avg_scores

def print_profile(candidates, voters, combos, voter_counts):
    print(f"\n--- Voter Profile ({candidates} candidates, {voters} voters) ---")
    print(f"{'Preference':<12} | {'Voters':>6}")
    print(f"{'-'*12}-+-{'-'*6}")
    for pref, count in zip(combos, voter_counts):
        print(f"{pref:<12} | {count:>6}")
    print(f"{'-'*12}-+-{'-'*6}")
    print(f"{'Total':<12} | {sum(voter_counts):>6}")

def print_scores(candidates, om_scores, pm_scores, avg_scores):
    labels = [chr(65 + i) for i in range(candidates)]
    print(f"\n--- Borda Scores ---")
    print(f"{'Candidate':<10} | {'OM':>8} | {'PM':>8} | {'Avg':>8}")
    print(f"{'-'*10}-+-{'-'*8}-+-{'-'*8}-+-{'-'*8}")
    for c in labels:
        print(f"{c:<10} | {om_scores[c]:>8} | {pm_scores[c]:>8} | {avg_scores[c]:>8.2f}")

def get_ranking(scores):
    return sorted(scores, key=lambda c: scores[c], reverse=True)



