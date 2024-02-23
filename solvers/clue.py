'''
Author: XPectuer
LastEditor: XPectuer
'''
from consts import *
import utils, game_map, budget



def filter_hermits(clues):
    return list(filter(lambda x: get_clue_type(x) == CLUE_HERMIT, clues))

def create_hermit_clue(clue_type, kernel, hIds, direction):
    assert clue_type == CLUE_HERMIT

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
    # print("AAA", hermit_clue, get_hermit_direction(hermit_clue))
    return get_hermit_direction(hermit_clue) != NO_DIRECTION

def get_hermit_offset(hermit_clue):
    kernels = get_kernels(hermit_clue)
    hcoor = (-1, -1)
    for k in kernels:
        for t in k:
            # print("t:", t)
            if get_terrain_type(t) == HERMITS:
                hcoor = get_terrain_coor(t)
                break
    
    assert hcoor != (-1, -1)
    
    offsets = []
    for k in kernels:
        for t in k:
            ttype = get_terrain_type(t)
            if  ttype != HERMITS:
                tcoor = get_terrain_coor(t)
                offst = utils.coor_diff(tcoor, hcoor)
                offsets.append(create_terrian(ttype, offst))
            
    return offsets

def set_hermit_nearby(gmap, budgets, h_base, offsets) -> bool:
    for t_offst in offsets:
        terrain_type = get_terrain_type(t_offst)
        offst_coor = get_terrain_coor(t_offst)
        absolute_coor = utils.coor_add(h_base, offst_coor)
        
        success = game_map.check_and_set_block(gmap, budgets,
                                               absolute_coor[0],
                                               absolute_coor[1],
                                               terrain_type)
        if not success:
            return False
        
    return True

def set_kernel(gmap, budgets, abs_base, base, offsets) -> bool:
    
    base_type = get_terrain_type(base)
    
    success = game_map.check_and_set_block(gmap, budgets,
                                            abs_base[0],
                                            abs_base[1],
                                            base_type)
    if not success:
     
        return False
        
    for t_offst in offsets:
        terrain_type = get_terrain_type(t_offst)
        offst_coor = get_terrain_coor(t_offst)
        absolute_coor = utils.coor_add(abs_base, offst_coor)
        
        success = game_map.check_and_set_block(gmap, budgets,
                                               absolute_coor[0],
                                               absolute_coor[1],
                                               terrain_type)
        if not success:
            return False
        
    return True
    
def create_bird_clue(clue_type, kernel):
    assert clue_type == CLUE_BIRD 

    
    return (clue_type, kernel)

def search_hermit_from_clue(kernel) -> list[tuple]:
    hermit_idxs = []
    for idx, t in enumerate(kernel):
        if get_terrain_type(t) == HERMITS:
            hermit_idxs.append(idx)
    
    # option unpack
    assert len(hermit_idxs) <= 1
    return hermit_idxs
        
        
        

def get_bird_alternative(clue_bird):
    ks = get_kernels(clue_bird)
    assert len(ks) == 1
    k = ks[0]
     # get hermit indices
    hermit_idxs = search_hermit_from_clue(k)
    
    if len(hermit_idxs) == 1:
        hermit_idx = hermit_idxs[0]
        hermit = k[hermit_idx]
        
        coor = get_terrain_coor(hermit)
        new_k = [_ for _ in k]
        new_k[hermit_idx] = (PLAINS, coor)
        c1 = create_clue(CLUE_BIRD, kernel=[new_k])
    
    return c1

"""
forests are NOT neighbors
"""
def get_forest_idxs(clue_dryad):
    ks = get_kernels(clue_dryad)
    assert len(ks) == 1
    k = ks[0]
    
    r = []
    for t in k:
        if get_terrain_type(t) == FOREST:
            r.append(t)
    
    return r

def rotate_coordinates(matrix, edge_num = 3):
    n = edge_num ** 2
    return [(y, n-x-1) for x, y in matrix]

