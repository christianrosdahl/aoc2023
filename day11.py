# Advent of Code 2023 - day 11

# %% Imports
from common import get_input

# %% Part 1
def main():
    image = get_input('input11.txt')
    expand_universe(image)

    galaxies = get_galaxies(image)
    pairs = [(g1, g2) for i, g1 in enumerate(galaxies)
             for j, g2 in enumerate(galaxies[i+1:])]
    distances = []
    for pair in pairs:
        distances.append(l1_norm(pair[0], pair[1]))
    dist_sum = sum(distances)
    
    print(f'Answer: The sum of the l1-distances between each galaxy pair is {dist_sum}')

def expand_universe(image):
    rows_to_expand = get_empty_rows(image)
    cols_to_expand = get_empty_cols(image)

    num_rows_added = 0
    for row in rows_to_expand:
        add_row(image, row + num_rows_added)
        num_rows_added += 1

    num_cols_added = 0
    for col in cols_to_expand:
        add_col(image, col + num_cols_added)
        num_cols_added += 1

def get_empty_rows(image):
    rows = []
    for i, row in enumerate(image):
        if '#' not in row:
            rows.append(i)
    return rows

def get_empty_cols(image):
    num_rows = len(image)
    num_cols = len(image[0])
    non_empty_cols = []
    for j in range(num_cols):
        for i in range(num_rows):
            if image[i][j] == '#':
                non_empty_cols.append(j)
                break
    empty_cols = []
    for i in range(num_cols):
        if i not in non_empty_cols:
            empty_cols.append(i)
    return empty_cols

def get_galaxies(image):
    num_rows = len(image)
    num_cols = len(image[0])
    galaxies = []
    for i in range(num_rows):
        for j in range(num_cols):
            if image[i][j] == '#':
                galaxies.append((i,j))
    return galaxies

def add_row(image, index):
    num_cols = len(image[0])
    row = '.' * num_cols
    image = image.insert(index, row)

def add_col(image, index):
    num_rows = len(image)
    num_cols = len(image[0])
    for i, row in enumerate(image):
        image[i] = row[:index] + '.' + row[index:]

def l1_norm(pos1, pos2):
    return abs(pos2[0] - pos1[0]) + abs(pos2[1] - pos1[1])

main()

# %% Part 2
def main2():
    image = get_input('input11.txt')

    galaxies = get_galaxies(image)
    pairs = [(g1, g2) for i, g1 in enumerate(galaxies)
             for j, g2 in enumerate(galaxies[i+1:])]
    
    empty_rows = get_empty_rows(image)
    empty_cols = get_empty_cols(image)

    distances = []
    for pair in pairs:
        distances.append(galaxy_norm(pair[0], pair[1], empty_rows, empty_cols))
    dist_sum = sum(distances)

    print(f'Answer: The distance between each galaxy pair is {dist_sum}')

def galaxy_norm(pos1, pos2, empty_rows, empty_cols):
    expansion_factor = 1000000
    norm = l1_norm(pos1, pos2)

    num_empty_rows_between_galaxies = 0
    for i in range(min(pos1[0], pos2[0]), max(pos1[0], pos2[0])):
        if i in empty_rows:
            num_empty_rows_between_galaxies += 1
        
    num_empty_cols_between_galaxies = 0
    for i in range(min(pos1[1], pos2[1]), max(pos1[1], pos2[1])):
        if i in empty_cols:
            num_empty_cols_between_galaxies += 1

    norm += (expansion_factor-1) * (num_empty_rows_between_galaxies
                                + num_empty_cols_between_galaxies)
    return norm

main2()
