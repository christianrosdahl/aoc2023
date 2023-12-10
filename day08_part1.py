# Advent of Code 2023 - day 8

# %% Imports
from common import get_input

# %% Part 1
def main():
    input_path = 'input08.txt'
    network, directions = get_data_from_input(input_path)
    steps = 0
    node = 'AAA'
    while not node == 'ZZZ':
        direction = directions[steps % len(directions)]
        node = network[node][direction]
        steps += 1
    
    print(f'Answer: The number of steps is {steps}')

def remove_symbols(string, symbols):
    new_string = string
    for symbol in symbols:
        new_string = new_string.replace(symbol, '')
    return new_string

def get_data_from_input(input_path):
    input_data = get_input(input_path)
    directions = input_data[0]
    network_spec = input_data[2:]
    network = {}
    for line in network_spec:
        line = remove_symbols(line, '(),')
        node, _, left, right = line.split(' ')
        network[node] = {'L': left, 'R': right}
    return network, directions

main()