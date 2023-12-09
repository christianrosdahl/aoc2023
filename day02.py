# Advent of Code 2023 - day 2

# %% Imports
from common import get_input

# %% Common functions and classes (used in both parts)
def set_to_dict(set):
    dict = {}
    for item in set.split(', '):
        num, color = item.split(' ')
        dict[color] = int(num)
    return dict

# %% Part 1
def main():
    games = get_input('input02.txt')
    feasible_game_id_sum = 0
    actual_numbers = {'red': 12, 'green': 13, 'blue': 14}
    for game in games:
        game_possible = True
        game_name, games = game.split(': ')
        game_id = int(game_name.split(' ')[1])
        sets = games.split('; ')
        for set in sets:
            if not possible_set(set_to_dict(set), actual_numbers):
                game_possible = False
                break
        if game_possible:
            feasible_game_id_sum += game_id
    print(f'Result: {feasible_game_id_sum}')

def possible_set(set, actual_numbers):
    for color in actual_numbers:
        if color in set and actual_numbers[color] < set[color]:
            return False
    return True

main()

# %% Part 2
def main():
    games = get_input('input02.txt')
    sum_of_powers = 0
    for game in games:
        min_num_cubes = {'red': 0, 'green': 0, 'blue': 0}
        game_name, games = game.split(': ')
        sets = games.split('; ')
        for set in sets:
            set_dict = set_to_dict(set)
            for color in set_dict:
                num_cubes_for_color = set_dict[color]
                if num_cubes_for_color > min_num_cubes[color]:
                    min_num_cubes[color] = num_cubes_for_color
        power = 1;
        for color in min_num_cubes:
            power *= min_num_cubes[color]
        sum_of_powers += power
    print(f'Result: {sum_of_powers}')

main()