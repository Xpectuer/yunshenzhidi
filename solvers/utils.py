import itertools
import game_map
from consts import *
import budget

def binon(collection, N):
    # Get all combinations of size N
    combinations = list(itertools.combinations(collection, N))
    return combinations

def flatMap(func, iterable):
    return list(itertools.chain.from_iterable(map(func, iterable)))

def flatten(iterable):
    return flatMap(lambda x: x, iterable)

def coor_diff(a, b):
    # print(a,b)
    return (a[0]- b[0], a[1]- b[1])

def coor_add(a,b):
    return (a[0] + b[0], a[1] + b[1])

def traverse_interval_2d(f, interval):
    x_coor = interval[0]
    y_coor = interval[1]
    for x in range(*x_coor):
        for y in range(*y_coor):
            f(x,y)

def coor_in(coor, _range):
    return coor[0] in range(*_range[0]) and coor[1] in range(*_range[1])

def saveState(gmap, budgets):
    return (game_map.copy_gmap(gmap), budget.copyBudget(budgets))

def get_combine_from_range(lower_bound, upper_bound):
    ret = []
    assert lower_bound < upper_bound
    for l in range(lower_bound, upper_bound):
        for r in range(l+1, upper_bound):
            ret.append((l,r))
        
    return ret

def filter_range(_ranges: list[tuple], *constraints):
    """
    constraints: ((x0, x1),(y0, y1))
    """
    t = _ranges
    for constraint in constraints:
        sat = []
        low, high = constraint
        for _range in t:
            x , y = _range
            if x in range(*low) and y in range(*high):
                sat.append(_range)
            t = sat
    return t
# def restoreState(gmap, oldMap, budgets, oldB):
#     oldMap
#     budgets = oldB

"""
undo_stack: [(0,0), (2,3), ...]
"""
# def undo(gmap,budgets, undo_stack: list[tuple]):
#     for _ in range(len(undo_stack)):
#         op = undo_stack.pop()
#         x,y = op[0],op[1]
        
#         terrain = game_map.get_block(gmap, x, y)
#         budget.restoreBudgets(budgets, terrain)
        
#         game_map.clear_block(gmap, x, y)
        
#     assert undo_stack == []
        
        
def die(gmap):
    print("Result: UNSAT.")
    print(f"Caused By {game_map.string(gmap)}")
    exit(-1)
    
    
if __name__ == '__main__':
    t = get_combine_from_range(3,5)
    print(t)
    x1 = filter_range(t, ((2,4),(4,5)))
    
    x2 = filter_range(t, ((0,2),(4,5)))
    
    print(x1, x2)
    
    
    
    
    