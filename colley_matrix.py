import numpy as np
import string


def non_diagonal(sample_profile, n, row, column):
    letters = string.ascii_uppercase[:n]
    non_diag = 0
    for key in sample_profile:
        if letters[row] in key or letters[column] in key:
            non_diag += sample_profile[key]
    return -non_diag


def colley_matrix(sample_profile, n):
    letters = string.ascii_uppercase[:n]
    diag = [0] * n
    for key in sample_profile:
        for i in range(n):
            if letters[i] in key:
                diag[i] += (n - 1) * sample_profile[key]
            if letters[i] not in key:
                diag[i] += len(key) * sample_profile[key]
    matrix = []
    for i in range(n):
        row = []
        for j in range(n):
            if j != i:
                row.append(non_diagonal(sample_profile, n, i, j))
            else:
                row.append(diag[i] + 2)
        matrix.append(row)
    return matrix


def win_loss(sample_profile, n):
    letters = string.ascii_uppercase[:n]
    win_loss_record = [0] * n
    for key in sample_profile:
        for i in range(n):
            if letters[i] in key:
                index = key.index(letters[i])
                win_loss_record[i] += sample_profile[key] * (n - 1 - index) - sample_profile[key] * index
            if letters[i] not in key:
                win_loss_record[i] -= sample_profile[key] * len(key)
    return win_loss_record


def b_values(win_loss_record, n):
    return [win_loss_record[i] / 2 + 1 for i in range(n)]


def borda_colley_scores(matrix, b):
    return np.linalg.solve(matrix, b)


def colley_ranking(scores, n):
    letters = string.ascii_uppercase[:n]
    holders = dict(zip(letters, scores))
    return sorted(holders, key=lambda c: holders[c], reverse=True)