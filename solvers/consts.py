'''
Author: XPectuer
LastEditor: XPectuer
'''

TOTAL_EDGE = 5
TOTAL_BLOCKS = TOTAL_EDGE ** 2

TERRIAN_NUMS = 6
# terrain 地形：
# 隐者
HERMITS=0 
# 森林
FOREST=1
# 道路
ROAD=2
# 河流
RIVER=3
# 村庄
VILLIAGE=4
# 平原
PLAINS= 5
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




enum_to_str_map = {
    HERMITS:"隐者",
    FOREST:"森林",
    ROAD:"道路",
    RIVER:"河流",
    VILLIAGE:"村庄",
    PLAINS:"平原"
}

def GetTerrainDesc(terrain):
    return enum_to_str_map[terrain]


