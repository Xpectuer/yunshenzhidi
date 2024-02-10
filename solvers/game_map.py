'''
Author: XPectuer
LastEditor: XPectuer
'''
TOTAL_EDGE = 5
TOTAL_BLOCKS = TOTAL_EDGE ** 2

"""
initial game map like:

-1 -1 -1 -1 -1 -1 -1
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

def set_block(game_map, i, j , v): game_map[i+1][j+1] = v

def string(game_map):
    s= ""
    for k in game_map:
        s += str(k)
        s += '\n'
    return s