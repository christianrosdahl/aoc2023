# Advent of Code 2023 - day 17

# %% Imports
from common import get_input
from typing import NamedTuple
import time

# %% Part 1
def main():
    start_time = time.time()
    input_data = get_input('input17.txt')
    height = len(input_data)
    width = len(input_data[0])
    grid_dimensions = (height, width)

    max_steps_in_same_dir = 3
    source = State(0, 0, 'undefined', 0)

    nodes = []
    for row in range(height):
        for col in range(width):
            for dir in ['up', 'down', 'left', 'right']:
                for steps_in_same_dir in range(1, max_steps_in_same_dir + 1):
                    nodes.append(State(row, col, dir, steps_in_same_dir))
    nodes.append(source)

    dist, prev = dijkstra(get_cost(input_data),
                          nodes,
                          get_neighbors_function(grid_dimensions, max_steps_in_same_dir),
                          source)
    
    destination_states = []
    for dir in ['up', 'down', 'left', 'right']:
        for steps_in_same_dir in range(1, max_steps_in_same_dir + 1):
            destination_states.append(State(height-1, width-1, dir, steps_in_same_dir))
    
    dist_for_destination_states = []
    for state in destination_states:
        dist_for_destination_states.append(dist[state])
    
    print_shortest_dist_for_each_destination_state = False
    if print_shortest_dist_for_each_destination_state:
        print('Min. heat loss for destination states:')
        for i, state in enumerate(destination_states):
            print(f'State: {state}, Min heat loss: {dist_for_destination_states[i]}')
        print()

    min_dist = min(dist_for_destination_states)
    dest_state = next(state for i, state in enumerate(destination_states)
                      if dist_for_destination_states[i] == min_dist)

    show_visualization = True
    if show_visualization:
        visualize(input_data, prev, source, dest_state)

    print(f'Answer: The least possible heat loss is {min_dist}')
    print(f'Computation time: {time.time() - start_time}')

def get_cost(grid_values):
    def cost(pos):
        row, col = pos
        return int(grid_values[row][col])
    return cost

def get_neighbors_function(grid_dimensions, max_steps_in_same_dir):
    def get_neighbors(node):
        neighbors = []
        direction_map = {'up': ['up', 'left', 'right'],
                        'down': ['down', 'left', 'right'],
                        'left': ['left', 'up', 'down'],
                        'right': ['right', 'up', 'down'],
                        'undefined': ['up', 'down', 'left', 'right']}
        possible_directions = direction_map[node.direction]
        if not node.direction == 'undefined':
            if node.steps_in_same_dir == max_steps_in_same_dir:
                possible_directions.remove(node.direction)
        for direction in possible_directions:
            pos = (node.row, node.col)
            pos = get_new_pos_from_direction(pos, direction)
            if position_allowed(grid_dimensions, pos):
                row, col = pos
                if direction == node.direction:
                    steps_in_same_dir = node.steps_in_same_dir + 1
                else:
                    steps_in_same_dir = 1
                neighbors.append(State(row, col, direction, steps_in_same_dir))
        return neighbors
    return get_neighbors

def get_new_pos_from_direction(pos, direction):
    row, col = pos
    if direction == 'up':
        return row - 1, col
    elif direction == 'down':
        return row + 1, col
    elif direction == 'left':
        return row, col - 1
    elif direction == 'right':
        return row, col + 1
    
def position_allowed(grid_dimensions, pos):
    row, col = pos
    height, width = grid_dimensions
    if row < 0 or row >= height:
        return False
    if col < 0 or col >= width:
        return False
    return True

class PriorityQueue:
    def __init__(self, items=[], sorted_prios=[]):
        self.items = items
        self.priorities = sorted_prios

    def add(self, item, prio):
        i = self._find_insertion_index(prio)
        if i < 0:
            self.items.append(item)
            self.priorities.append(prio)
        else:
            self.items.insert(i, item)
            self.priorities.insert(i, prio)
    
    def has_more_items(self):
        return len(self.items) > 0
    
    def get(self):
        self.priorities.pop(0)
        return self.items.pop(0)
    
    def change_prio(self, item, prio):
        i = self.items.index(item)
        self.priorities.pop(i)
        self.items.pop(i)
        self.add(item, prio)

    def _find_insertion_index(self, prio):
        i1 = 0
        i2 = len(self.priorities) - 1
        while not i1 == i2:
            i_middle = int(round((i1 + i2) / 2))
            if self.priorities[i_middle] >= prio:
                i2 = i_middle
            else:
                i1 = i_middle

            if i2 == i1 + 1:
                return i1 if self.priorities[i1] >= prio else i2
        return i1
        

