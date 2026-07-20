import csv
from collections import Counter
from main import compute_borda_scores, print_scores

INPUT_FILE = "Lehi_20211102_CityCouncil.csv"
SPECIAL_TOKENS = {"skipped", "overvote", "undervote", ""}


def load_raw_ballots(path):
    with open(path, newline="") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    return rows


def build_candidate_mapping(rows):
    seen = []
    for row in rows:
        for cell in row[1:]:
            if cell not in SPECIAL_TOKENS and cell not in seen:
                seen.append(cell)
    mapping = {name: chr(65 + i) for i, name in enumerate(seen)}
    return mapping


def ballot_to_string(row, mapping):
    ranked_letters = []
    seen_letters = set()

    for cell in row[1:]:
        if cell in SPECIAL_TOKENS:
            break

        letter = mapping[cell]
        if letter in seen_letters:
            return None
        seen_letters.add(letter)
        ranked_letters.append(letter)

    if not ranked_letters:
        return None

    return "".join(ranked_letters)


def convert(path):
    rows = load_raw_ballots(path)
    mapping = build_candidate_mapping(rows)

    ballot_counts = Counter()
    discarded = 0

    for row in rows:
        ballot = ballot_to_string(row, mapping)
        if ballot is None:
            discarded += 1
            continue
        ballot_counts[ballot] += 1

    combos = list(ballot_counts.keys())
    voter_counts = [ballot_counts[c] for c in combos]

    return mapping, combos, voter_counts

if __name__ == "__main__":
    mapping, combos, voter_counts = convert(INPUT_FILE)
    candidates = len(mapping)

    om, pm, avg, mbc = compute_borda_scores(candidates, combos, voter_counts)

    print_scores(candidates, om, pm, avg)