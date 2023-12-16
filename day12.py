# Advent of Code 2023 - day 12

# %% Imports
from common import get_input
import re
from itertools import combinations

# %% Part 1
# Note: Part 1 was implemented before part 2, and uses more of a "brute force" solution.
# The same method as in part 2 could of course be used also for part 1 for higher efficiency.

def main():
    input_data = get_input('input12.txt')
    num_arrangements = []
    for line in input_data:
        row, spec = line.split(' ')
        spec = spec.split(',')
        spec = [int(i) for i in spec]
        possible_allowed_rows = []
        for r in possible_rows(row, spec):
            if satisfies_spec(r, spec):
                possible_allowed_rows.append(r)
        num_arrangements.append(len(possible_allowed_rows))
    print(f'Answer: The sum of the number of arrangements for each row is {sum(num_arrangements)}')

def groups_of_damaged_in_row(row):
    row = row.replace('.', ' ')
    row = row.replace('?', ' ').strip()
    row = re.sub(' +', ' ', row)
    groups = row.split(' ')
    return [len(group) for group in groups]

def groups_of_unknown_in_row(row):
    row = row.replace('.', ' ')
    row = row.replace('#', ' ').strip()
    row = re.sub(' +', ' ', row)
    groups = row.split(' ')
    return [len(group) for group in groups]

def satisfies_spec(row, spec):
    groups = groups_of_damaged_in_row(row)
    if not len(spec) == len(groups):
        return False
    else:
        for i in range(len(spec)):
            if not groups[i] == spec[i]:
                return False
    return True

def num_known_damaged_in_row(row):
    return row.count('#')

def num_damaged_to_place(row, spec):
    return sum(spec) - num_known_damaged_in_row(row)

def unknown_indices(row):
    return [i for i, char in enumerate(row) if char == '?']

def possible_rows(row, spec):
    num_to_place = num_damaged_to_place(row, spec)
    indices = unknown_indices(row)
    ways_to_place = list(combinations(indices, num_to_place))
    possible_rows = []
    for placement_spec in ways_to_place:
        new_row = row
        for index in placement_spec:
            if index < len(row):
                new_row = new_row[:index] + '#' + new_row[index+1:]
            else:
                new_row = new_row[:index] + '#'
        new_row = new_row.replace('?', '.')
        possible_rows.append(new_row)
    return possible_rows

main()

# %% Part 2
def main2():
    input_data = get_input('input12.txt')
    num_arrangements = []
    for line in input_data:
        row, spec = line.split(' ')
        row = row + ('?' + row) * 4
        row = row + '.' # Add a dot at the end so that all groups of '#' end in a dot
        spec = spec.split(',')
        spec = [int(i) for i in spec]
        spec *= 5
        record = {} # Dict to keep record of already evaluated row-spec combinations
        num_arrangements.append(get_num_placements(row, spec, record))
    print(f'Answer: The sum of the number of arrangements for each row is {sum(num_arrangements)}')

def get_num_placements(row, spec, record):
    spec_str = ','.join([str(i) for i in spec])
    if (row, spec_str) in record:
        return record[(row, spec_str)]
    last_number_in_spec = (len(spec) == 1)
    if len(spec) == 0:
        return 1

    num_placements = 0
    num_to_place = spec[0]
    max_last_index = get_max_last_index(row, num_to_place)

    start = 0 # Start index for search of a match
    # Look for possible placements, starting at index 'start' of the row
    while start < max_last_index:
        match = re.search('[#?]' * num_to_place + '[\.?]', row[start:])
        if match:
            match_start_index = start + match.span()[0]
            start_of_rest = start + match.span()[1]

            damaged_before_match = '#' in row[start:match_start_index]
            damaged_after_match = '#' in row[start_of_rest:]

            # The first '#' must be contained in the placement,
            # so no '#' can occur before the match for a valid placement.
            # Furthermore, when placing the last number, no '#' can occur after this placement.
            if not damaged_before_match and not (last_number_in_spec and damaged_after_match):
                num_placements += get_num_placements(row[start_of_rest:], spec[1:], record)
            new_start = match_start_index + 1

            # The first '#' must be contained in the placement,
            # so no placements after this can be allowed
            if '#' in row[start:new_start]:
                break
            start = new_start # Start index for next search
        else:
            break

    record[(row, spec_str)] = num_placements
    return num_placements

def get_max_last_index(row, num_to_place):
    max_last_index = len(row) - 1
    next_larger_group = re.search('#' * (num_to_place + 1), row)
    if next_larger_group:
        max_last_index = next_larger_group.span()[0] - 1
    return max_last_index

main2()