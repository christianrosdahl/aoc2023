# Advent of Code 2023 - day 16

# %% Imports
from common import get_input

# %% Part 1
def main():
    input_data = get_input('input16.txt')
    grid = Grid(input_data)
    beams = [Beam(grid)]
    num_energized_tiles = propagate_beams(grid, beams)

    print(f'Answer: The number of energized tiles is {num_energized_tiles}')

class Beam:
    def __init__(self, grid, row = 0, col = 0, direction = 'right'):
        self.grid = grid
        self.row = row
        self.col = col
        self.direction = direction

    def pos(self):
        return self.row, self.col
    
    def split(self, direction):
        if direction == 'vertically':
            return (Beam(self.grid, self.row, self.col, direction = 'up'),
                    Beam(self.grid, self.row, self.col, direction = 'down'))
        elif direction == 'horizontally':
            return (Beam(self.grid, self.row, self.col, direction = 'left'),
                    Beam(self.grid, self.row, self.col, direction = 'right'))

    def can_move_one_step(self, direction):
        if direction == 'up':
            return not self.row == 0
        elif direction == 'down':
            return not self.row == self.grid.height - 1
        elif direction == 'left':
            return not self.col == 0
        elif direction == 'right':
            return not self.col == self.grid.width - 1
        
    def move_one_step(self, direction):
        if direction == 'up':
            self.row -= 1
        elif direction == 'down':
            self.row += 1
        elif direction == 'left':
            self.col -= 1
        elif direction == 'right':
            self.col += 1

class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])
        self.reset() # Reset record of energized tiles

    def __call__(self, pos):
        row, col = pos
        return self.grid[row][col]
    
    def set_energized(self, pos):
        row, col = pos
        self.energized[row][col] = '#'

    def get_num_energized(self):
        num = 0
        for row in range(self.height):
            for col in range(self.width):
                if self.energized[row][col] == '#':
                    num += 1
        return num
    
    def reset(self):
        # Reset record of energized tiles
        self.energized = [['.' for _ in range(self.width)]
                           for _ in range(self.width)]

def remove(list, indices):
    # Remove several items by index from a list
    indices.sort()
    for i, index in enumerate(indices):
        del list[index - i]

def maybe_split_beam(grid, beam):
    split_beams = False
    if beam.direction in ['left', 'right'] and grid(beam.pos()) == '|':
        split_beams = True
        beam1, beam2 = beam.split('vertically')
    elif beam.direction in ['up', 'down'] and grid(beam.pos()) == '-':
        split_beams = True
        beam1, beam2 = beam.split('horizontally')
    if split_beams:
        return beam1, beam2
    return False

def maybe_change_direction(grid, beam):
    if grid(beam.pos()) == '\\':
        dir_change = {'up': 'left', 'down': 'right',
                        'left': 'up', 'right': 'down'}
        beam.direction = dir_change[beam.direction]
    if grid(beam.pos()) == '/':
        dir_change = {'up': 'right', 'down': 'left',
                        'left': 'down', 'right': 'up'}
        beam.direction = dir_change[beam.direction]

def maybe_split_or_change_direction(grid, beams):
    beams_to_remove = []
    beams_to_add = []
    for i, beam in enumerate(beams):
        # Split beam if on a split tile
        split_beam = maybe_split_beam(grid, beam)
        if split_beam:
            beams_to_add.append(split_beam[0])
            beams_to_add.append(split_beam[1])
            beams_to_remove.append(i)

        # Change direction if on a mirror tile
        maybe_change_direction(grid, beam)

    # Replace each split beam with the two resulting ones
    remove(beams, beams_to_remove)
    for beam in beams_to_add:
        beams.append(beam)

def move_beams(beams):
    # Move each beam one step if possible, or delete the beam
    beams_to_remove = []
    for i, beam in enumerate(beams):
        if beam.can_move_one_step(beam.direction):
            beam.move_one_step(beam.direction)
        else:
            beams_to_remove.append(i)
    remove(beams, beams_to_remove)

def propagate_beams(grid, beams):
    record = set() # Record of previous combinations of beam position and direction
    while len(beams) > 0:
        # Remove beams that correspond to previous ones
        beams_to_remove = []
        for i, beam in enumerate(beams):
            if (beam.pos(), beam.direction) in record:
                beams_to_remove.append(i)
        remove(beams, beams_to_remove)

        # Save current beam position to record and mark tile as energized
        for i, beam in enumerate(beams):
            record.add((beam.pos(), beam.direction))
            grid.set_energized(beam.pos())

        maybe_split_or_change_direction(grid, beams)
        move_beams(beams)
    
    return grid.get_num_energized()

main()

# %% Part 2
def main2():
    input_data = get_input('input16.txt')
    grid = Grid(input_data)

    max_num_energized_tiles = 0
    for row in range(grid.height):
        col = 0
        beams = [Beam(grid, row, col, 'right')]
        num_energized_tiles = propagate_beams(grid, beams)
        max_num_energized_tiles = max(num_energized_tiles, max_num_energized_tiles)
        grid.reset()

        col = grid.width - 1
        beams = [Beam(grid, row, col, 'left')]
        num_energized_tiles = propagate_beams(grid, beams)
        max_num_energized_tiles = max(num_energized_tiles, max_num_energized_tiles)
        grid.reset()

    for col in range(grid.width):
        row = 0
        beams = [Beam(grid, row, col, 'down')]
        num_energized_tiles = propagate_beams(grid, beams)
        max_num_energized_tiles = max(num_energized_tiles, max_num_energized_tiles)
        grid.reset()

        row = grid.height - 1
        beams = [Beam(grid, row, col, 'up')]
        num_energized_tiles = propagate_beams(grid, beams)
        max_num_energized_tiles = max(num_energized_tiles, max_num_energized_tiles)
        grid.reset()

    print(f'Answer: The maximum number of energized tiles is {max_num_energized_tiles}')

main2()