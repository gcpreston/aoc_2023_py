from typing import Set


class Beam:
    position: (int, int) # row, col
    direction: str # '^', '<', '>', or 'v'

    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def __eq__(self, other):
        return self.position == other.position and self.direction == other.direction

    def tick(self, tile: str) -> list['Beam']:
        new_directions = self._next_direction(tile)

        new_beams = []
        for d in new_directions:
            new_beam = Beam(self.position, d)
            new_position = new_beam._next_position()
            new_beam.position = new_position
            new_beams.append(new_beam)

        return new_beams


    def _next_direction(self, tile: str) -> list[str]:
        if tile == '-':
            if self.direction in ['<', '>']:
                return [self.direction]
            else:
                return ['<', '>']

        elif tile == '|':
            if self.direction in ['^', 'v']:
                return [self.direction]
            else:
                return ['^', 'v']

        elif tile == '/':
            if self.direction == '>':
                return ['^']
            elif self.direction == '<':
                return ['v']
            elif self.direction == '^':
                return ['>']
            elif self.direction == 'v':
                return ['<']

        elif tile == '\\':
            if self.direction == '>':
                return ['v']
            elif self.direction == '<':
                return ['^']
            elif self.direction == '^':
                return ['<']
            elif self.direction == 'v':
                return ['>']

        return [self.direction]


    def _next_position(self) -> (int, int):
        row, col = self.position

        if self.direction == '^':
            return (row - 1, col)
        if self.direction == 'v':
            return (row + 1, col)
        if self.direction == '<':
            return (row, col - 1)
        if self.direction == '>':
            return (row, col + 1)

        raise ValueError(f'Invalid direction: {self.direction}')


class Contraption:
    input: list[str]
    beams: list[Beam]
    seen = set()
    energized = set()

    def __init__(self, input: list[str], start_position: (int, int), start_direction: str):
        self.input = input
        self.beams = [Beam(start_position, start_direction)]
        self.seen = set([(start_position[0], start_position[1], start_direction)])
        self.energized = set([start_position])

    def tick(self):
        new_beams = []

        for beam in self.beams:
            row, col = beam.position
            if row >= 0 and row < len(self.input) and col >= 0 and col < len(self.input[row]):
                pos_and_dir = (row, col, beam.direction)
                self.seen.add(pos_and_dir)
                self.energized.add(beam.position)

                next_beams = beam.tick(self.input[row][col])

                for n in next_beams:
                    pos_and_dir = (n.position[0], n.position[1], n.direction)
                    if pos_and_dir not in self.seen:
                        new_beams.append(n)

        self.beams = new_beams


def num_energized(input: list[str], start_position: (int, int), start_direction: str) -> int:
    contraption = Contraption(input, start_position, start_direction)

    while contraption.beams:
        contraption.tick()

    return len(contraption.energized)


def main():
    with open('input/day_16.txt') as f:
        input = [line.strip() for line in f.readlines()]

    most_energized = 0
    for row in range(len(input)):
        right_test = num_energized(input, (row, 0), '>')
        left_test = num_energized(input, (row, len(input[0]) - 1), '<')
        higher = max(right_test, left_test)

        if higher > most_energized:
            most_energized = higher

    for col in range(len(input[0])):
        down_test = num_energized(input, (0, col), 'v')
        up_test = num_energized(input, (len(input) - 1, col), '^')
        higher = max(down_test, up_test)

        if higher > most_energized:
            most_energized = higher

    print("Day 16 part 2:", most_energized)


if __name__ == '__main__':
    main()
