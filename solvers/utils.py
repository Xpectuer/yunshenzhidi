import itertools

import game_map
from consts import *
def pick_elements(collection, N):
    # Get all combinations of size N
    combinations = list(itertools.combinations(collection, N))
    return combinations

def flatMap(func, iterable):
    return list(itertools.chain.from_iterable(map(func, iterable)))

def flatten(iterable):
    return flatMap(lambda x: x, iterable)

def coor_diff(a, b):
    print(a,b)
    return (a[0]- b[0], a[1]- b[1])

def coor_add(a,b):
    return (a[0] + b[0], a[1] + b[1])

def traverse_interval_2d(f, interval):
    x_coor = interval[0]
    y_coor = interval[1]
    for x in range(*x_coor):
        for y in range(*y_coor):
            f(x,y)

"""
undo_stack: [(0,0), (2,3), ...]
"""
def undo(gmap, undo_stack: list[tuple]):
    for _ in range(len(undo_stack)):
        op = undo_stack.pop()
        x,y = op[0],op[1]
        game_map.clear_block(gmap, x, y)
        
    assert undo_stack == []
        
        
def die(gmap):
    print("Result: UNSAT.")
    print(f"Caused By {game_map.string(gmap)}")
    exit(-1)