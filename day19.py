# Advent of Code 2023 - day 19

# %% Imports
from common import get_input
from typing import NamedTuple

# %% Part 1
def main():
    input_data = get_input('input19.txt')
    workflows, parts = parse_data(input_data)
    rating_sum = 0
    for part in parts:
        accepted = run_workflows(workflows, part)
        if accepted:
            rating_sum += sum(part.values())
    print(f'Answer: The sum of the ratings for the accepted parts is {rating_sum}')

def parse_data(input_data):
    i = next(i for i, line in enumerate(input_data) if line == '')
    workflows_list = input_data[:i]
    parts_list = input_data[i+1:]

    workflows = {}
    for workflow in workflows_list:
        name, rules = workflow[:-1].split('{')
        workflows[name] = rules.split(',')
    
    parts = []
    for part in parts_list:
        part_properties = {}
        properties_list = part[1:-1].split(',')
        for property in properties_list:
            name, val = property.split('=')
            part_properties[name] = int(val)
        parts.append(part_properties)
        
    return workflows, parts

def run_workflows(workflows, part):
    state = 'in'
    i = 0
    while not state in ['A', 'R'] or i < 1:
        i += 1
        for rule in workflows[state]:
            if '<' in rule or '>' in rule:
                condition, result = rule.split(':')
                if check_condition(condition, part):
                    state = result
                    break
            else:
                state = rule

    return state == 'A'

def check_condition(condition, part):
    if '>' in condition:
        prop, val = condition.split('>')
        return part[prop] > int(val)
    elif '<' in condition:
        prop, val = condition.split('<')
        return part[prop] < int(val)

main()

# %% Part 2
def main2():
    input_data = get_input('input19.txt')
    workflows, _ = parse_data(input_data)
    prop_min = 1
    prop_max = 4000
    all_intervals = get_intervals_for_accepted(workflows, prop_min, prop_max)
    total_num_combinations = 0
    for intervals in all_intervals:
        total_num_combinations += get_combinations_for_intervals(intervals)
    print(f'Answer: The total number of property combinations for accepted parts is {total_num_combinations}')

class State(NamedTuple):
    workflow: str
    rule_num: int

def get_intervals_for_accepted(workflows, prop_min, prop_max):
    all_intervals = []
    state = State('in', 0)
    intervals = {prop: [prop_min, prop_max] for prop in ['x', 'm', 'a', 's']}
    add_intervals_from_state(workflows, all_intervals, state, intervals)
    return all_intervals

def add_intervals_from_state(workflows, all_intervals, state, intervals):
    if state.workflow == 'A':
        all_intervals.append(intervals)
        return
    elif state.workflow == 'R':
        return
    rule = workflows[state.workflow][state.rule_num]
    if '<' in rule:
        condition, result = rule.split(':')
        prop, limit = condition.split('<')
        limit = int(limit)
        intervals1 = intervals.copy()
        intervals2 = intervals.copy()
        intervals1[prop] = [intervals[prop][0], limit-1]
        intervals2[prop] = [limit, intervals[prop][1]]
        state1 = State(result, 0)
        state2 = State(state.workflow, state.rule_num + 1)
        add_intervals_from_state(workflows, all_intervals, state1, intervals1)
        add_intervals_from_state(workflows, all_intervals, state2, intervals2)
    elif '>' in rule:
        condition, result = rule.split(':')
        prop, limit = condition.split('>')
        limit = int(limit)
        intervals1 = intervals.copy()
        intervals2 = intervals.copy()
        intervals1[prop] = [intervals[prop][0], limit]
        intervals2[prop] = [limit+1, intervals[prop][1]]
        state1 = State(state.workflow, state.rule_num + 1)
        state2 = State(result, 0)
        add_intervals_from_state(workflows, all_intervals, state1, intervals1)
        add_intervals_from_state(workflows, all_intervals, state2, intervals2)
    else:
        workflow = rule
        state = State(workflow, 0)
        add_intervals_from_state(workflows, all_intervals, state, intervals)

def get_combinations_for_intervals(intervals):
    result = 1
    for interval in intervals.values():
        result *= (interval[1] - interval[0] + 1)
    return result

main2()