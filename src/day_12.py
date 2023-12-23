import re
import itertools


def condition_match(template: str, condition: str) -> bool:
    t = template.replace('.', 'x').replace('?', '.')
    c = condition.replace('.', 'x')
    template_re = re.compile(t)
    return bool(template_re.match(c))


def is_possible_arrangement(
        groups: list[int],
        slot_distribution: list[int],
        condition_template: str
    ) -> bool:
    if len(slot_distribution) != len(groups) + 1:
        raise f"Invalid groups + slot distributions combo: {groups}, {slot_distribution}"

    condition = '.' * slot_distribution[0]
    for (group, slot) in zip(groups, slot_distribution[1:]):
        condition += '#' * group
        condition += '.' * (slot + 1)
    condition = condition[:-1]
    # print(f"checking condition {condition} vs template {condition_template}")

    return condition_match(condition_template, condition)


# https://stackoverflow.com/questions/28965734/general-bars-and-stars
def partitions(n: int, k: int):
    for c in itertools.combinations(range(n + k - 1), k - 1):
        yield [b - a - 1 for a, b in zip((-1,) + c, c + (n + k - 1,))]


def main():
    with open('input/day_12.txt') as f:
        contents = f.readlines()

    grand_total = 0

    for row in contents:
        row_total = 0
        condition_template, groups = row.split(' ')
        groups = list(map(int, groups.split(',')))

        extra_space_count = len(condition_template) - (sum(groups) + (len(groups) - 1))
        slot_count = len(groups) + 1

        if extra_space_count == 0:
            row_total += 1
        else:
            for slot_distribution in partitions(extra_space_count, slot_count):
                if is_possible_arrangement(groups, slot_distribution, condition_template):
                    row_total += 1

        grand_total += row_total
        print("template and total", condition_template, row_total)

    print("Day 12 part 1:", grand_total)



if __name__ == '__main__':
  main()
