# Advent of Code 2023 - day 3

# %% Common functions and classes (used in both parts)
def get_input():
    file = open('input03.txt','r')
    lines = file.readlines()
    for i in range(len(lines)):
        lines[i] = lines[i].replace('\n', '')
    file.close()
    return lines

class GridNumber:
    def __init__(self, number, line, start_index, end_index):
        self.number = number
        self.line = line
        self.start_index = start_index
        self.end_index = end_index
    
    def __eq__(self, other):
        self.number == other.number
        self.line == other.line
        self.start_index = other.start_index
        self.end_index = other.end_index

def get_grid_numbers(grid):
    grid_height = len(grid)
    grid_width = len(grid[0])
    grid_numbers = []
    for i, line in enumerate(grid):
        j = 0
        while j < grid_width:
            if line[j].isnumeric():
                k = j
                while line[k].isnumeric():
                    k += 1
                    if k == grid_width:
                        break
                grid_numbers.append(GridNumber(line[j:k], i, j, k-1))
                j = k
            else:
                j += 1
    return grid_numbers

# %% Part 1
def main():
    grid = get_input()
    grid_numbers = get_grid_numbers(grid)
    result = 0
    for grid_number in grid_numbers:
        if has_adjacent_symbol(grid, grid_number):
            result += int(grid_number.number)
    print(f'Answer: {result}')

def has_adjacent_symbol(grid, grid_number):
    grid_height = len(grid)
    grid_width = len(grid[0])
    for i in range(grid_number.start_index, grid_number.end_index + 1):
        adj_values = get_adjacent_values(grid, grid_number.line, i)
        for adj_value in adj_values:
            if not adj_value.isnumeric() and not adj_value == '.':
                return True
    return False

def get_adjacent_values(grid, row, col):
    grid_height = len(grid)
    grid_width = len(grid[0])
    values = []
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if not (i == 0 and j == 0):
                adj_row = row + i
                adj_col = col + j
                if adj_row >= 0 and adj_row < grid_height and adj_col >= 0 and adj_col < grid_width:
                    values.append(grid[adj_row][adj_col])
    return values

main()

# %% Part 2
def main():
    grid = get_input()
    grid_numbers = get_grid_numbers(grid)
    stars = {}
    for grid_number in grid_numbers:
        adj_stars = get_adjacent_stars(grid, grid_number)
        for star in adj_stars:
            if star in stars:
                if grid_number not in stars[star]:
                    stars[star].append(grid_number)
            else:
                stars[star] = [grid_number]
    
    answer = 0
    for star in stars:
        if len(stars[star]) == 2:
            num_close_to_star = [int(num.number) for num in stars[star]]
            row = star[0]
            col = star[1]
            answer += num_close_to_star[0] * num_close_to_star[1]

    print(f'Answer: {answer}')

def get_adjacent_stars(grid, grid_number):
    grid_height = len(grid)
    grid_width = len(grid[0])
    stars = []
    row = grid_number.line
    for col in range(grid_number.start_index, grid_number.end_index + 1):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                if not (i == 0 and j == 0):
                    adj_row = row + i
                    adj_col = col + j
                    if adj_row >= 0 and adj_row < grid_height and adj_col >= 0 and adj_col < grid_width:
                        if grid[adj_row][adj_col] == '*' and (adj_row, adj_col) not in stars:
                            stars.append((adj_row, adj_col))
    return stars

main()