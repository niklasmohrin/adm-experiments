from typing import TypeAlias
from numbers import Real
from pathlib import Path

Distances: TypeAlias = dict[tuple[int, int], Real]
Tour: TypeAlias = list[int]

def generate_greedy(dist: Distances) -> Tour:
    raise NotImplementedError

def improve(tour: Tour) -> Tour:
    raise NotImplementedError
