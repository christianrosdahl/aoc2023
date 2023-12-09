# Advent of Code 2023 - day 5

# %% Imports
from common import get_input
import time

# %% Part 1
def main():
    start_time = time.time()
    input_data = get_input('input05.txt')
    seeds = [int(i) for i in input_data[0].split(' ')[1:]]
    locations = get_locations_from_seeds(input_data, seeds)
    min_location = min(locations)
    index = locations.index(min_location)
    first_seed = seeds[index]
    print(f'Answer: The lowest location number is {min_location}' + 
          f' (and seed number {first_seed} should be planted there)')
    print(f'Execution time: {time.time() - start_time} s')

class Map:
    def __init__(self, ranges):
        self.ranges = ranges

    def __call__(self, source):
        for range in self.ranges:
            if source >= range['start'] and source < range['end']:
                return source + range['deviation']
        return source

def create_map(input_data, map_type):
    map_ranges = []
    read = False
    for line in input_data:
        if len(line) == 0:
            read = False
        if read:
            dest_start, source_start, range_len = [int(i) for i in line.split(' ')]
            deviation = dest_start - source_start
            map_ranges.append({'start': source_start, 'end': source_start + range_len, 'deviation': deviation})
        if map_type in line:
            read = True

    return Map(map_ranges)

def get_locations_from_seeds(input_data, seeds):
    map_order = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light',
                 'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']
    maps = [create_map(input_data, map_type) for map_type in map_order]
    locations = []
    for seed in seeds:
        value = seed
        for m in maps:
            value = m(value)
        locations.append(value)
    return locations

main()

# %% Part 2
# NOTE: This part takes almost 2 hours to run with the given input.
# There should be a faster way to do it...

def main2():
    start_time = time.time()
    input_data = get_input('input05.txt')
    seed_ranges_spec = [int(i) for i in input_data[0].split(' ')[1:]]

    seed_ranges = []
    i = 0
    while i < len(seed_ranges_spec):
        range_start = seed_ranges_spec[i]
        range_len = seed_ranges_spec[i+1]
        range_stop = range_start + range_len
        seed_ranges.append(range(range_start, range_stop))
        i += 2

    min_location = float('inf')
    for r in seed_ranges:
        min_location_for_range = get_min_location_from_seed_range(input_data, r)
        if min_location_for_range < min_location:
            min_location = min_location_for_range

    print(f'Answer: The lowest location number is {min_location}')
    print(f'Execution time: {time.time() - start_time} s')

def get_min_location_from_seed_range(input_data, seed_range):
    map_order = ['seed-to-soil', 'soil-to-fertilizer', 'fertilizer-to-water', 'water-to-light',
                 'light-to-temperature', 'temperature-to-humidity', 'humidity-to-location']
    maps = [create_map(input_data, map_type) for map_type in map_order]
    min_location = float('inf')

    def seed_to_location_map(seed):
        value = seed
        for m in maps:
            value = m(value)
        return value

    for seed in seed_range:
        location = seed_to_location_map(seed)
        if location < min_location:
            min_location = location
    return min_location

main2()