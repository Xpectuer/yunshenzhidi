'''
Author: XPectuer
LastEditor: XPectuer
'''
from consts import *
from game_map import TOTAL_EDGE
"""

  1              3
3 2 5 ======>  4 2 1
  4              5
"""
def rot90D(kernel):
    n = 3
    newK = [[0 for _ in range(n)]for _ in range(n)]
    # flip up-down
    for i, e in enumerate(kernel):
        for j, ee in enumerate(e):
            newK[j][n-i-1] = kernel[i][j]

    return newK


def expandDryadClue(kernel):
    r = []
    t = kernel
    for _ in range(4):
        r.append(t)
        t = rot90D(t)
        
    return r
    
def expandOverLookClue(kernel):
    return kernel

def expand(clue_type, kernel):
    if clue_type == CLUE_HERMIT:
        return kernel
    elif clue_type == CLUE_BIRD:
        return kernel
    elif clue_type == CLUE_DRYAD:
        return expandDryadClue(kernel)
    elif clue_type == CLUE_OVERLOOK:
        return expandOverLookClue(kernel)

def create_hermit_clue(clue_type, kernel, hIds, direction):
    assert clue_type == CLUE_HERMIT
    ex_kernel = expand(clue_type, kernel)
    return (clue_type,
            kernel, 
            hIds,
            direction)

def get_hermit_hids(hermit_clue):
    assert get_clue_type(hermit_clue) == CLUE_HERMIT
    return hermit_clue[2]

def get_hermit_direction(hermit_clue):
    assert get_clue_type(hermit_clue) == CLUE_HERMIT
    return hermit_clue[3]

def is_direction_hermit(hermit_clue):
    assert get_clue_type(hermit_clue) == CLUE_HERMIT
    return get_hermit_direction(hermit_clue) == NO_DIRECTION

 
def create_bird_clue(clue_type, kernel):
    assert clue_type == CLUE_BIRD

    ex_kernel = expand(clue_type, kernel)
    return (clue_type, ex_kernel)

def create_dryad_clue(clue_type, kernel):
    assert clue_type == CLUE_DRYAD
    ex_kernel = expand(clue_type, kernel)
    return (clue_type, ex_kernel)


def create_overlook_clue(clue_type, kernel, direction):
    assert clue_type == CLUE_OVERLOOK
    ex_kernel = expand(clue_type, kernel)
    return (clue_type, ex_kernel, direction)


def create_clue(clue_type, **kwargs):
    
    if clue_type == CLUE_HERMIT:
        return create_hermit_clue(clue_type,  kwargs['kernel'], kwargs['hIds'], kwargs['direction'])
    elif clue_type == CLUE_BIRD:
        return create_bird_clue(clue_type, kwargs['kernel'])
    elif clue_type == CLUE_DRYAD:
        return create_dryad_clue(clue_type, kwargs['kernel'])
    elif clue_type == CLUE_OVERLOOK:
        return create_overlook_clue(clue_type, kwargs['kernel'], kwargs['direction'])
        
def get_clue_type(clue):
    return clue[0]

def get_kernel(clue):
    return clue[1]

def create_kernel(k1, *args):
    return [k1] + list(args)


if __name__ == '__main__':
    overlook = create_clue(CLUE_OVERLOOK, kernel= [[FOREST],[PLAINS],[VILLIAGE],[RIVER]], direction=NORTH)
    dryad = create_clue(CLUE_DRYAD, kernel=[[EMPTY, VILLIAGE, EMPTY],
                                            [HERMITS, FOREST, VILLIAGE],
                                            [OUTER, OUTER, OUTER]])
    
    print(overlook)
    print(dryad)
    
    kernel = [
    [0,1,0],
    [3,2,5],
    [0,4,0],
    ]

