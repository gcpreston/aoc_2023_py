import re

from common import SquareGrid, breadth_first_search


def walk_between(start: tuple[int, int], end: tuple[int, int]) -> list[tuple[int, int]]:
    """Walk between two points, not including the start point"""
    x1, y1 = start
    x2, y2 = end

    if x1 == x2:
        step = 1 if y1 < y2 else -1
        end = y2 + 1 if step == 1 else y2 - 1
        return [(x1, y) for y in range(y1 + step, end, step)]
    elif y1 == y2:
        step = 1 if x1 < x2 else -1
        end = x2 + 1 if step == 1 else x2 - 1
        return [(x, y1) for x in range(x1 + step, end, step)]
    else:
        raise ValueError('Cannot walk between two points that are not on the same axis.')


def area(instructions: list[tuple[str, int, str]]) -> int:
    current = (0, 0) # (x, y)
    outline = [current]

    for instruction in instructions:
        direction, distance, _hash = instruction
        distance = int(distance)

        if direction == 'L':
            following = (current[0] - distance, current[1])
        elif direction == 'R':
            following = (current[0] + distance, current[1])
        elif direction == 'U':
            following = (current[0], current[1] + distance)
        elif direction == 'D':
            following = (current[0], current[1] - distance)

        outline.extend(walk_between(current, following))
        current = following

    print('Computed outline, length:', len(outline), end='\n\n')

    min_x = min(x for x, y in outline)
    max_x = max(x for x, y in outline)
    min_y = min(y for x, y in outline)
    max_y = max(y for x, y in outline)

    grid = SquareGrid(min_x - 1, max_x + 1, min_y - 1, max_y + 1, outline)

    print('Computing BFS...')
    bfs_start = (min_x - 1, min_y - 1)
    result = breadth_first_search(grid, bfs_start)
    print('Computed BFS, length:', len(result), end='\n\n')

    canvas_width = (max_x - min_x + 3)
    canvas_height = (max_y - min_y + 3)
    print('x and y ranges', (min_x, max_x), (min_y, max_y))
    print('w and h', canvas_width, canvas_height)
    return (canvas_width * canvas_height) - len(result)


def main():
    with open('input/day_18.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    line_re = re.compile(r'(L|R|U|D) (\d+) \(#(.+)\)')
    instructions = [line_re.match(line).groups() for line in lines]

    print('Day 18 part 1:', area(instructions))


if __name__ == '__main__':
    main()
