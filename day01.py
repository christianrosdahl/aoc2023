# Advent of Code 2023 - day 1

# %% Imports
from common import get_input

# %% Part 1
def main():
    lines = get_input('input01.txt')

    # Get sum
    sum = 0
    numbers = [str(i) for i in range(0,10)]
    for line in lines:
        first_number = None
        last_number = None
        for char in line:
            if char in numbers:
                last_number = char
                if first_number is None:
                    first_number = char
        sum += int(first_number + last_number)
    print("Result: " + str(sum))

main()

# %% Part 2
def main():
    lines = get_input('input01.txt')
    sum = 0
    numbers = [str(i) for i in range(0,10)]
    numbers_text = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
    text_to_num = {numbers_text[i]: str(i) for i in range(0,10)}
    numbers += numbers_text
    for line in lines:
        first_index = None
        last_index = None
        first_number = None
        last_number = None
        for number in numbers:
            index = line.find(number)
            if index >= 0 and (first_index is None or index < first_index):
                first_index = index
                first_number = text_to_num[number] if len(number) > 1 else number
            
            index = line.rfind(number)
            if index >= 0 and (last_index is None or index > last_index):
                last_index = index
                last_number = text_to_num[number] if len(number) > 1 else number
        sum += int(first_number + last_number)
    print("Result: " + str(sum))

main()