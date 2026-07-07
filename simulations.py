from main import getCombinations, numCombinations, sample_integer_simplex, compute_borda_scores, get_ranking, format_to_colley
from colley_matrix import colley_matrix, win_loss, b_values, borda_colley_scores, colley_ranking
from convert_csv import convert

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


for candidates in [3, 4, 5]:
    run_simulations(candidates, VOTERS, NUM_SIMULATIONS)

run_real_data(INPUT_FILE)