class State(NamedTuple):
    # State object corresponding to a node
    row: int
    col: int
    direction: str
    steps_in_same_dir: int

def dijkstra(cost, nodes, get_neighbors, source):
    print_progress = True
    dist = {source: 0} # Distance per node
    prev = {} # Predecessor of each node

    # Create priority queue
    items = [source]
    prios = [dist[source]]
    for node in nodes:
        if not node == source:
            dist[node] = float('inf')
            prev[node] = None
            items.append(node)
            prios.append(dist[node])
    q = PriorityQueue(items, prios)

    initial_len_q = len(q.items)
    while q.has_more_items():
        node = q.get()
        if print_progress and len(q.items) % 10000 == 0:
            print(f'Progress: {round(100*(initial_len_q - len(q.items)) / initial_len_q)}%')
        for neighbor in get_neighbors(node):
            neighbor_pos = (neighbor.row, neighbor.col)
            alt = dist[node] + cost(neighbor_pos)
            if alt < dist[neighbor]:
                dist[neighbor] = alt
                prev[neighbor] = node
                q.change_prio(neighbor, alt)
    return dist, prev

def visualize(grid, prev, source, dest):
    grid = grid.copy()
    state = dest
    while not state == source:
        row, col = state.row, state.col
        dir = state.direction
        direction_symbols = {'up': '^', 'down': 'v', 'left': '<', 'right': '>'}
        symbol = direction_symbols[dir]
        grid[row] = grid[row][:col] + symbol + grid[row][col+1:]
        state = prev[state]
    for line in grid:
        print(line)
    print()

main()

# %% Part 2
def main2():
    start_time = time.time()
    input_data = get_input('input17.txt')
    height = len(input_data)
    width = len(input_data[0])
    grid_dimensions = (height, width)

    min_steps_in_same_dir = 4
    max_steps_in_same_dir = 10
    source = State(0, 0, 'undefined', 0)

    nodes = []
    for row in range(height):
        for col in range(width):
            for dir in ['up', 'down', 'left', 'right']:
                for steps_in_same_dir in range(1, max_steps_in_same_dir + 1):
                    nodes.append(State(row, col, dir, steps_in_same_dir))
    nodes.append(source)

    dist, prev = dijkstra(get_cost(input_data),
                          nodes,
                          get_neighbors_function2(grid_dimensions,
                                                  min_steps_in_same_dir,
                                                  max_steps_in_same_dir),
                          source)
    
    destination_states = []
    for dir in ['up', 'down', 'left', 'right']:
        for steps_in_same_dir in range(min_steps_in_same_dir, max_steps_in_same_dir + 1):
            destination_states.append(State(height-1, width-1, dir, steps_in_same_dir))
    
    dist_for_destination_states = []
    for state in destination_states:
        dist_for_destination_states.append(dist[state])
    
    print_shortest_dist_for_each_destination_state = False
    if print_shortest_dist_for_each_destination_state:
        print('Min. heat loss for destination states:')
        for i, state in enumerate(destination_states):
            print(f'State: {state}, Min heat loss: {dist_for_destination_states[i]}')
        print()

    min_dist = min(dist_for_destination_states)
    dest_state = next(state for i, state in enumerate(destination_states)
                      if dist_for_destination_states[i] == min_dist)

    show_visualization = True
    if show_visualization:
        visualize(input_data, prev, source, dest_state)

    print(f'Answer: The least possible heat loss is {min_dist}')
    print(f'Computation time: {time.time() - start_time}')

def get_neighbors_function2(grid_dimensions, min_steps_in_same_dir, max_step_in_same_dir):
    def get_neighbors(node):
        neighbors = []
        direction_map = {'up': ['up', 'left', 'right'],
                        'down': ['down', 'left', 'right'],
                        'left': ['left', 'up', 'down'],
                        'right': ['right', 'up', 'down'],
                        'undefined': ['up', 'down', 'left', 'right']}
        possible_directions = direction_map[node.direction]
        if not node.direction == 'undefined':
            if node.steps_in_same_dir == max_step_in_same_dir:
                possible_directions.remove(node.direction)
            elif node.steps_in_same_dir < min_steps_in_same_dir:
                possible_directions = [node.direction]
        for direction in possible_directions:
            pos = (node.row, node.col)
            pos = get_new_pos_from_direction(pos, direction)
            if position_allowed(grid_dimensions, pos):
                row, col = pos
                if direction == node.direction:
                    steps_in_same_dir = node.steps_in_same_dir + 1
                else:
                    steps_in_same_dir = 1
                neighbors.append(State(row, col, direction, steps_in_same_dir))
        return neighbors
    return get_neighbors

main2()