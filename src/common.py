# https://www.redblobgames.com/pathfinding/a-star/implementation.html

import heapq
import collections

from typing import Tuple, TypeVar, Iterator, Optional

Location = TypeVar('Location')
GridLocation = Tuple[int, int]
T = TypeVar('T')

class Queue:
    def __init__(self):
        self.elements = collections.deque()

    def empty(self) -> bool:
        return not self.elements

    def put(self, x: T):
        self.elements.append(x)

    def get(self) -> T:
        return self.elements.popleft()

    def __repr__(self) -> str:
        return str(list(self.elements))


class Graph:
    def neighbors(self, id: Location) -> list[Location]: pass


class SquareGrid(Graph):
    def __init__(self, min_x: int, max_x: int, min_y: int, max_y: int, walls: list[GridLocation]):
        self.min_x = min_x
        self.max_x = max_x
        self.min_y = min_y
        self.max_y = max_y
        self.walls: list[GridLocation] = walls

    def in_bounds(self, id: GridLocation) -> bool:
        (x, y) = id
        return self.min_x <= x <= self.max_x and self.min_y <= y <= self.max_y

    def passable(self, id: GridLocation) -> bool:
        return id not in self.walls

    def neighbors(self, id: GridLocation) -> Iterator[GridLocation]:
        (x, y) = id
        neighbors = [(x+1, y), (x-1, y), (x, y-1), (x, y+1)] # E W N S
        # see "Ugly paths" section for an explanation:
        if (x + y) % 2 == 0: neighbors.reverse() # S N W E
        results = filter(self.in_bounds, neighbors)
        results = filter(self.passable, results)
        return results


class WeightedGraph(Graph):
    def cost(self, from_id: Location, to_id: Location) -> float: pass


class GridWithWeights(SquareGrid, WeightedGraph):
    def __init__(self, min_x: int, max_x: int, min_y: int, max_y: int):
        super().__init__(min_x, max_x, min_y, max_y)
        self.weights: dict[GridLocation, float] = {}

    def cost(self, from_node: GridLocation, to_node: GridLocation) -> float:
        return self.weights.get(to_node, 1)

class PriorityQueue:
    def __init__(self):
        self.elements: list[tuple[float, T]] = []

    def empty(self) -> bool:
        return not self.elements

    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))

    def get(self) -> T:
        return heapq.heappop(self.elements)[1]

def dijkstra_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    directions: dict[Location, str] = {}

    while not frontier.empty():
        current: Location = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:

                # skip if we've been going straight too long
                if current[0] == next[0]:
                    if current[1] < next[1]:
                        direction = '>'
                    else:
                        direction = '<'
                else:
                    if current[0] < next[0]:
                        direction = 'v'
                    else:
                        direction = '^'

                max_repeats = 3
                last_few = [direction, directions.get(current, None)]
                last_few_positions = [next, current]
                previous = current

                for _ in range(max_repeats - 1):
                    previous = came_from[previous]
                    if previous is None:
                        break
                    last_few.append(directions.get(previous, None))
                    last_few_positions.append(previous)

                if len(last_few) == max_repeats + 1 and len(set(last_few)) == 1:
                    print('skipping', next, list(reversed(last_few)), list(reversed(last_few_positions)))
                    continue

                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current

                directions[next] = direction

    return came_from, cost_so_far, directions

def heuristic(a: GridLocation, b: GridLocation) -> float:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)

def a_star_search(graph: WeightedGraph, start: Location, goal: Location):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: dict[Location, Optional[Location]] = {}
    cost_so_far: dict[Location, float] = {}
    came_from[start] = None
    cost_so_far[start] = 0

    directions: dict[Location, str] = {}

    while not frontier.empty():
        current: Location = frontier.get()

        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:

                # skip if we've been going straight too long
                if current[0] == next[0]:
                    if current[1] < next[1]:
                        direction = '>'
                    else:
                        direction = '<'
                else:
                    if current[0] < next[0]:
                        direction = 'v'
                    else:
                        direction = '^'

                max_repeats = 3
                last_few = [direction, directions.get(current, None)]
                last_few_positions = [next, current]
                previous = current

                for _ in range(max_repeats - 1):
                    previous = came_from.get(previous, None)
                    if previous is None:
                        break
                    last_few.append(directions.get(previous, None))
                    last_few_positions.append(previous)

                if len(last_few) == max_repeats + 1 and len(set(last_few)) == 1:
                    print('skipping', next, list(reversed(last_few)), list(reversed(last_few_positions)))
                    continue

                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next, goal)
                frontier.put(next, priority)
                came_from[next] = current

                # add direction
                directions[next] = direction

    return came_from, cost_so_far, directions

def reconstruct_path(came_from: dict[Location, Location],
                     start: Location, goal: Location) -> list[Location]:
    current: Location = goal
    path: list[Location] = []
    if goal not in came_from: # no path was found
        return []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start) # optional
    path.reverse() # optional
    return path

def breadth_first_search(graph: Graph, start: Location):
    frontier = Queue()
    frontier.put(start)
    came_from: dict[Location, Optional[Location]] = {}
    came_from[start] = None

    while not frontier.empty():
        current: Location = frontier.get()

        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    return came_from

