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

    def __init__(self, input: list[str]):
        self.input = input
        self.beams = [Beam((0, 0), '>')]

    def tick(self):
        new_beams = []

        for beam in self.beams:
            row, col = beam.position
            if row >= 0 and row < len(self.input) and col >= 0 and col < len(self.input[row]):
                next_beams = beam.tick(self.input[row][col])

                for n in next_beams:
                    pos_and_dir = (n.position[0], n.position[1], n.direction)
                    if pos_and_dir not in self.seen:
                        self.seen.add(pos_and_dir)
                        new_beams.append(n)

        self.beams = new_beams


def num_energized(input: list[str]) -> int:
    contraption = Contraption(input)
    energized_positions = set(contraption.beams[0].position)

    while contraption.beams:
        contraption.tick()

        for beam in contraption.beams:
            energized_positions.add(beam.position)

    return len(energized_positions)


def main():
    with open('input/test.txt') as f:
        input = [line.strip() for line in f.readlines()]

    print("Day 16 part 1:", num_energized(input))


if __name__ == '__main__':
    main()
