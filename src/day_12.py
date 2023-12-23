import re
import itertools
from functools import cache


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


def old_main():
    with open('input/test.txt') as f:
        contents = f.readlines()

    grand_total = 0

    for row in contents:
        row_total = 0
        condition_template, groups = row.split(' ')
        groups = list(map(int, groups.split(',')))

        condition_template, groups = unfold(condition_template, groups)

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

    print("Day 12 part 2:", grand_total)

# --------

def unfold(template: str, groups: list[int]) -> (str, list[int]):
    template_rep = [template] * 5
    return ('?'.join(template_rep), groups * 5)


# https://advent-of-code.xavd.id/writeups/2023/day/12/
@cache
def num_valid_solutions(record: str, groups: tuple[int, ...]) -> int:
    # base cases
    if not record:
        # if there are no more spots to check;
        # our only chance at success is if there are no `groups` left
        return len(groups) == 0

    if not groups:
        # if there are no more groups the only possibility of success
        # is that there are no `#` remaining
        return "#" not in record

    # recursive cases
    char, rest_of_record = record[0], record[1:]

    if char == ".":
        # dots are ignores, so keep recursing
        return num_valid_solutions(rest_of_record, groups)

    if char == "#":
        group = groups[0]
        # we're at the start of a group! make sure there are enough here to fill the first group
        # to be valid, we have to be:
        if (
            # long enough to match
            len(record) >= group
            # made of only things that can be `#` (no `.`)
            and all(c != "." for c in record[:group])
            # either at the end of the record (allowed)
            # or the next character isn't also a `#` (would be too big)
            and (len(record) == group or record[group] != "#")
        ):
            return num_valid_solutions(record[group + 1 :], groups[1:])

        return 0

    if char == "?":
        return num_valid_solutions(f"#{rest_of_record}", groups) + num_valid_solutions(
            f".{rest_of_record}", groups
        )


def main():
    with open('input/day_12.txt') as f:
        contents = f.readlines()

    grand_total = 0

    for row in contents:
        record, groups = row.split(' ')
        groups = tuple(map(int, groups.split(',')))

        record, groups = unfold(record, groups)
        row_total = num_valid_solutions(record, groups)
        print("record", record, "total", row_total)
        grand_total += row_total


    print("Day 12 part 2:", grand_total)


if __name__ == '__main__':
  main()
