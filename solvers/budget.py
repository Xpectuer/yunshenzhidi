from consts import *

def initBudget():
    budget = [0] * (TERRIAN_NUMS+1)
    budget[HERMITS] = 4
    budget[FOREST] = 4
    budget[ROAD] = 4
    budget[RIVER] = 5
    budget[VILLIAGE] = 3
    budget[PLAINS] = 5
    return budget

def copyBudget(budgets):
    return [b for b in budgets]

def consumeBudget(budgets, terrian) -> bool:
    old = budgets[terrian] 
    new = old - 1
    succ = new >= 0
    if succ:
        budgets[terrian] = new
    return succ

def restoreBudgets(budgets, terrain):
    old = budgets[terrain]
    new = old + 1
    budgets[terrain] = new 
    return new >= 0

# spec: sum(budgets) == TOTALBLOCKS
def validateBudgets(budgets):
    cnt = 0
    for e in budgets:
        cnt  += e
    assert cnt ==  TOTAL_BLOCKS

def empty(budgets):
    for budget in budgets:
        if budget != 0:
            return False
    return True