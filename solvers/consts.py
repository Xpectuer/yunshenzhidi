'''
Author: XPectuer
LastEditor: XPectuer
'''

TERRIAN_SIZE = 6
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


# direction
NORTH=0
EAST=1
SOUTH=2
WEST=3

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
