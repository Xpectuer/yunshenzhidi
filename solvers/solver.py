'''
Author: XPectuer
LastEditor: XPectuer

'''

from consts import *
import game_map, clue, utils
import copy


def initBudget():
    budget = [0] * (TERRIAN_NUMS+1)
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
        NORTH_EAST:((0,2),(n-2, n)),
        SOUTH_EAST :((n-2,n),(n-2,n)),
        SOUTH_WEST :((n-2,n),(0,2)),
        NORTH_WEST :((0,2),(0,2))
    }
    
hermit_sections = init_direction_interval_map()

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
    
    def compile_hermit_direction(gmap, ghids, car,cdr, results):
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
                    game_map.check_and_set_block(gmap, x, y, HERMITS)
                    compile(gmap, ghidsp, cdr,results)
                    game_map.check_and_set_block(gmap, x, y, EMPTY)
        
        
    def compile_hermit_common(gmap, ghids, car, cdr, results):
        if not clue.is_direction_hermit(car):
            
            curr_hid = clue.get_hermit_hids(car)[0]
            # pre-compute offset of 
            offsets = clue.get_hermit_offset(car)
            # print("offsets", offsets)
            undo_stack = []
            
            # set hermit or update
            
            for direction, id in ghids.items():
                
                interval = hermit_sections[direction]
                if curr_hid  == id:
                    print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
                    # base coordinate
                    h_bases = game_map.search_interval(gmap, HERMITS, interval)
                    
                    assert h_bases != []
                    # has hermit in indicated direction
                    h_base = h_bases[0]
                    
                    # absolute coor = (ax, ay) + (rx, ry)
                    clue.set_hermit_nearby(gmap, h_base, offsets, undo_stack)
                    
                    # continue
                    compile(gmap, ghids, cdr, results)
                    utils.undo(gmap, undo_stack=undo_stack)
                        
                        
                elif id == EMPTY: 
                    # has NO hermit in indicated direction
                    x_coor = interval[0]
                    y_coor = interval[1]
                    for x in range(*x_coor):
                        for y in range(*y_coor):
                            # print("direction, (x,y):",direction, x, y)
                            game_map.check_and_set_block(gmap, x, y, HERMITS)    
                            h_base = (x, y)
                            undo_stack.append(h_base)
                                
                            # absolute coor = (ax, ay) + (rx, ry)
                            succ = clue.set_hermit_nearby(gmap, 
                                                          h_base, 
                                                          offsets, 
                                                          undo_stack)
                            
                            if succ:
                                game_map.set_hermit_id(ghids, direction, curr_hid)
                                
                                # continue                
                                compile(gmap, ghids, cdr, results)
                                
                                # print("undo_stack", undo_stack)
                                # print(game_map.string(gmap))
                                utils.undo(gmap, undo_stack)
                                # print(game_map.string(gmap))
                                # undo game map hermit id
                                game_map.set_hermit_id(ghids, direction, EMPTY)
                            else:
                                utils.undo(gmap, undo_stack)
                    

            # if hid in ghids.values():
            #     interval = hermit_sections[]
            #     = search_inteval(gmap, interval)
                    
    
                
    def compile(gmap, ghids, clue_hermits, results):
        # dfs
        if clue_hermits == []: 
            # base case 
            r = ([x[:] for x in gmap], dict(ghids))
            print("leaf:",  show_results([r]))
            # breakpoint()
            results.append(r)
            return
        else: 
            car = clue_hermits[0]
            cdr = clue_hermits[1:]
            ctype  = clue.get_clue_type(car)
            assert ctype == CLUE_HERMIT
            # choose 1 / 2
            compile_hermit_direction(gmap, ghids, car, cdr, results)
            compile_hermit_common(gmap, ghids, car, cdr, results)
            
            
           

    # todo: test clue hermits
    chs = clues_hermits
    
    compile(game_map.init_game_map(), 
         game_map.init_hermit_ids(),
          chs, results=results)
    
    return results
    
    
    
    
def breakdown_kernels(clues):
    """
    break down multiple kernels in single clue into multiple clues
    clue([k1,k2], [i1, i2]) ==> [clue([k1], [i1]), clue([k2], [i2])]
    """
    r = []
    for c in clues:
        t = clue.get_clue_type(c)    
        
        if t == CLUE_HERMIT:
            ks = clue.get_kernels(c)
            hids = clue.get_hermit_hids(c)
            khs = zip(ks, hids)
            
            di = clue.get_hermit_direction(c)
            m = map(lambda x: clue.create_hermit_clue(t, [x[0]], [x[1]], di), khs)
            
            r.extend(m)
        else:
            r.append(c)
    return r

def show_gamemap(gmap: list[list[int]]):
    print(f"GameMap: \n{game_map.string(gmap)}")

"""
Display Result 

results: list
"""
def show_results(results:list[tuple]):
    for cnt, res in enumerate(results):
        print(f"Result ({cnt})")
        gmap = res[0]
        show_gamemap(gmap)
        h_layout = res[1]
        print(f"Hermits Layout(0 For Empty Space):\n{game_map.string_hermit_layout(h_layout)}")
        print()


"""
General Idea: BackTrack Testing

budgets: List[int],  number of each terrian
hermit_clue: 
normal_clue: 
"""
def solve(budgets, clues):
    validateBudgets(budgets)
    cluesp = breakdown_kernels(clues)
    print("AFTER PRE PROCESS:", cluesp)
    clues_hermits = clue.filter_hermits(cluesp)
    results = compile_hermits(clues_hermits)
    
    show_results(results)
    
    # print(gmap_results)
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
  
                
                
                
    #         elif type in {CLUE_BIRD, CLUE_DRYAD, CLUE_OVERLOOK}:
    #             workset.extend(k)
    #         else:
    #             assert False
    #     else:
    #         # fill up
    #         pass

def test1():
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

def test2():
    my_game_map = game_map.init_game_map()
    print(game_map.string(my_game_map))
    budgets = initBudget()
    print("budget: ",budgets)
    
    k1 = clue.create_kernel((HERMITS, (0,0)),
                            (ROAD, (1,0)))
    k2 = clue.create_kernel((FOREST, (0,0)),
                            (HERMITS, (0,1)))
    
    k3 = clue.create_kernel((HERMITS, (0,0)),
                            (RIVER,(1,0)))
    
    k4 = clue.create_kernel((HERMITS, (0,0)),
                            (VILLIAGE, (1,0)))
    
    
    hclue =  clue.create_clue(CLUE_HERMIT, 
                              kernel= [k1,k2],
                              hIds= [1, 4],
                              direction= NO_DIRECTION)
    
    hclue1 =  clue.create_clue(CLUE_HERMIT, 
                              kernel= [k3,k4],
                              hIds= [2, 3],
                              direction= NO_DIRECTION)
    solve(budgets, [hclue, hclue1])


if __name__ == '__main__':
    test1()
    test2()
    
    

