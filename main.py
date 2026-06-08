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

candidates = int(input("Enter number of candidates: "))
voters = int(input("Enter number of voters: "))

if (candidates < 1 or voters < 1):
    print("Unable to execute")
    exit()

combos = getCombinations(candidates)
k = numCombinations(candidates)
voter_counts = sample_integer_simplex(voters, k)

print(f"\n--- Voter Profile ({candidates} candidates, {voters} voters) ---")
print(f"{'Preference':<12} | {'Voters':>6}")
print(f"{'-'*12}-+-{'-'*6}")
for pref, count in zip(combos, voter_counts):
    print(f"{pref:<12} | {count:>6}")
print(f"{'-'*12}-+-{'-'*6}")
print(f"{'Total':<12} | {sum(voter_counts):>6}")