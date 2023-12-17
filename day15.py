# Advent of Code 2023 - day 15

# %% Imports
from common import get_input

# %% Part 1
def main():
    input_data = get_input('input15.txt')
    steps = input_data[0].split(',')
    hashed_steps = []
    for step in steps:
        hashed_steps.append(hash(step))
    ans = sum(hashed_steps)
    print(f'Answer: The sum of the hashed steps is {ans}')

def hash(str):
    value = 0
    for char in str:
        value += ord(char)
        value *= 17
        value = value % 256
    return value

main()

# %% Part 2
def main2():
    input_data = get_input('input15.txt')
    steps = input_data[0].split(',')
    boxes = [Box() for _ in range(256)]
    for step in steps:
        box_number, label, action, focal_length = decode_step(step)
        if action == 'remove':
            boxes[box_number].remove(label)
        elif action == 'add':
            lens = Lens(label, focal_length)
            boxes[box_number].add(lens)

    ans = get_focusing_power(boxes)
    print(f'Answer: The focusing power of the resulting lens config is {ans}')

class Box:
    def __init__(self):
        self.num_lenses = 0
        self.lenses = {}
        self.lens_positions = {}

    def remove(self, label):
        if label in self.lenses:
            del self.lenses[label]
            self.num_lenses -= 1

            # Move other lenses to fill void
            position = self.lens_positions[label]
            for other_lens in self.lenses:
                if self.lens_positions[other_lens] > position:
                    self.lens_positions[other_lens] -= 1

            del self.lens_positions[label]

    def add(self, lens):
        label = lens.label
        if not label in self.lenses:
            self.num_lenses += 1
            self.lens_positions[label] = self.num_lenses
        self.lenses[label] = lens

class Lens:
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length

def decode_step(step):
    step = step.replace('=', ' = ')
    step = step.replace('-', ' -')
    info = step.split(' ')
    label = info[0]
    box_number = hash(label)
    action = info[1]
    if action == '-':
        action = 'remove'
        focal_length = None
    elif action == '=':
        action = 'add'
        focal_length = int(info[2])
    return box_number, label, action, focal_length

def get_focusing_power(boxes):
    focusing_power = 0
    for i, box in enumerate(boxes):
        for label in box.lenses:
            lens = box.lenses[label]
            focusing_power += (i+1) * box.lens_positions[label] * lens.focal_length
    return focusing_power

main2()