'''
Author: XPectuer
LastEditor: XPectuer
'''

from consts import *
import budget, utils

def init_direction_interval_map():
    """
    (row_range, col_range)
    """
    n = TOTAL_EDGE + 1
    return {
        NORTH_EAST:((1,3),(n-2, n)),
        SOUTH_EAST :((n-2,n),(n-2,n)),
        SOUTH_WEST :((n-2,n),(1,3)),
        NORTH_WEST :((1,3),(1,3))
    }
    
hermit_sections = init_direction_interval_map()

"""
initial game map like:

-1 -1 -1 -1 -1 -1 -1
-1 0  0  0  0  0  -1
-1 0  0  0  0  0  -1
-1 0  0  0  0  0  -1
-1 0  0  0  0  0  -1
-1 0  0  0  0  0  -1
-1 -1 -1 -1 -1 -1 -1
"""
def init_game_map():
    game_map = [[0 for _ in range(TOTAL_EDGE+2)] for _ in range( TOTAL_EDGE + 2)]
    col_num = len(game_map)
    row_num = len(game_map[0])
    game_map[0] = [-1 for _ in range(col_num)]
    for i in range(row_num):
        game_map[i][0] = -1
        game_map[i][-1] = -1
    
    game_map[-1] = [-1 for _ in range(col_num)]
    return game_map


def get_block(game_map, i, j):
    return game_map[i][j]

def get_block_from_coor(game_map, coor):
    i = coor[0]
    j = coor[1]
    return get_block(game_map, i, j)

def validate_index(i, j):
    return (1 <= i < TOTAL_EDGE+1 and 1 <= j < TOTAL_EDGE+1)

def set_block(game_map, i, j ,v):
    game_map[i][j] = v

def clear_block(game_map, i, j): set_block(game_map, i, j, EMPTY)

# for block fill 
def check_and_place_block(game_map, budgets, i, j , terrian) -> bool: 
    if terrian == HERMITS:
        inHermit = False
        for _, section in hermit_sections.items():
            inHermit = inHermit or utils.coor_in((i,j), section)
        return inHermit and place_inner(game_map, budgets, i, j , terrian)
    else:
        return place_inner(game_map, budgets, i, j, terrian)

# place inner
def place_inner(game_map, budgets, i, j , terrian):
    inBound = validate_index(i, j) 
    if inBound:
        avai = get_block(game_map, i, j) == EMPTY 
        if avai:
            set_block(game_map, i, j, terrian)
            return budget.consumeBudget(budgets, terrian)
    else:
        return False

# for clue fill
def check_and_set_block(game_map, budgets, i, j , terrian) -> bool: 
    if terrian == OUTER:
        return set_outer(i,j)
    elif terrian == HERMITS:
        
        inHermit = False
        for _, section in hermit_sections.items():
            inHermit = inHermit or utils.coor_in((i,j), section)
        return inHermit and set_inner(game_map, budgets, i, j , terrian)
    else:
        return set_inner(game_map, budgets, i, j, terrian)



def set_inner(game_map, budgets, i, j, terrian) -> bool:
    inBound = validate_index(i, j) 

    if inBound:
        avai = get_block(game_map, i, j) == EMPTY 
        isOverride = get_block(game_map, i, j) == terrian
        if isOverride:    
            return True
        elif avai:
            set_block(game_map, i, j, terrian)
            # budget > 0
            return budget.consumeBudget(budgets, terrian)
    else:
        return False

def set_outer(i, j) -> bool:
    inBound = validate_index(i, j) 
    if not inBound:
        return True
    else:
        return False
    
# def set_block(game_map, coor , v): 
#     i = coor[0]
#     j = coor[1]
#     assert validate_index(i, j)
#     game_map[i+1][j+1] = v

def inbound(i, j):
    return validate_index(i,j) 

def copy_gmap(gmap)->list[list]:
    return [x[:] for x in gmap]

# def set_block_relative(game_map, base, relative_coor, v):
#     i = base[0] + relative_coor[0]
#     j = base[1] + relative_coor[1]
#     set_block(game_map, i, j, v)



def init_hermit_ids():
    return {
        NORTH_EAST : EMPTY,
        SOUTH_EAST : EMPTY,
        SOUTH_WEST : EMPTY,
        NORTH_WEST : EMPTY
    }
    
def set_hermit_id(hids, direction, id):
    hids.update({direction:id})
    
def get_hermit_id(hids, direction):
    return hids[direction]

def is_hermit_id_empty(hids, direction):
    return get_hermit_id(hids, direction) == EMPTY
    

def search_interval(game_map, terrain, interval) -> list[tuple]:
    int_x = interval[0]
    int_y = interval[1]
    r = []
    for x in range(*int_x):
        for y in range(*int_y):
            if get_block(game_map, x, y) == terrain:
                r.append((x,y))
    
    return r

def string(game_map):
    s= ""
    for k in game_map:
        ts = ""
        for e in k:
            ts += f"{e:>5}"
        s += ts
        s += '\n'
    return s

def string_hermit_layout(hids):
    r = "{"
    for direction, id in hids.items():
        s_dire = GetDirectionDesc(direction)
        r += f"{s_dire}:{id}|"
    
    return r.strip("|") + "}"