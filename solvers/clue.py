'''
Author: XPectuer
LastEditor: XPectuer
'''
from consts import *


def rot90D(kernel):
    
    pass

def expandDryadClue(kernel):
    r = []
    t = kernel
    for _ in range(4):
        r.append(t)
        t = rot90D(kernel)
        
    return r
    

def expand(clue_type, kernel):
    if clue_type == CLUE_HERMIT:
        return kernel
    elif clue_type == CLUE_BIRD:
        return kernel
    elif clue_type == CLUE_DRYAD:
        return expandDryadClue(kernel)
    elif clue_type == CLUE_OVERLOOK:
        return kernel

def create_hermit_clue(clue_type, kernel, hIds):
    assert clue_type == CLUE_HERMIT
    ex_kernel = expand(clue_type, kernel)
    return (clue_type,
            tuple(ex_kernel[0], ex_kernel[1]), 
            tuple(hIds[0], hIds[1]))


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
        return create_hermit_clue(clue_type,  kwargs['kernel'], kwargs['hIds'],)
    elif clue_type == CLUE_BIRD:
        return create_bird_clue(clue_type, kwargs['kernel'])
    elif clue_type == CLUE_DRYAD:
        return create_dryad_clue(clue_type, kwargs['kernel'])
    elif clue_type == CLUE_OVERLOOK:
        return create_overlook_clue(clue_type, kwargs['kernel'], kwargs['direction'])
        


def get_kernel(clue):
    return clue[1]


if __name__ == '__main__':
    overlook = create_clue(CLUE_OVERLOOK, kernel= [[FOREST],[PLAINS],[VILLIAGE],[RIVER]], direction=NORTH)
    dryad = create_clue(CLUE_DRYAD, kernel=[[EMPTY, VILLIAGE, EMPTY],
                                            [HERMITS, FOREST, VILLIAGE],
                                            [OUTER, OUTER, OUTER]])
    
    print(overlook)
    print(dryad)