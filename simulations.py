from main import getCombinations, numCombinations, sample_integer_simplex, compute_borda_scores, get_ranking, format_to_colley
from colley_matrix import colley_matrix, win_loss, b_values, borda_colley_scores, colley_ranking
import random
from convert_csv import convert
import copy

NUM_SIMULATIONS = 1000
VOTERS = 1001
INPUT_FILE = "Genola_20211102_CityCouncil.csv"


def run_simulations(candidates, voters, num_simulations):
    combos = getCombinations(candidates)
    k = numCombinations(candidates)

    ompm_rank = ompm_win = 0
    omavg_rank = omavg_win = 0
    pmavg_rank = pmavg_win = 0
    colleyom_rank = colleyom_win = 0
    colleypm_rank = colleypm_win = 0
    colleyavg_rank = colleyavg_win = 0

    for _ in range(num_simulations):
        voter_counts = sample_integer_simplex(voters, k)
        profile = format_to_colley(combos, voter_counts)

        om, pm, avg = compute_borda_scores(candidates, combos, voter_counts)

        om_rank  = get_ranking(om)
        pm_rank  = get_ranking(pm)
        avg_rank = get_ranking(avg)

        matrix = colley_matrix(profile, candidates)
        wl = win_loss(profile, candidates)
        b = b_values(wl, candidates)
        colley_scores = borda_colley_scores(matrix, b)
        colley_rank = colley_ranking(colley_scores, candidates)

        if om_rank != pm_rank:   ompm_rank += 1
        if om_rank[0] != pm_rank[0]:  ompm_win += 1

        if om_rank != avg_rank:  omavg_rank += 1
        if om_rank[0] != avg_rank[0]: omavg_win += 1

        if pm_rank != avg_rank:  pmavg_rank += 1
        if pm_rank[0] != avg_rank[0]: pmavg_win += 1

        if colley_rank != om_rank:   colleyom_rank += 1
        if colley_rank[0] != om_rank[0]:  colleyom_win += 1

        if colley_rank != pm_rank:   colleypm_rank += 1
        if colley_rank[0] != pm_rank[0]:  colleypm_win += 1

        if colley_rank != avg_rank:  colleyavg_rank += 1
        if colley_rank[0] != avg_rank[0]: colleyavg_win += 1

    print(f"\n=== {candidates} Candidates, {voters} Voters, {num_simulations} Simulations ===")
    print(f"{'Comparison':<20} | {'Ranking differs':>15} | {'Winner differs':>14}")
    print(f"{'-'*20}-+-{'-'*15}-+-{'-'*14}")
    print(f"{'OM vs PM':<20} | {ompm_rank:>15} | {ompm_win:>14}")
    print(f"{'OM vs Avg':<20} | {omavg_rank:>15} | {omavg_win:>14}")
    print(f"{'PM vs Avg':<20} | {pmavg_rank:>15} | {pmavg_win:>14}")
    print(f"{'Colley vs OM':<20} | {colleyom_rank:>15} | {colleyom_win:>14}")
    print(f"{'Colley vs PM':<20} | {colleypm_rank:>15} | {colleypm_win:>14}")
    print(f"{'Colley vs Avg':<20} | {colleyavg_rank:>15} | {colleyavg_win:>14}")


