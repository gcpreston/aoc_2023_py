def tilt_north(input: list[str]) -> list[str]:
    if len(input) == 0:
        return []

    stops = [0] * len(input[0])
    tilted: list[list[str]] = []

    for row in range(len(input)):
        tilted.append(list(input[row]))
        next_stops = stops.copy()

        for col in range(len(input[row])):
            char = input[row][col]

            if char == 'O':
                tilted[stops[col]][col] = 'O'
                next_stops[col] += 1

                if stops[col] != row:
                    tilted[row][col] = '.'
            elif char == '#':
                next_stops[col] = row + 1

        stops = next_stops

    return [''.join(row) for row in tilted]


def tilt_south(input: list[str]) -> list[str]:
    return list(reversed(tilt_north(list(reversed(input)))))


def flip_east(a: list[str]) -> list[str]:
    return [''.join(z) for z in reversed(list(zip(*a)))]


def flip_west(a: list[str]) -> list[str]:
    return [''.join(z) for z in zip(*reversed(a))]


def tilt_east(input: list[str]) -> list[str]:
    flipped = flip_east(input)
    tilted = tilt_north(flipped)
    result = flip_west(tilted)
    return result


def tilt_west(input: list[str]) -> list[str]:
    west_input = flip_west(input)
    return flip_east(tilt_north(west_input))

def cycle(input: tuple[str, ...]) -> tuple[str, ...]:
    a = tilt_north(input)
    a = tilt_west(a)
    a = tilt_south(a)
    a = tilt_east(a)
    return tuple(a)


def total_load(input: list[str]) -> int:
    total = 0

    for row, line in enumerate(input):
        load_per_rock = len(input) - row

        for char in line:
            if char == 'O':
                total += load_per_rock

    return total


def print_grid(g: list[str]) -> None:
    for h in g:
        print(h)


def main():
    with open('input/day_14.txt') as f:
        contents = tuple(line.strip() for line in f.readlines())

    target_cycles = 1000000000
    seen = {}
    cycle_start = None
    cycle_length = None
    results = {}

    tilted = contents
    for c in range(target_cycles):
        results[c] = tilted
        tilted = cycle(tilted)

        if tilted in seen:
            cycle_start = seen[tilted]
            cycle_length = c - seen[tilted]
            break
        else:
            seen[tilted] = c

    equiv = ((target_cycles - cycle_start) % cycle_length) + cycle_start
    print("Day 14 part 2:", total_load(results[equiv]))


if __name__ == '__main__':
    main()
