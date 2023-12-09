# Advent of Code 2023 - day 4

# %% Imports
from common import get_input

# %% Common functions and classes (used in both parts)
def get_num_matches(card):
    card = card.replace('  ', ' ') # Remove double spaces
    card = card.split(': ')[1] # Remove "Card N: " from line
    winning_nbrs, my_nbrs = card.split(' | ')
    winning_nbrs = winning_nbrs.split(' ')
    my_nbrs = my_nbrs.split(' ')

    num_matches = 0
    for nbr in my_nbrs:
        if nbr in winning_nbrs:
            num_matches += 1
    return num_matches

# %% Part 1
def main():
    cards = get_input('input04.txt')
    answer = 0
    for card in cards:
        card_points = 0
        num_matches = get_num_matches(card)
        card_points = 2**(num_matches-1) if num_matches >= 1 else 0
        answer += card_points
    print(f'Answer: {answer}')

main()

# %% Part 2
def main():
    cards = get_input('input04.txt')
    num_cards = [1 for _ in range(len(cards))]
    for i, card in enumerate(cards):
        num_matches = get_num_matches(card)
        for j in range(i + 1, i + 1 + num_matches):
            num_cards[j] += num_cards[i]

    total_num_cards = sum(num_cards)
    print(f'Answer: {total_num_cards}')

main()