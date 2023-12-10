# Advent of Code 2023 - day 10

# %% Imports
from common import get_input

# %% Part 1
def main():
    grid = get_input('input10.txt')
    grid = add_padding(grid)

    start = find_start(grid)
    start_neighbors = find_start_neighbors(grid, start)
    pos1 = start_neighbors[0]
    pos2 = start_neighbors[1]
    visited1 = [start, pos1]
    visited2 = [start, pos2]

    num_steps = 1
    while not pos1 == pos2:
        directions1 = directions_from_pos(grid, pos1)
        directions2 = directions_from_pos(grid, pos2)
        pos1 = get_next_pos(pos1, visited1, directions1)
        pos2 = get_next_pos(pos2, visited2, directions2)
        visited1.append(pos1)
        visited2.append(pos2)
        num_steps += 1

    print(f'Answer: The point farthest from start is {num_steps} steps away')

def add_padding(grid):
    extra_row = ['.' * len(grid[0])]
    padded_grid = extra_row + grid + extra_row
    for i in range(len(padded_grid)):
        padded_grid[i] = '.' + padded_grid[i] + '.'
    return padded_grid

def find_start(grid):
    grid_height = len(grid)
    grid_width = len(grid[0])
    for row in range(grid_height):
        for col in range(grid_width):
            if grid[row][col] == 'S':
                return (row, col)
            
def find_start_neighbors(grid, start_pos):
    (row, col) = start_pos
    start_neighbors = []
    delta = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for d in delta:
        row2 = row + d[0]
        col2 = col + d[1]
        if not grid[row2][col2] == '.':
            start_neighbors.append((row2, col2))
    return start_neighbors

def directions_from_pos(grid, pos):
    return directions_from_char(grid[pos[0]][pos[1]])

def directions_from_char(char):
    if char == '|':
        return [(-1,0), (1,0)]
    elif char == '-':
        return [(0,-1), (0,1)]
    elif char == 'L':
        return [(0,1), (-1,0)]
    elif char == 'J':
        return [(0,-1), (-1,0)]
    elif char == '7':
        return [(0,-1), (1,0)]
    elif char == 'F':
        return [(0,1), (1,0)]
    
def get_next_pos(pos, visited, directions):
        pos_alt1 = (pos[0] + directions[0][0], pos[1] + directions[0][1])
        pos_alt2 = (pos[0] + directions[1][0], pos[1] + directions[1][1])
        if pos_alt1 in visited:
            return pos_alt2
        return pos_alt1

main()