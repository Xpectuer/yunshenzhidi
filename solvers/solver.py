'''
Author: XPectuer
LastEditor: XPectuer

'''

from consts import *
import game_map, clue, utils
# ==========================================================


def initBudget():
    budget = [0] * TERRIAN_NUMS
    budget[HERMITS] = 4
    budget[FOREST] = 4
    budget[ROAD] = 4
    budget[RIVER] = 5
    budget[VILLIAGE] = 3
    budget[PLAINS] = 5
    return budget

def init_direction_interval_map():
    """
    (row_range, col_range)
    """
    n = TOTAL_EDGE
    return {
        NORTH_EAST:((0,1),(n-2, n-1)),
        SOUTH_EAST :((n-2,n-1),(n-2,n-1)),
        SOUTH_WEST :((n-2,n-1),(0,1)),
        NORTH_WEST :((0,1),(n-2,n-1))
    }
    
hermit_sections = init_direction_interval_map()


def init_hermit_ids():
    return {
        NORTH_EAST : EMPTY,
        SOUTH_EAST : EMPTY,
        SOUTH_WEST : EMPTY,
        NORTH_WEST : EMPTY
    }
    
def set_hermit_id(hids, direction, id):
    hids[direction] = id

def get_hermit_id(hids, direction):
    return hids[direction]


# spec: sum(budgets) == TOTALBLOCKS
def validateBudgets(budgets):
    cnt = 0
    for e in budgets:
        cnt  += e
    assert cnt ==  TOTAL_BLOCKS

def consumeBudget(budgets, kernel):
    for cs in kernel:
        for e in cs:
            budgets[e] -= 1
            if budgets[e] < 0:
                return False
            
    return True



def isBudEmpty(budget):
    return sum(budget) == 0
    
def compile_hermits(clues_hermits):
    """
    A function \f that takes hermit_clues
    and outputs gmap filled by possible hermits (gmap, direction)
    """
    # ...
    results = []
    
    def compile_hermit_direction(gmap, ghids, car, cdr):
        if clue.is_direction_hermit(car):
            hids = clue.get_hermit_hids(car)
            direction = clue.get_hermit_direction(car)
            interval = hermit_sections[direction]
            x_range = interval[0]
            y_range = interval[1]
            hid = hids[0]
            ghidsp = set_hermit_id(ghids, direction, hid)
            for x in range(*x_range):
                for y in range(*y_range):
                    game_map.set_block(gmap, x, y, HERMITS)
                    compile(gmap, ghidsp, cdr)
                    game_map.set_block(gmap, x, y, EMPTY)


    def compile_hermit_common(gmap, ghids, car, cdr):
        if not clue.is_direction_hermit(car):
            k =clue.get_kernel(car)
            for direction, ghid in ghids:
                # todo
                
                
                

    def compile(gmap, ghids, clue_hermits):
        # dfs
        if clue_hermits == []: 
            # base case 
            results.append((gmap, ghids))
            return
        else: 
            # recursion
            car = clue_hermits[0]
            cdr = clue_hermits[1:]
            ctype  = clue.get_clue_type(car)
            assert ctype == CLUE_HERMIT
            
            compile_hermit_direction(gmap, ghids, car, cdr)
            compile_hermit_common(gmap, ghids, car, cdr)
           
        
    # todo: test clue hermits
    chs = []
    compile(game_map= game_map.init_game_map(), 
          ghids= init_hermit_ids(),
          clue_hermits= chs)
    
    
def pre_process(clues):
    r = []
    for c in clues:
        t = clue.get_clue_type(c)    
        
        if t == CLUE_HERMIT:
            ks = clue.get_kernel(c)
            hids = clue.get_hermit_hids(c)
            di = clue.get_hermit_direction(c)
            m = map(lambda x: clue.create_hermit_clue(t, [x], hids, di), ks)
            r.extend(m)
        else:
            r.append(c)
    return r

"""
General Idea: BackTrack Testing

budgets: List[int],  number of each terrian
hermit_clue: 
normal_clue: 
"""
def solve(budgets, clues):
    validateBudgets(budgets)
    cluesp = pre_process(clues)
    print("CLUESP:", cluesp)
    assert False
    clues_hermits = list(filter(lambda x: clue.get_clue_type(x) == HERMITS, cluesp))
    gmap_results = compile_hermits(clues_hermits_p)
    # def inner(gmap, budgets, hermitset , workset, clues):
    #     """
    #     gmap: game map 
    #     budgets: 
    #     workset: set of clues in kernel
        
    #     """
    #     # base case 
    #     if isBudEmpty(budgets):
    #         print(gmap)
    #         return
        
        
    #     if clues != []:
    #         # merge possible clues
    #         clue = clues[0]
    #         type = clue.get_clue_type(clue)
    #         k = get_kernel(clue)
    #         if type == CLUE_HERMIT:
    #             hermitset.extend(list(k))
    #             # todo: k0 = k[0]
                
                
                
    #         elif type in {CLUE_BIRD, CLUE_DRYAD, CLUE_OVERLOOK}:
    #             workset.extend(k)
    #         else:
    #             assert False
    #     else:
    #         # fill up
    #         pass

if __name__ == '__main__':
    my_game_map = game_map.init_game_map()
    print(game_map.string(my_game_map))
    budgets = initBudget()
    print("budget: ",budgets)
    
    k1 = clue.create_kernel((HERMITS, (0,0)),
                            (ROAD, (1,0)))
    k2 = clue.create_kernel((FOREST, (0,0)),
                            (HERMITS, (0,1)))
    
    hclue =  clue.create_clue(CLUE_HERMIT, 
                              kernel= [k1,k2],
                              hIds= [1, 2],
                              direction= NO_DIRECTION)
    solve(budgets, [hclue])
    