def run_real_data(path):
    mapping, combos, voter_counts = convert(path)
    candidates = len(mapping)
    profile = format_to_colley(combos, voter_counts)

    om, pm, avg = compute_borda_scores(candidates, combos, voter_counts)

    om_rank  = get_ranking(om)
    pm_rank  = get_ranking(pm)
    avg_rank = get_ranking(avg)

    matrix = colley_matrix(profile, candidates)
    wl = win_loss(profile, candidates)
    b = b_values(wl, candidates)
    colley_scores = borda_colley_scores(matrix, b)
    colley_rank = colley_ranking(colley_scores, candidates)

    reverse_map = {v: k for k, v in mapping.items()}

    def named(rank):
        return [reverse_map[c] for c in rank]

    print(f"\n=== Real Data: Lehi City Council ({candidates} candidates) ===")
    print(f"{'Comparison':<20} | {'Ranking differs':>15} | {'Winner differs':>14}")
    print(f"{'-'*20}-+-{'-'*15}-+-{'-'*14}")
    print(f"{'OM vs PM':<20} | {str(om_rank != pm_rank):>15} | {str(om_rank[0] != pm_rank[0]):>14}")
    print(f"{'OM vs Avg':<20} | {str(om_rank != avg_rank):>15} | {str(om_rank[0] != avg_rank[0]):>14}")
    print(f"{'PM vs Avg':<20} | {str(pm_rank != avg_rank):>15} | {str(pm_rank[0] != avg_rank[0]):>14}")
    print(f"{'Colley vs OM':<20} | {str(colley_rank != om_rank):>15} | {str(colley_rank[0] != om_rank[0]):>14}")
    print(f"{'Colley vs PM':<20} | {str(colley_rank != pm_rank):>15} | {str(colley_rank[0] != pm_rank[0]):>14}")
    print(f"{'Colley vs Avg':<20} | {str(colley_rank != avg_rank):>15} | {str(colley_rank[0] != avg_rank[0]):>14}")

    print(f"\nOM ranking:     {named(om_rank)}")
    print(f"PM ranking:     {named(pm_rank)}")
    print(f"Avg ranking:    {named(avg_rank)}")
    print(f"Colley ranking: {named(colley_rank)}")

def find_all_disagree(candidates):
    
    labels = [chr(65 + i) for i in range(candidates)]
    short_combos = labels + [a+b for a in labels for b in labels if a != b]

    found = False

    while not found:
        voter_counts = [random.randint(0, 100) for _ in range(len(short_combos))]
        profile = format_to_colley(short_combos, voter_counts)

        om, pm, avg = compute_borda_scores(candidates, short_combos, voter_counts)
        om_rank    = get_ranking(om)
        pm_rank    = get_ranking(pm)
        avg_rank   = get_ranking(avg)

        matrix = colley_matrix(profile, candidates)
        wl = win_loss(profile, candidates)
        b = b_values(wl, candidates)
        colley_scores = borda_colley_scores(matrix, b)
        colley_rank = colley_ranking(colley_scores, candidates)

        winners = [om_rank[0], pm_rank[0], avg_rank[0], colley_rank[0]]

        if len(set(winners)) == candidates:
            found = True
            print(f"\n=== {candidates} Candidates ===")
            print(f"Profile: {profile}\n")
            print(f"OM winner:     {om_rank[0]}")
            print(f"PM winner:     {pm_rank[0]}")
            print(f"Avg winner:    {avg_rank[0]}")
            print(f"Colley winner: {colley_rank[0]}")
    
def modify_ballot(profile, ballot, candidate):
    p2 = copy.deepcopy(profile)
    p2[ballot] -= 1
    if p2[ballot] == 0:
        del p2[ballot]
    new_ballot = ballot + candidate
    if new_ballot in p2:
        p2[new_ballot] += 1
    else:
        p2[new_ballot] = 1
    return p2

def get_colley_winner(profile, candidates):
    matrix = colley_matrix(profile, candidates)
    wl = win_loss(profile, candidates)
    b = b_values(wl, candidates)
    scores = borda_colley_scores(matrix, b)
    return colley_ranking(scores, candidates)[0]

def test_dominated_power(candidates, voters, num_simulations):
    labels = [chr(65 + i) for i in range(candidates)]
    combos = getCombinations(candidates)
    k = numCombinations(candidates)
    violations = 0

    for _ in range(num_simulations):
        voter_counts = sample_integer_simplex(voters, k)
        profile = format_to_colley(combos, voter_counts)

        winner_p1 = get_colley_winner(profile, candidates)

        ballots_with_unranked = [b for b in profile if profile[b] > 0 and len(b) < candidates]
        if not ballots_with_unranked:
            continue

        ballot = random.choice(ballots_with_unranked)
        unranked = [c for c in labels if c not in ballot]
        candidate_to_add = random.choice(unranked)

        p2 = modify_ballot(profile, ballot, candidate_to_add)
        winner_p2 = get_colley_winner(p2, candidates)

        winner_was_on_ballot = winner_p1 in ballot

        if winner_was_on_ballot and winner_p1 != winner_p2:
            violations += 1

    print(f"\n=== Dominated Power Property Test ({candidates} candidates, {num_simulations} simulations) ===")
    print(f"Violations: {violations}/{num_simulations}")

test_dominated_power(4, VOTERS, NUM_SIMULATIONS)