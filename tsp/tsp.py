#!/usr/bin/env python3

import random
import sys
from dataclasses import dataclass
from functools import partial
from numbers import Real
from typing import TypeAlias

import matplotlib.pyplot as plt

import tsp_utils as tspu


Distances: TypeAlias = dict[tuple[int, int], Real]
Tour: TypeAlias = list[int]


def plot(points, path):
    x = [points[i][0] for i in path]
    y = [points[i][1] for i in path]
    plt.plot(x, y)
    plt.title("path")
    plt.show()


MAX_CANDIDATES = 5


def generate_greedy(n: int, dist: Distances) -> Tour:
    tour = [random.randrange(n)]
    remaining = set(range(n)) - {tour[-1]}

    for _ in range(n - 1):
        candidates = sorted(remaining, key=lambda v: dist[tour[-1], v])[:MAX_CANDIDATES]
        tour.append(random.choice(candidates))
        remaining.remove(tour[-1])

    return tour


def assert_is_valid_tour(tour: Tour) -> Tour:
    assert sorted(tour) == list(range(len(tour)))
    return tour


@dataclass
class Move:
    tour: Tour
    i: int
    h: int

    def resulting_tour(self) -> Tour:
        j = self.i + 1
        k = self.h + 1
        return assert_is_valid_tour(
            self.tour[:j] + list(reversed(self.tour[j:k])) + self.tour[k:]
        )

    def cost_difference(self, dist: Distances) -> Real:
        n = len(self.tour)
        cost = lambda a, b: dist[self.tour[a % n], self.tour[b % n]]
        removed_cost = cost(self.i, self.i + 1) + cost(self.h, self.h + 1)
        added_cost = cost(self.i, self.h) + cost(self.i + 1, self.h + 1)
        return added_cost - removed_cost

    @classmethod
    def all_for(cls, tour: Tour):
        for i in range(len(tour) - 1):
            j = i + 1
            for h in range(j + 1, len(tour)):
                k = h + 1

                if i == 0 and k == len(tour):
                    continue

                yield Move(tour, i, h)


def improve_locally(dist: Distances, tour: Tour) -> Tour:
    while True:
        move = min(Move.all_for(tour), key=partial(Move.cost_difference, dist=dist))
        if move.cost_difference(dist) >= 0:
            return tour
        tour = move.resulting_tour()


def main():
    n, points, dist, opt_tour, opt_cost = tspu.readTSPLIB(sys.argv[1])

    start = generate_greedy(n, dist)
    plot(points, start)
    local_optimum = improve_locally(dist, start)
    print(
        f"Improved random tour from {tspu.computeCost(start, dist)} to {tspu.computeCost(local_optimum, dist)} (global optimum is {opt_cost})"
    )
    plot(points, local_optimum)


if __name__ == "__main__":
    main()
