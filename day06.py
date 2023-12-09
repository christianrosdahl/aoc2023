# Advent of Code 2023 - day 6

# %% Imports
from common import get_input
import re
import math

# %% Part 1
# Let x = time to push the button, T = total time, r = previous record time.
# The distance travelled is d = x*(T - x) = -x^2 + T*x.
# To beat the record, we must choose x such that d > r, i.e.,
# -x^2 + T*x > r <=> x^2 - T*x + r > 0.
# This is satisfied for (T/2) - sqrt(T^2/4 - r) < x < (T/2) - sqrt(T^2/4 - r).

def main():
    input_data = get_input('input06.txt')

    # Remove extra spaces in input data
    input_data = [re.sub(' +', ' ', input_data[i]) for i in range(len(input_data))]

    race_times = [int(i) for i in input_data[0].strip().split(' ')[1:]]
    records = [int(i) for i in input_data[1].strip().split(' ')[1:]]

    num_races = len(race_times)

    num_ways_to_win = []
    for race in range(num_races):
        race_time = race_times[race]
        record = records[race]
        num_ways_to_win.append(get_num_ways_to_win_race(race_time, record))

    total_num_ways_to_win = 1
    for i in num_ways_to_win:
        total_num_ways_to_win *= i
    print(f'Number of ways to win each race: {num_ways_to_win}')
    print(f'Answer: The total number of ways to win is {total_num_ways_to_win}')

def get_num_ways_to_win_race(race_time, record):
    eps = 1e-9 # Epsilon used to get strict inequality
    T = race_time
    r = record
    x_min = math.ceil(T/2 - math.sqrt(T**2/4 - r) + eps)
    x_max = math.floor(T/2 + math.sqrt(T**2/4 - r) - eps)
    return x_max - x_min + 1

main()

# %% Part 2
def main():
    input_data = get_input('input06.txt')

    # Remove all spaces in input data
    input_data = [line.replace(' ', '') for line in input_data]

    race_time = int(input_data[0].split(':')[1])
    record = int(input_data[1].split(':')[1])

    num_ways_to_win = get_num_ways_to_win_race(race_time, record)
    print(f'Number of ways to win the race: {num_ways_to_win}')

main()