'''
Author: XPectuer
LastEditor: XPectuer

'''

from consts import *
import game_map

# ==========================================================


def initBudget():
    budget = [0] * TERRIAN_SIZE
    budget[HERMITS] = 4
    budget[FOREST] = 4
    budget[ROAD] = 4
    budget[RIVER] = 5
    budget[VILLIAGE] = 3
    budget[PLAINS] = 5
    return budget

# spec: sum(budgets) == TOTALBLOCKS
def validateBudgets(budgets):
    cnt = 0
    for e in budgets:
        cnt  += e
    assert cnt ==  game_map.TOTAL_BLOCKS

"""
budgets: List[int],  number of each terrian
hermit_clue: 
normal_clue: 
"""
def solve(budgets, hermit_clue, normal_clue):
    validateBudgets(budgets)




if __name__ == '__main__':
    my_game_map = game_map.init_game_map()
    print(game_map.string(my_game_map))
    budgets = initBudget()
    print("budget: ",budgets)
    solve(budgets)
    

