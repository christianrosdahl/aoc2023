# Advent of Code 2023 - day 7

# %% Imports
from common import get_input
from collections import Counter, OrderedDict

# %% Part 1
def main():
    input_data = get_input('input07.txt')
    hands, bids = get_hands_and_bids(input_data)
    encoding = {'A': 'a', 'K': 'b', 'Q': 'c', 'J': 'd', 'T': 'e', '9': 'f', '8': 'g',
                '7': 'h', '6': 'i', '5': 'j', '4': 'k', '3': 'l', '2': 'm'}
    hands = encode_hands(hands, encoding, get_type)
    hands_to_bids = {hands[i]: bids[i] for i in range(len(hands))}
    hands.sort(reverse=True)
    profit = 0
    for i, hand in enumerate(hands):
        rank = i + 1
        profit += hands_to_bids[hand] * rank
    print(f'Answer: The total profit is {profit}')

def get_hands_and_bids(input_data):
    hands = []
    bids = []
    for line in input_data:
        hand, bid = line.split(' ')
        bid = int(bid)
        hands.append(hand)
        bids.append(bid)
    return hands, bids

def encode_hands(hands, encoding, play_with_jokers=False):
    encoded_hands = []
    for hand in hands:
        encoded_hand = hand
        for char in encoding:
            encoded_hand = encoded_hand.replace(char, encoding[char])
        
        # Add type first to encoding, to allow sorting of encoded strings
        encoded_hand = str(get_type(encoded_hand, play_with_jokers)) + encoded_hand
        encoded_hands.append(encoded_hand)
    return encoded_hands

def get_type(hand, play_with_jokers=False):
    counter = Counter(hand)
    counter = OrderedDict(counter.most_common())
    if play_with_jokers:
        if 'z' in counter: # If there are jokers
            num_jokers = counter.pop('z')
            counter_keys = list(counter.keys())
            if len(counter_keys) == 0: # If there are only jokers
                counter['z'] = num_jokers
            else: # Add jokers to count of mosts frequent card
                first_key = counter_keys[0]
                counter[first_key] += num_jokers
    num_per_label = list(counter.values())
    num_per_label.sort(reverse=True)
    if num_per_label[0] == 5: # Five of a kind
        return 1
    elif num_per_label[0] == 4: # Four of a kind
        return 2
    elif num_per_label[0] == 3 and num_per_label[1] == 2: # Full house
        return 3
    elif num_per_label[0] == 3: # Three of a kind
        return 4
    elif num_per_label[0] == 2 and num_per_label[1] == 2: # Two pair
        return 5
    elif num_per_label[0] == 2: # One pair
        return 6
    else: # High card (all labels distinct)
        return 7
main()

# %% Part 2
def main2():
    input_data = get_input('input07.txt')
    hands, bids = get_hands_and_bids(input_data)
    encoding = {'A': 'a', 'K': 'b', 'Q': 'c', 'J': 'z', 'T': 'e', '9': 'f', '8': 'g',
                '7': 'h', '6': 'i', '5': 'j', '4': 'k', '3': 'l', '2': 'm'}
    hands = encode_hands(hands, encoding, play_with_jokers=True)
    hands_to_bids = {hands[i]: bids[i] for i in range(len(hands))}
    hands.sort(reverse=True)
    profit = 0
    for i, hand in enumerate(hands):
        rank = i + 1
        profit += hands_to_bids[hand] * rank
    print(f'Answer: The total profit is {profit}')

main2()