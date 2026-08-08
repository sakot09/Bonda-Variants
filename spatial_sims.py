from main import compute_borda_scores, get_ranking, format_to_colley
from colley_matrix import colley_matrix, win_loss, b_values, borda_colley_scores, colley_ranking
import random
import copy
import math

NUM_SIMULATIONS = 10000
VOTERS = 1001

def spatial_model(candidates):

    ompm_rank = ompm_win = 0
    omavg_rank = omavg_win = 0
    pmavg_rank = pmavg_win = 0
    ommbc_rank = ommbc_win = 0
    pmmbc_rank = pmmbc_win = 0
    avgmbc_rank = avgmbc_win = 0
    colleyom_rank = colleyom_win = 0
    colleypm_rank = colleypm_win = 0
    colleyavg_rank = colleyavg_win = 0
    colleymbc_rank = colleymbc_win = 0

    for _ in range(NUM_SIMULATIONS):
        labels = [chr(65 + i) for i in range(candidates)]
        assigned = []

        for i in range(len(labels)):
            assigned_pt = random.gauss(0,1)
            assigned.append(assigned_pt)

        candidate_distribution = dict(zip(labels, assigned))

        voting_dist = dict()

        for i in range(VOTERS):

            voter_pt = random.gauss(0,1)

            ranked = sorted(labels, key=lambda c: abs(voter_pt - candidate_distribution[c]))
            ballot = "".join(ranked)

            if ballot in voting_dist:
                voting_dist[ballot]+=1
            else:
                voting_dist[ballot] = 1

        om_scores, pm_scores, avg_scores, mbc_scores = compute_borda_scores_from_profile(voting_dist, candidates)

        om_rank    = get_ranking(om_scores)
        pm_rank    = get_ranking(pm_scores)
        avg_rank   = get_ranking(avg_scores)
        mbc_rank   = get_ranking(mbc_scores)

        matrix = colley_matrix(voting_dist, candidates)
        wl = win_loss(voting_dist, candidates)
        b = b_values(wl, candidates)
        colley_scores = borda_colley_scores(matrix, b)
        colley_rank = colley_ranking(colley_scores, candidates)

        if om_rank != pm_rank:             ompm_rank += 1
        if om_rank[0] != pm_rank[0]:       ompm_win += 1

        if om_rank != avg_rank:            omavg_rank += 1
        if om_rank[0] != avg_rank[0]:      omavg_win += 1

        if pm_rank != avg_rank:            pmavg_rank += 1
        if pm_rank[0] != avg_rank[0]:      pmavg_win += 1

        if om_rank != mbc_rank:            ommbc_rank += 1
        if om_rank[0] != mbc_rank[0]:      ommbc_win += 1

        if pm_rank != mbc_rank:            pmmbc_rank += 1
        if pm_rank[0] != mbc_rank[0]:      pmmbc_win += 1

        if avg_rank != mbc_rank:           avgmbc_rank += 1
        if avg_rank[0] != mbc_rank[0]:     avgmbc_win += 1

        if colley_rank != om_rank:         colleyom_rank += 1
        if colley_rank[0] != om_rank[0]:   colleyom_win += 1

        if colley_rank != pm_rank:         colleypm_rank += 1
        if colley_rank[0] != pm_rank[0]:   colleypm_win += 1

        if colley_rank != avg_rank:        colleyavg_rank += 1
        if colley_rank[0] != avg_rank[0]:  colleyavg_win += 1

        if colley_rank != mbc_rank:        colleymbc_rank += 1
        if colley_rank[0] != mbc_rank[0]:  colleymbc_win += 1


    print(f"\n=== {candidates} Candidates, {VOTERS} Voters, {NUM_SIMULATIONS} Simulations ===")
    print(f"{'Comparison':<20} | {'Ranking differs':>15} | {'Winner differs':>14}")
    print(f"{'-'*20}-+-{'-'*15}-+-{'-'*14}")
    print(f"{'OM vs PM':<20} | {ompm_rank:>15} | {ompm_win:>14}")
    print(f"{'OM vs Avg':<20} | {omavg_rank:>15} | {omavg_win:>14}")
    print(f"{'OM vs MBC':<20} | {ommbc_rank:>15} | {ommbc_win:>14}")
    print(f"{'PM vs Avg':<20} | {pmavg_rank:>15} | {pmavg_win:>14}")
    print(f"{'PM vs MBC':<20} | {pmmbc_rank:>15} | {pmmbc_win:>14}")
    print(f"{'Avg vs MBC':<20} | {avgmbc_rank:>15} | {avgmbc_win:>14}")
    print(f"{'Colley vs OM':<20} | {colleyom_rank:>15} | {colleyom_win:>14}")
    print(f"{'Colley vs PM':<20} | {colleypm_rank:>15} | {colleypm_win:>14}")
    print(f"{'Colley vs Avg':<20} | {colleyavg_rank:>15} | {colleyavg_win:>14}")
    print(f"{'Colley vs MBC':<20} | {colleymbc_rank:>15} | {colleymbc_win:>14}")       

def compute_borda_scores_from_profile(profile, candidates):
    labels = [chr(65 + i) for i in range(candidates)]

    om_scores  = {c: 0 for c in labels}
    pm_scores  = {c: 0 for c in labels}
    avg_scores = {c: 0.0 for c in labels}
    mbc_scores = {c: 0 for c in labels}

    for ballot, count in profile.items():
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

        for i, c in enumerate(ranked):
            mbc_scores[c] += count * (num_ranked - i)

    return om_scores, pm_scores, avg_scores, mbc_scores
    
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


spatial_model(4)

