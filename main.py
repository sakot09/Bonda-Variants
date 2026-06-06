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

def arrangeVoters(candidates):
    remainingVoters = 501
    remainingCandidates = candidates - 1

    profile = []

    for i in range(candidates-1):
        chosen = random.randint(1, remainingVoters-remainingCandidates)
        remainingVoters-=chosen
        remainingCandidates-=1
        profile.append(chosen)
    profile.append(remainingVoters)
    return profile

candidates = int(input("Enter number of candidates: "))

arrange = arrangeVoters(candidates)
numCombos = numCombinations(candidates)
assigned = []
combos = getCombinations(candidates)
for i in range(len(arrange)):
    chosen = random.randint(0,numCombos)
    assigned.append(combos[chosen])


print(f"\n--- Voter Profile ({candidates} candidates, 501 voters) ---")
print(f"{'Preference':<12} | {'Voters':>6}")
print(f"{'-'*12}-+-{'-'*6}")
for i in range(len(arrange)):
        print(f"{assigned[i]:<12} | {arrange[i]:>6}")
print(f"{'-'*12}-+-{'-'*6}")
print(f"{'Total':<12} | {'501':>6}")