# Advent of Code 2023 - day 18

# %% Imports
from common import get_input
from typing import NamedTuple
import copy

# %% Part 1
def main():
    input_data = get_input('input18.txt')
    edges = []
    pos_change = lambda s: {'U': (-s, 0), 'D': (s, 0), 'L': (0, -s), 'R': (0, s)}
    last_point = Point(0, 0)
    for line in input_data:
        direction, steps, _ = line.split(' ')
        steps = int(steps)
        d_row, d_col = pos_change(steps)[direction]
        new_point = Point(last_point.row + d_row, last_point.col + d_col)
        edges.append(Edge(last_point, new_point))
        last_point = new_point
    edges = get_displaced_edges(edges)
    grid = create_grid(edges)
    grid = get_filled_grid(grid)
    visualize_area = True
    if visualize_area:
        visualize(grid)
    print(f'Answer: The total area is {area(grid)}')

class Point(NamedTuple):
    row: int
    col: int

class Edge(NamedTuple):
    p1: Point
    p2: Point

def get_displaced_edges(edges):
    min_row = float('inf')
    min_col = float('inf')
    for e in edges:
        min_row = min(min_row, e.p1.row, e.p2.row)
        min_col = min(min_col, e.p1.col, e.p2.col)

    new_edges = []
    for e in edges:
        p1 = Point(e.p1.row - min_row, e.p1.col - min_col)
        p2 = Point(e.p2.row - min_row, e.p2.col - min_col)
        new_edges.append(Edge(p1, p2))
    return new_edges

def create_grid(edges):
    max_row = -float('inf')
    max_col = -float('inf')
    for e in edges:
        max_row = max(max_row, e.p1.row, e.p2.row)
        max_col = max(max_col, e.p1.col, e.p2.col)
    width = max_col + 1
    height = max_row + 1
    grid = [['.' for _ in range(width)] for _ in range(height)]

    for e in edges:
        row1, col1 = e.p1.row, e.p1.col
        row2, col2 = e.p2.row, e.p2.col
        for row in range(min(row1, row2), max(row1, row2) + 1):
            for col in range(min(col1, col2), max(col1, col2) + 1):
                grid[row][col] = '#'
    return grid

def get_filled_grid(grid):
    height = len(grid)
    width = len(grid[0])
    filled_grid = copy.deepcopy(grid)
    for row in range(1, height-1):
        inside = False
        for col in range(0, width):
            if grid[row-1][col] == '#' and grid[row][col] == '#':
                inside = not inside
            if inside:
                filled_grid[row][col] = '#'
    return filled_grid

def area(grid):
    value = 0
    for row in grid:
        for char in row:
            if char == '#':
                value += 1
    return value

def visualize(grid):
    print()
    for row in grid:
        print(''.join(row))
    print()

main()

# %% Part 2
def main2():
    input_data = get_input('input18.txt')
    pos_change = lambda s: {'U': (-s, 0), 'D': (s, 0), 'L': (0, -s), 'R': (0, s)}
    direction_dict = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}
    last_point = Point(0, 0)
    points = [last_point]
    directions = []
    for line in input_data:
        info = line.split(' ')[2][2:-1]
        steps = int(info[:-1], 16)
        direction = direction_dict[int(info[-1])]
        directions.append(direction)
        d_row, d_col = pos_change(steps)[direction]
        new_point = Point(last_point.row + d_row, last_point.col + d_col)
        points.append(new_point)
        last_point = new_point

    area = get_lagoon_area(points, directions)
    print(f'Answer: The total area is {area}')

def polygon_area(points):
    # Compute the area of a polygon from its corner points
    # using the "trapezoid formula"
    area = 0
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i+1) % len(points)]
        area += 0.5 * (p1.col + p2.col) * (p1.row - p2.row)
    area = int(abs(area))
    return area

def circumference(points):
    # Compute the circumference of a polygon from its corner points
    circumference = 0
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i+1) % len(points)]
        circumference += abs(p2.row - p1.row) + abs(p2.col - p1.col)
    return circumference

def get_num_clockwise_turns(directions):
    clockwise_turns = ['RD', 'DL', 'LU', 'UR']
    count = 0
    for i in range(len(directions)):
        dir1 = directions[i]
        dir2 = directions[(i+1) % len(directions)]
        if dir1 + dir2 in clockwise_turns:
            count += 1
    return count

def get_lagoon_area(points, directions):
    # To compute the lagoon area, we start by computing the area of the 
    # polygon that is made up by connecting the center points of each 
    # pair of consecutively dug square meters in the trench (as well as
    # the center points of the first and the last dug square meters).

    # To this, we have to add the parts of the trench that are ouside of
    # this polygon. For the "interior part" of each edge, excluding the two 
    # square meters at the corners, half of the trench is outside the 
    # polygon, so we should add half a square meter for each edge meter.

    # For each corner square meter, the area outside of the polygon is
    # 3/4 square meters if the trench turns clockwise and 1/4 square meters
    # if it turns anti-clockwise. So, for the corner square meters, the area
    # outside of the polygon is either 1/4 square meters more or less than
    # for the interior of the edges, depending on the turning direction.
    # Combining this information, we can compute the area of the lagoon:

    num_clockwise_turns = get_num_clockwise_turns(directions)
    num_anticlockwise_turns = len(directions) - num_clockwise_turns

    area = int(polygon_area(points) + 0.5 * circumference(points)
            + 0.25 * num_clockwise_turns - 0.25 * num_anticlockwise_turns)
    return area


main2()