"""

  1              3
3 2 5 ======>  4 2 1
  4              5
"""
def draydRot90D(clue_dryad):
    _type = get_clue_type(clue_dryad)
    assert _type == CLUE_DRYAD \
        or _type == CLUE_DRYAD_ROT
        
    ks = get_kernels(clue_dryad)
    assert len(ks) == 1
    k = ks[0]
    # get hermit indices
    
    forest_idxs = get_forest_idxs(clue_dryad)
    print(forest_idxs)
    assert len(forest_idxs) == 1
    
    coors = map(lambda t: get_terrain_coor(t), k)
    terrain_types = map(lambda t: get_terrain_type(t), k)
    
    coors_p = rotate_coordinates(coors)
    
    terrains_p = zip(terrain_types, coors_p)
    
    k = create_kernel(*terrains_p)
    
    return create_clue(CLUE_DRYAD_ROT, kernel=[k])
            
# buggy
def get_drayd_rot_default(clue_dryad) :
    assert get_clue_type(clue_dryad) == CLUE_DRYAD
    ks = get_kernels(clue_dryad)
    
    r = create_clue(CLUE_DRYAD_ROT, kernel=ks)
    
    return r

def get_overlook_placed_default(clue_dryad):
    assert get_clue_type(clue_dryad) == CLUE_OVERLOOK
    ks = get_kernels(clue_dryad)
    
    r = create_clue(CLUE_OVERLOOK, kernel=ks)
    
    return r


def get_dryad_alternatives(clue_dryad) -> list:
    
    cluep = get_drayd_rot_default(clue_dryad)
    r = [cluep]
    
    for _ in range(3):
        cluek = draydRot90D(cluep)
        r.append(cluek)
        cluep = cluek
        
    
    return r
    
def kernel_has_terrain(kernel, terrain):
    n = filter(lambda t: get_terrain_type(t) == terrain, kernel)
    return n > 0

# todo
def get_overlook_alternatives(car) -> list:
    ks = get_kernels(car)
    assert len(ks) == 1
    k = ks[0]
    n_terrains = len(k)
    if kernel_has_terrain(kernel, FOREST):
        if n_terrains == TOTAL_EDGE:
            return get_overlook_placed_default(car)
        elif n_terrains == TOTAL_EDGE - 1:
            pass
        
        
        

def create_dryad_clue(clue_type, kernel):
    assert clue_type == CLUE_DRYAD or clue_type == CLUE_DRYAD_ROT
    return (clue_type, kernel)


def create_overlook_clue(clue_type, kernel, direction):
    assert clue_type == CLUE_OVERLOOK or clue_type == CLUE_OVERLOOK_PLACED
    
    return (clue_type, kernel, direction)


def create_clue(clue_type, **kwargs):
    if clue_type == CLUE_HERMIT:
        return create_hermit_clue(clue_type,  kwargs['kernel'], kwargs['hIds'], kwargs['direction'])
    elif clue_type == CLUE_BIRD :
        return create_bird_clue(clue_type, kwargs['kernel'])
    elif clue_type == CLUE_DRYAD or clue_type == CLUE_DRYAD_ROT:
        print("clue_type", clue_type, "deadbeef:", kwargs)
        return create_dryad_clue(clue_type, kwargs['kernel'])
    elif clue_type == CLUE_OVERLOOK or clue_type == CLUE_OVERLOOK_PLACED:
        return create_overlook_clue(clue_type, kwargs['kernel'], kwargs['direction'])
    else:
        assert False 
     
def get_clue_type(clue):
    return clue[0]

def get_kernels(clue):
    return clue[1]

def create_kernel(k1, *args):
    return [k1] + list(args)

def kernel_has_hermit(kernel):
    for terrian in kernel:
        if get_terrain_type(terrian) == HERMITS:
            return True
    return False

def copy_kernel(k: list):
    return [terrain for terrain in k]

def get_kernel_offsets(kernel: list[tuple]):
    assert kernel != []
    base_terrian = kernel[0]
    base_terrian_rel_coor = get_terrain_coor(base_terrian)
    base_terrian_type = get_terrain_type(base_terrian)
    rest = kernel[1:]
    
    ret = []
    
    for terrain in rest:
        _type = get_terrain_type(terrain)
        rel_coor = get_terrain_coor(terrain)
        offst = utils.coor_diff(rel_coor, base_terrian_rel_coor)
        ret.append(create_terrian(_type, offst))
    
    return create_terrian(base_terrian_type, (-1, -1)), ret

def get_terrain_type(terrian) -> int:
    return terrian[0]

def get_terrain_coor(terrain) -> tuple:
    return terrain[1]

def create_terrian(ttype, coor) -> tuple:
    return (ttype, coor)

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

