# Advent of Code 2023 - day 9

# %% Imports
from common import get_input

# %% Part 1
def main():
    sequences = get_sequences_from_input('input09.txt')
    predictions_sum = 0
    for sequence in sequences:
        pred = get_next(sequence)
        predictions_sum += pred
    print(f'Answer: The sum of the predictions is {predictions_sum}')

def get_sequences_from_input(input_path):
    input_data = get_input(input_path)
    return [[int(i) for i in line.split(' ')] for line in input_data]

def sequence_diff(sequence):
    diff = []
    for i in range(len(sequence) - 1):
        diff.append(sequence[i+1] - sequence[i])
    return diff

def get_next(sequence):
    last_value = sequence[-1]
    diff = sequence_diff(sequence)
    if all([i == 0 for i in diff]):
        return last_value + 0
    else:
        return last_value + get_next(diff)

main()

# %% Part 2
def main2():
    sequences = get_sequences_from_input('input09.txt')
    extrapolation_sum = 0
    for sequence in sequences:
        back_extrapolation = get_previous(sequence)
        extrapolation_sum += back_extrapolation
    print(f'Answer: The sum of the back extrapolations is {extrapolation_sum}')

def get_previous(sequence):
    first_value = sequence[0]
    diff = sequence_diff(sequence)
    if all([i == 0 for i in diff]):
        return first_value - 0
    else:
        return first_value - get_previous(diff)

main2()