# Advent of Code 2023 - day 14

# %% Imports
from common import get_input
import matplotlib.pyplot as plt

# %% Part 1
def main():
    input_data = get_input('input14.txt')
    for i in range(1000):
        grid = Grid(input_data)
        for row in range(grid.height):
            for col in range(grid.width):
                if grid(row, col) == 'O':
                    grid.slide_up(row, col)

    print(f'Answer: The load is {evaluate(grid)}')

def evaluate(grid):
    value = 0
    for row in range(grid.height):
        for col in range(grid.width):
            if grid(row, col) == 'O':
                value += (grid.height - row)
    return value

class Grid:
    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def __call__(self, row, col):
        return self.grid[row][col]
    
    def set_char(self, char, row, col):
        self.grid[row] = self.grid[row][:col] + char + self.grid[row][col + 1:]

    def can_move_up_one_step(self, row, col):
        if row == 0:
            return False
        return self(row - 1, col) not in '#O'
    
    def move_up_one_step(self, row, col):
        self.set_char(self(row, col), row - 1, col)
        self.set_char('.', row, col)

    def slide_up(self, row, col):
        r = row
        while self.can_move_up_one_step(r, col):
            self.move_up_one_step(r, col)
            r -= 1

main()

# %% Part 2
def main2():
    # By setting 'plot' below to True, the transient and periodicity at equilibrium
    # for the load can be inspected, so that adequate values can be selected for
    # 'equilbrium_limit' (a number of cycles larger than the number for which 
    # the transient is over and the limit cycle has been reached) and 
    # 'max_period' (a number larger than the period of the limit cycle)
    plot = True
    input_data = get_input('input14.txt')
    grid = Grid2(input_data)
    
    loads = []
    num_cycles_simulated = 500
    equilibrium_limit = 400
    max_period = 100
    for i in range(num_cycles_simulated):
        grid.spin_cycle()
        loads.append(evaluate(grid))
        if i > equilibrium_limit:
            period = find_period(loads, max_period)
            steps_to_index = (int(1e9) - (i + 1)) % period
            load_after_a_billion_cycles = loads[-1 + steps_to_index - period]
    
    if plot:
        plt.plot(range(1, len(loads) + 1), loads)
        plt.xlabel('Number of spin cycles')
        plt.ylabel('Load')
        plt.grid(True)
    
    print(f'At equilibrium, the load varies periodically with period {period}.')
    print(f'Answer: The load after a billion cycles is {load_after_a_billion_cycles}')

class Grid2:
    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0])

    def __call__(self, row, col):
        return self.grid[row][col]
    
    def set_char(self, char, row, col):
        self.grid[row] = self.grid[row][:col] + char + self.grid[row][col + 1:]

    def can_move_up_one_step(self, row, col):
        if row == 0:
            return False
        return self(row - 1, col) not in '#O'
    
    def can_move_down_one_step(self, row, col):
        if row == self.height - 1:
            return False
        return self(row + 1, col) not in '#O'
    
    def can_move_left_one_step(self, row, col):
        if col == 0:
            return False
        return self(row, col - 1) not in '#O'

    def can_move_right_one_step(self, row, col):
        if col == self.width - 1:
            return False
        return self(row, col + 1) not in '#O'

    def move_one_step(self, row, col, direction):
        if direction == 'up':
            self.set_char(self(row, col), row - 1, col)
        elif direction == 'down':
            self.set_char(self(row, col), row + 1, col)
        elif direction == 'left':
            self.set_char(self(row, col), row, col - 1)
        elif direction == 'right':
            self.set_char(self(row, col), row, col + 1)
        self.set_char('.', row, col)

    def slide(self, row, col, direction):
        r = row
        c = col
        if direction == 'up':
            while self.can_move_up_one_step(r, c):
                self.move_one_step(r, c, 'up')
                r -= 1
        elif direction == 'down':
            while self.can_move_down_one_step(r, c):
                self.move_one_step(r, c, 'down')
                r += 1
        elif direction == 'left':
            while self.can_move_left_one_step(r, c):
                self.move_one_step(r, c, 'left')
                c -= 1
        elif direction == 'right':
            while self.can_move_right_one_step(r, c):
                self.move_one_step(r, c, 'right')
                c += 1

    def slide_all(self, direction):
        if direction == 'up':
            for row in range(self.height):
                for col in range(self.width):
                    if self(row, col) == 'O':
                        self.slide(row, col, 'up')
        elif direction == 'down':
            for row in range(self.height):
                # Go through rows in opposite direction
                row = self.height - 1 - row
                for col in range(self.width):
                    if self(row, col) == 'O':
                        self.slide(row, col, 'down')
        elif direction == 'left':
            for col in range(self.width):
                for row in range(self.height):
                    if self(row, col) == 'O':
                        self.slide(row, col, 'left')
        elif direction == 'right':
            for col in range(self.width):
                # Go through columns in opposite direction
                col = self.width - 1 - col
                for row in range(self.height):
                    if self(row, col) == 'O':
                        self.slide(row, col, 'right')

    def spin_cycle(self):
        self.slide_all('up')
        self.slide_all('left')
        self.slide_all('down')
        self.slide_all('right')

def find_period(numbers, max_len):
    for T in range(1, max_len):
        T_is_period = True
        for i in range(max_len):
            if not numbers[-1 - i] == numbers[-1 - T - i]:
                T_is_period = False
                break
        if T_is_period:
            return T

main2()