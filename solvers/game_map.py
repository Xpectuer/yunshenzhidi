'''
Author: XPectuer
LastEditor: XPectuer
'''

from consts import *
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
    return game_map[i+1][j+1]

def get_block_from_coor(game_map, coor):
    i = coor[0]
    j = coor[1]
    return get_block(game_map, i, j)

def validate_index(i, j):
    return (0 <= i < TOTAL_EDGE and 0 <= j < TOTAL_EDGE)

def set_block(game_map, i, j ,v):
    game_map[i+1][j+1] = v

def clear_block(game_map, i, j): set_block(game_map, i, j, EMPTY)

def check_and_set_block(game_map, i, j , v) -> bool: 
    succ = validate_index(i, j) and \
        get_block(game_map, i, j) == EMPTY
    
    if succ:
        game_map[i+1][j+1] = v
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
    
    

def search_interval(game_map, terrain, interval):
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