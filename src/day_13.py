from typing import Optional


def check_horizontal_reflection(pattern: list[str], top_line_index: int) -> bool:
    top_check = top_line_index
    bottom_check = top_line_index + 1

    while top_check >= 0 and bottom_check < len(pattern):
        if pattern[top_check] != pattern[bottom_check]:
            return False

        top_check -= 1
        bottom_check += 1

    return True


# Returns the number of rows above the horizontal reflection,
# if one exists. Otherwise, returns None.
def find_horizontal_reflection(pattern: list[str]) -> Optional[int]:
    possible_h_reflections = []

    prev_line = pattern[0]
    for (i, line) in enumerate(pattern[1:]):
        if line == prev_line:
            possible_h_reflections.append(i + 1) # since for line index 1, i = 0
        prev_line = line

    return next((r for r in possible_h_reflections if check_horizontal_reflection(pattern, r - 1)), None)


def diagonal_flip(pattern: list[str]) -> list[str]:
    new_pattern = []

    for col in range(len(pattern[0])):
        new_line = ''
        for row in range(len(pattern)):
            new_line += pattern[row][col]

        new_pattern.append(new_line)

    return new_pattern


def find_vertical_reflection(pattern: list[str]) -> int:
    diag = diagonal_flip(pattern)
    return find_horizontal_reflection(diag)


def summarize(pattern: list[str]) -> int:
    # check horizontal
    h_reflection = find_horizontal_reflection(pattern)
    v_reflection = find_vertical_reflection(pattern)

    if h_reflection:
        return h_reflection * 100
    return v_reflection


def main():
    with open('input/day_13.txt') as f:
        contents = f.read().strip()

    patterns = [p.split('\n') for p in contents.split('\n\n')]
    total = sum(summarize(p) for p in patterns)

    print("Day 13 part 1:", total)


if __name__ == '__main__':
    main()
