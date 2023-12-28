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


def area(instructions: list[tuple[str, int]]) -> int:
    current = (0, 0) # (x, y)
    outline = [current]

    print('Computing outline...')
    for instruction in instructions:
        print('instruction', instruction)
        direction, distance = instruction
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

    grid = SquareGrid(min_x - 1, max_x + 1, min_y - 1, max_y + 1, set(outline))

    print('Computing BFS...')
    bfs_start = (min_x - 1, min_y - 1)
    result = breadth_first_search(grid, bfs_start)
    print('Computed BFS, length:', len(result), end='\n\n')

    canvas_width = (max_x - min_x + 3)
    canvas_height = (max_y - min_y + 3)
    print('x and y ranges', (min_x, max_x), (min_y, max_y))
    print('w and h', canvas_width, canvas_height)
    return (canvas_width * canvas_height) - len(result)


def area_v2(instructions: list[tuple[str, int]]) -> int:
    current = (0, 0) # (x, y)
    outline = [current]

    print('Computing outline...')
    for instruction in instructions:
        direction, distance = instruction
        distance = int(distance)

        if direction == 'L':
            current = (current[0] - distance, current[1])
        elif direction == 'R':
            current = (current[0] + distance, current[1])
        elif direction == 'U':
            current = (current[0], current[1] + distance)
        elif direction == 'D':
            current = (current[0], current[1] - distance)

        outline.append(current)

    print('Done:', outline)
    print()
    connections = [(outline[i], outline[i + 1]) for i in range(len(outline) - 1)]
    min_y = min(y for x, y in outline)
    max_y = max(y for x, y in outline)

    borders_and_passings: dict[int, tuple[tuple[int, int], int]] = dict()

    print('Computing borders and passings...')
    for row in range(min_y, max_y + 1):
        borders = []
        passings = []

        for ((x0, y0), (x1, y1)) in connections:
            is_horizontal = y0 == y1

            if is_horizontal:
                if y0 == row:
                    borders.append((x0, x1))
            elif y0 < row < y1 or y1 < row < y0:
                # => is vertical => x0 == x1
                passings.append(x0)

        borders_and_passings[row] = (borders, passings)
        print('row', row, 'got b&p', borders, passings)

    print('Done:', borders_and_passings)
    print()

    print('Computing area...')
    total_area = 0

    for row, (borders, passings) in borders_and_passings.items():
        combined_connections = 

        # OLD
        # border_area = sum(abs(b - a) + 1 for (a, b) in borders)
        # passings_groups = [(passings[i], passings[i + 1]) for i in range(0, len(passings) - 1, 2)]
        # passings_area = sum(abs(b - a) + 1 for (a, b) in passings_groups)

        # print('row', row, 'got border', border_area, 'and passings', passings_area)

        # total_area += border_area + passings_area

    return total_area


def main():
    with open('input/test.txt') as f:
        lines = [line.strip() for line in f.readlines()]

    line_re = re.compile(r'(L|R|U|D) (\d+) \(#(.+)\)')

    # instructions = []
    # for line in lines:
    #     hex_data = line_re.match(line).group(3)
    #     distance = int(hex_data[:5], 16)

    #     if hex_data[5] == '0':
    #         direction = 'R'
    #     elif hex_data[5] == '1':
    #         direction = 'D'
    #     elif hex_data[5] == '2':
    #         direction = 'L'
    #     elif hex_data[5] == '3':
    #         direction = 'U'

    #     instructions.append((direction, distance))

    instructions = [line_re.match(line).groups()[:2] for line in lines]

    print('Day 18 part 2:', area_v2(instructions))


if __name__ == '__main__':
    main()
