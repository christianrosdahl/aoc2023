# Advent of Code 2023 - day 13

# %% Imports
from common import get_input

# %% Part 1
def main():
    input_data = get_input('input13.txt')
    patterns = get_patterns(input_data)

    lines_of_reflection = []
    for pattern in patterns:
        lines_of_reflection.append(get_line_of_reflection(pattern))

    ans = get_pattern_notes_summary(lines_of_reflection)
    print(f'Answer: The summary of the pattern notes is {ans}')

def get_patterns(input_data):
    patterns = []
    pattern = []
    for line in input_data:
        if line == '':
            patterns.append(pattern)
            pattern = []
        else:
            pattern.append(line)
    patterns.append(pattern)
    return patterns

def equal_rows(pattern, row1, row2):
    return pattern[row1] == pattern[row2]

def equal_cols(pattern, col1, col2):
    for i in range(len(pattern)):
        if not pattern[i][col1] == pattern[i][col2]:
            return False
    return True

def get_line_of_reflection(pattern):
    height = len(pattern)
    width = len(pattern[0])

    # Get horizontal line of reflection
    for row1 in range(height - 1):
        if is_horizontal_line_of_reflection(pattern, row1):
            # Return type and num rows above reflection line
            return ('horizontal', row1 + 1)

    # Get vertical line of reflection
    for col1 in range(width - 1):
        if is_vertical_line_of_reflection(pattern, col1):
            # Return type and num cols to the left of reflection line
            return ('vertical', col1 + 1)

def is_horizontal_line_of_reflection(pattern, row1):
    # Returns true if there is a horizontal line of reflection between
    # row 'row1' and the following row 'row2' in the pattern
    height = len(pattern)
    row2 = row1 + 1
    for i in range(min(row1 + 1, height - row2)):
        if not equal_rows(pattern, row1 - i, row2 + i):
            return False
    return True
        
def is_vertical_line_of_reflection(pattern, col1):
    # Returns true if there is a vertical line of reflection between
    # column 'col1' and the following column 'col2' in the pattern
    width = len(pattern[0])
    col2 = col1 + 1
    for i in range(min(col1 + 1, width - col2)):
        if not equal_cols(pattern, col1 - i, col2 + i):
            return False
    return True

def get_pattern_notes_summary(lines_of_reflection):
    ans = 0
    for line in lines_of_reflection:
        if line[0] == 'vertical':
            ans += line[1]
        else: # line[0] == 'horizontal'
            ans += 100 * line[1]
    return ans

main()

# %% Part 2
def main2():
    input_data = get_input('input13.txt')
    patterns = get_patterns(input_data)

    lines_of_reflection = []
    for pattern in patterns:
        lines_of_reflection.append(get_line_of_reflection_with_smudge(pattern))

    ans = get_pattern_notes_summary(lines_of_reflection)
    print(f'Answer: The summary of the pattern notes is {ans}')

def get_line_of_reflection_with_smudge(pattern):
    height = len(pattern)
    width = len(pattern[0])

    # Get horizontal line of reflection
    for row1 in range(height - 1):
        if is_horizontal_line_of_reflection_with_smudge(pattern, row1):
            # Return type and num rows above reflection line
            return ('horizontal', row1 + 1)

    # Get vertical line of reflection
    for col1 in range(width - 1):
        if is_vertical_line_of_reflection_with_smudge(pattern, col1):
            # Return type and num cols to the left of reflection line
            return ('vertical', col1 + 1)
        
def is_horizontal_line_of_reflection_with_smudge(pattern, row1):
    # Returns true if there is a horizontal line of reflection between
    # row 'row1' and the following row 'row2' in the pattern
    height = len(pattern)
    row2 = row1 + 1
    smudge_found = False
    for i in range(min(row1 + 1, height - row2)):
        if not equal_rows(pattern, row1 - i, row2 + i):
            if not smudge_found and almost_equal_rows(pattern, row1 - i, row2 + i):
                smudge_found = True
            else:
                return False
    return smudge_found
        
def is_vertical_line_of_reflection_with_smudge(pattern, col1):
    # Returns true if there is a vertical line of reflection between
    # column 'col1' and the following column 'col2' in the pattern
    width = len(pattern[0])
    col2 = col1 + 1
    smudge_found = False
    for i in range(min(col1 + 1, width - col2)):
        if not equal_cols(pattern, col1 - i, col2 + i):
            if not smudge_found and almost_equal_cols(pattern, col1 - i, col2 + i):
                smudge_found = True
            else:
                return False
    return smudge_found

def almost_equal_rows(pattern, row1, row2):
    # Returns true if rows are equal except for one character
    width = len(pattern[0])
    row1 = pattern[row1]
    row2 = pattern[row2]
    num_different_chars = 0
    for i in range(width):
        if not row1[i] == row2[i]:
            num_different_chars += 1
        if num_different_chars > 1:
            return False
    return num_different_chars == 1

def almost_equal_cols(pattern, col1, col2):
    # Returns true if columns are equal except for one character
    height = len(pattern)
    num_different_chars = 0
    for i in range(height):
        if not pattern[i][col1] == pattern[i][col2]:
            num_different_chars += 1
        if num_different_chars > 1:
            return False
    return num_different_chars == 1

main2()