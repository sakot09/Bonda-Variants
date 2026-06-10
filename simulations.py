from main import getCombinations, numCombinations, sample_integer_simplex, compute_borda_scores, print_scores

candidates = 4
voters = 501

combos = getCombinations(candidates)
k = numCombinations(candidates)

for i in range(10):

    voter_counts = sample_integer_simplex(voters, k)

    om, pm, avg = compute_borda_scores(candidates, combos, voter_counts)
    

    print_scores(candidates, om, pm, avg)