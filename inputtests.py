from main import *

candidates = int(input("Enter number of candidates: "))
voters = int(input("Enter number of voters: "))

if (candidates < 1 or voters < 1):
    print("Unable to execute")
    exit()

combos = getCombinations(candidates)
k = numCombinations(candidates)
voter_counts = sample_integer_simplex(voters, k)

om, pm, avg, mbc = compute_borda_scores(candidates, combos, voter_counts)
print_profile(candidates, voters, combos, voter_counts)

print_scores(candidates, om, pm, avg)