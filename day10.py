# Advent of Code 2023 - day 10

# %% Imports
from common import get_input

# %% Part 1
def main(input_path):
    grid = get_input(input_path)
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
    
    visited2.reverse()
    path = visited1 + visited2[1:]

    print(f'Answer: The point farthest from start is {num_steps} steps away')
    return path

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

path = main('input10.txt')

# %% Part 2
def main2(input_path, visualize=False):
    grid = get_input(input_path)
    grid = add_padding(grid)
    path = main(input_path)
    remove_junk(grid, path)
    replace_start_tile(grid, path)
    label_grid(grid)
    num_tiles_inside_loop = count_labels('I', grid)
    
    if visualize:
        for line in grid:
            print(line)

    print(f'Answer: The number of tiles inside the loop is {num_tiles_inside_loop}')

def replace_start_tile(grid, path):
    start = path[0]
    neighbor1 = path[1]
    neighbor2 = path[-2]
    directions = [get_neighbor_direction(start, neighbor1), 
                  get_neighbor_direction(start, neighbor2)]
     
    if 'up' in directions and 'down' in directions:
        replacement_tile = '|'
    elif 'left' in directions and 'right' in directions:
        replacement_tile = '-'
    elif 'up' in directions and 'right' in directions:
        replacement_tile = 'L'
    elif 'up' in directions and 'left' in directions:
        replacement_tile = 'J'
    elif 'left' in directions and 'down' in directions:
        replacement_tile = '7'
    elif 'down' in directions and 'right' in directions:
        replacement_tile = 'F'
    else:
        replacement_tile = '?'
    
    replace_grid_char(grid, start[0], start[1], replacement_tile)

def get_neighbor_direction(pos, neighbor_pos):
    d_row, d_col = (neighbor_pos[0] - pos[0], neighbor_pos[1] - pos[1])
    if d_row == -1:
        return 'up'
    elif d_row == 1:
        return 'down'
    elif d_col == -1:
        return 'left'
    elif d_col == 1:
        return 'right'
    else:
        return '?'

def remove_junk(grid, path):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if not (i,j) in path:
                replace_grid_char(grid, i, j, '.')

def replace_grid_char(grid, row, col, char):
    grid[row] = grid[row][:col] + char + grid[row][col+1:]

def label_grid(grid):
    # Assume that the pipes run along the center lines of the tiles
    # and that we iterate each row of the grid slightly above the center line.
    # Then, we cross the curve if we pass a tile |, L or J; but not if we pass
    # 7 or F, since the vertical lines run only below the center of the row.
    for i, line in enumerate(grid):
        is_in_loop = False
        for j, char in enumerate(line):
            if char in '|LJ':
                is_in_loop = not is_in_loop
            elif is_in_loop and char == '.':
                replace_grid_char(grid, i, j, 'I')

def count_labels(label, grid):
    count = 0
    for row in grid:
        for char in row:
            if char == label:
                count += 1
    return count

visualize = False # Show resulting grid with path and tiles inside the loop marked
main2('input10.txt', visualize)