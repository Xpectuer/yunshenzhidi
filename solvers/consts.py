'''
Author: XPectuer
LastEditor: XPectuer
'''

TOTAL_EDGE = 5
TOTAL_BLOCKS = TOTAL_EDGE ** 2

TERRIAN_NUMS = 6
# terrain 地形：
# 隐者
HERMITS=1 
# 森林
FOREST=2
# 道路
ROAD=3
# 河流
RIVER=4
# 村庄
VILLIAGE=5
# 平原
PLAINS= 6
# 地图外
OUTER = -1
# empty
EMPTY = 0

# clue
# 隐士
CLUE_HERMIT = 0
# 飞鸟
CLUE_BIRD = 1
# 树灵
CLUE_DRYAD = 2
# 极目
CLUE_OVERLOOK = 3

# 树灵，旋转后
CLUE_DRYAD_ROT = 4
# 极目，放置隐者后
CLUE_OVERLOOK_PLACED = 5

# set 

SET_SUCC = 0
SET_SAME = 1
SET_FAIL = 2

# directions
NO_DIRECTION=-1
NORTH=0
NORTH_EAST= 1
EAST=2
SOUTH_EAST = 3 
SOUTH= 4
SOUTH_WEST = 5
WEST= 6
NORTH_WEST = 7

terrian_to_str_map = {
    HERMITS:"隐者",
    FOREST:"森林",
    ROAD:"道路",
    RIVER:"河流",
    VILLIAGE:"村庄",
    PLAINS:"平原"
}

direction_to_str_map  = {
    NO_DIRECTION: '无方向',
    NORTH: '北',
    NORTH_EAST: '东北',
    EAST: '东',
    SOUTH_EAST: '东南',
    SOUTH: '南',
    SOUTH_WEST: '西南',
    WEST: '西',
    NORTH_WEST: '西北'
}


def GetTerrainDesc(terrain: int):
    return terrian_to_str_map[terrain]

def GetDirectionDesc(direction: int) -> str:
    return direction_to_str_map[direction]    


