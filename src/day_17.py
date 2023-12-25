from typing import List
from collections import deque

from common import GridWithWeights, GridLocation, a_star_search, reconstruct_path, dijkstra_search

def main():
    with open('input/test.txt') as f:
        data = [line.strip() for line in f.readlines()]

    grid = GridWithWeights(len(data[0]), len(data))
    for row in range(len(data)):
        for col in range(len(data[row])):
            grid.weights[(row, col)] = int(data[row][col])

    start = (0, 0)
    destination = (7, 11)
    came_from, cost_so_far, directions = a_star_search(grid, start, destination)
    # came_from, cost_so_far, directions = dijkstra_search(grid, (0, 0), (len(data[0]) - 1, len(data) - 1))
    path = reconstruct_path(came_from, start, destination)

    # print('cost', cost_so_far[destination])
    print('path', path)

    # print the grid
    for row in range(len(data)):
        for col in range(len(data[row])):
            if (row, col) in path:
                direction = directions.get((row, col), None)
                if direction is not None:
                    print(directions[(row, col)], end='')
                else:
                    print(data[row][col], end='')
            else:
                print(data[row][col], end='')
        print()
    print()

    # answer
    print(cost_so_far[destination])
    print(sum(int(data[row][col]) for row, col in path))


if __name__ == '__main__':
    main()
