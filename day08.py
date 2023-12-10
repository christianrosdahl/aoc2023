# Advent of Code 2023 - day 8

# %% Imports
from common import get_input
import math

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

# %% Part 2

# Examining the frequency for which each path reaches an end state,
# it turns out that this occurs periodically, with the period equal to 
# the number of steps to reach an end node the first time (why is this?).
# Thus, all end nodes will be in an end state simultaneously for the least
# common multiple of these periods, which can be computed using the least
# common divisor, which is implemented in the math package.

def main2():
    input_path = 'input08.txt'
    network, directions = get_data_from_input(input_path)

    nodes = [n for n in network if n[-1] == 'A']
    steps_to_endnodes = []
    for node in nodes:
        steps = 0
        while not node[-1] == 'Z':
            direction = directions[steps % len(directions)]
            node = network[node][direction]
            steps += 1
        steps_to_endnodes.append(steps)

    total_number_of_steps = lcm(steps_to_endnodes)
    
    print(f'Answer: The number of steps is {total_number_of_steps}')

def lcm_two_numbers(a, b):
    # Compute least common multiple between a and b
    return round(abs(a*b) / math.gcd(a,b))

def lcm(numbers):
    # Compute least common multiple between all numbers in a list
    if len(numbers) == 2:
        return lcm_two_numbers(numbers[0], numbers[1])
    else:
        return lcm_two_numbers(numbers[0], lcm(numbers[1:]))

main2()