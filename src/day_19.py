import re

from typing import Dict, List, Optional, Tuple

Category = str # 'x', 'm', 'a', 's'
Rating = Dict[Category, int]

Label = str
Comparator = str # '<' | '>'
Result = Label | bool
Rule = Tuple[Category, Comparator, int, Result] | Result
Instruction = List[Rule]
Workflows = Dict[Label, Instruction]


def rule_match(rule: Rule, rating: Rating) -> Optional[Result]:
    if isinstance(rule, (str, bool)):
        return rule

    category, operation, benchmark, result = rule

    if operation == '<':
        if rating[category] < benchmark:
            return result
    else:
        if rating[category] > benchmark:
            return result

    return None


def run_instruction(instruction: Instruction, rating: Rating) -> Result:
    for rule in instruction:
        maybe_result = rule_match(rule, rating)
        if maybe_result is not None:
            return maybe_result


def is_rating_accepted(workflows: Workflows, rating: List[Rating]) -> bool:
    current = workflows['in']

    while True:
        next_val = run_instruction(current, rating)

        if isinstance(next_val, bool):
            return next_val

        current = workflows[next_val]


def parse_result(s: str) -> Result:
    if s == 'A':
        return True
    elif s == 'R':
        return False
    else:
        return s


def parse_workflows(s: str) -> Workflows:
    workflow_re = re.compile(r'([a-z]+)\{(.+)\}')
    rule_re = re.compile(r'([a-z]+)(<|>)(\d+):([a-zA-Z]+)')
    workflows: Workflows = {}

    for line in s.strip().split('\n'):
        workflow_match = workflow_re.match(line)
        label = workflow_match.group(1)
        rules_str = workflow_match.group(2)

        rules_split = rules_str.split(',')
        rules = []

        for rule_str in rules_split:
            if rule_m := rule_re.match(rule_str):
                # conditional case
                rule = (rule_m.group(1), rule_m.group(2), int(rule_m.group(3)), parse_result(rule_m.group(4)))
            else:
                # label case
                rule = parse_result(rule_str)

            rules.append(rule)

        workflows[label] = rules

    return workflows


def parse_ratings(s: str) -> List[Rating]:
    rule_re = re.compile(r'\{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)\}')
    ratings = []

    for line in s.strip().split('\n'):
        rating = {category: int(value) for category, value in rule_re.match(line).groupdict().items()}
        ratings.append(rating)

    return ratings


def main():
    with open('input/day_19.txt') as f:
        contents = f.read().strip()

    workflows_str, ratings_str = contents.split('\n\n')

    workflows = parse_workflows(workflows_str)
    ratings = parse_ratings(ratings_str)

    accepted_ratings = filter(lambda rating: is_rating_accepted(workflows, rating), ratings)
    total = sum(map(lambda rating: sum(rating.values()), accepted_ratings))

    print('Day 19 part 1:', total)


if __name__ == '__main__':
    main()
