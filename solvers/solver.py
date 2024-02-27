'''
Author: XPectuer
LastEditor: XPectuer

'''

from consts import *
import game_map, clue, utils
import copy, budget


def set_hermit_id(hids, direction, id):
    hids[direction] = id

def get_hermit_id(hids, direction):
    return hids[direction]


def isBudEmpty(budget):
    return sum(budget) == 0

def compile_hermits(clues_hermits, budgets):
    """
    A function \f that takes hermit_clues
    and outputs gmap filled by possible hermits (gmap, direction)
    """
    # ...
    results = []
    
    def compile_hermit_direction(gmap, ghids, budgets, car, cdr, results) -> bool:
        
        if clue.is_direction_hermit(car):
            hids = clue.get_hermit_hids(car)
            direction = clue.get_hermit_direction(car)
            interval = game_map.hermit_sections[direction]
            x_range = interval[0]
            y_range = interval[1]
            hid = hids[0]
            # undo_stack = []
            
            
            if game_map.is_hermit_id_empty(ghids, direction) :
                old_gmap = game_map.copy_gmap(gmap)
                oldB = budget.copy(budgets)
                ghidsp = set_hermit_id(ghids, direction, hid)
            
                for x in range(*x_range):
                    for y in range(*y_range):
                       
                        succ = game_map.check_and_set_block(gmap, budgets, x, y, HERMITS)
                        # undo_stack.append((x,y))
                        if succ:
                            compile(gmap, ghidsp, budgets, cdr,results)
                        gmap = old_gmap
                        budgets = oldB
                        
            elif game_map.get_hermit_id(ghids, direction) == hid:
                compile(gmap, ghids, budgets, cdr, results)
        
        # todo: game map         
        
    def compile_hermit_common(gmap, ghids, budgets, car, cdr, results):
        if not clue.is_direction_hermit(car):
            
            curr_hid = clue.get_hermit_hids(car)[0]
            # pre-compute offset of 
            offsets = clue.get_hermit_offset(car)
            # print("offsets", offsets)
            # undo_stack = []
            
            # set hermit or update
            
            for direction, id in ghids.items():
                old = game_map.copy_gmap(gmap)
                oldB = budget.copyBudget(budgets)
                interval = game_map.hermit_sections[direction]
                if curr_hid  == id:
                    # base coordinate
                    h_bases = game_map.search_interval(gmap, HERMITS, interval)
                    
                    assert h_bases != []
                    # has hermit in indicated direction
                    h_base = h_bases[0]
                    
                    # absolute coor = (ax, ay) + (rx, ry)
                    succ = clue.set_hermit_nearby(gmap, budgets, h_base, offsets)
                    if succ:
                        # continue
                        compile(gmap, ghids, budgets, cdr, results)
                        gmap = old
                        budgets = oldB
                         
                        
                elif id == EMPTY: 
                    # has NO hermit in indicated direction
                    x_coor = interval[0]
                    y_coor = interval[1]
                    
                    for x in range(*x_coor):
                        for y in range(*y_coor):
                            old = game_map.copy_gmap(gmap)
                            oldB = budget.copyBudget(budgets)
                            # print("direction, (x,y):",direction, x, y)
                            game_map.check_and_set_block(gmap, budgets, x, y, HERMITS)    
                            h_base = (x, y)
                            # undo_stack.append(h_base)
                                
                            # absolute coor = (ax, ay) + (rx, ry)
                            succ = clue.set_hermit_nearby(gmap, 
                                                          budgets,
                                                          h_base, 
                                                          offsets)
                            
                            if succ:
                                game_map.set_hermit_id(ghids, direction, curr_hid)
                                # continue                
                                compile(gmap, ghids, budgets, cdr, results)
                                
                                # print("undo_stack", undo_stack)
                                # print(game_map.string(gmap))
                                
                                # print(game_map.string(gmap))
                                # undo game map hermit id
                                game_map.set_hermit_id(ghids, direction, EMPTY)
                           
                            gmap = old
                            budgets = oldB
                    
                    
    
                
    def compile(gmap, ghids, budgets, clue_hermits, results):
        # dfs
        if clue_hermits == []: 
            # base case 
            r = (game_map.copy_gmap(gmap), dict(ghids), [_ for _ in budgets])
            # print("leaf:",  show_results([r]))
            # breakpoint()
            results.append(r)
            return
        else: 
            car = clue_hermits[0]
            cdr = clue_hermits[1:]
            ctype  = clue.get_clue_type(car)
            assert ctype == CLUE_HERMIT
            # choose 1 / 2
            compile_hermit_direction(gmap, ghids, budgets, car, cdr, results)
            compile_hermit_common(gmap, ghids,budgets, car, cdr, results)
            
            
           

    # todo: test clue hermits
    chs = clues_hermits
    
    compile(game_map.init_game_map(), 
         game_map.init_hermit_ids(),
         budgets, chs, results=results)
    
    return results
    
    
def breakdown_bird(c, r: list):
    """
    SEE HERMIT AS PLAIN
    """
    ks = clue.get_kernels(c)
    assert len(ks) == 1
    
    k = ks[0]
    # get hermit indices
    hermit_idxs = clue.search_hermit_from_clue(k)
    
    if len(hermit_idxs) == 1:
        hermit_idx = hermit_idxs[0]
        hermit = k[hermit_idx]
        
        coor = clue.get_terrain_coor(hermit)
        new_k = [_ for _ in k]
        new_k[hermit_idx] = (PLAINS, coor)
        c1 = clue.create_clue(CLUE_BIRD, kernel=[new_k])
        r.extend([c, c1])

def breakdown_hermit(c,r:list): 
    ks = clue.get_kernels(c)
    if ks != []:
        hids = clue.get_hermit_hids(c)
        khs = zip(ks, hids)
        
        di = clue.get_hermit_direction(c)
        m = map(lambda x: clue.create_hermit_clue(CLUE_HERMIT, [x[0]], [x[1]], di), khs)
        
        r.extend(m)
    elif ks == []:
        r.append(c)

def breakdown_kernels(clues)-> list[list]:
    """
    break down multiple kernels in single clue into multiple clues
    clue([k1,k2], [i1, i2]) ==> [clue([k1], [i1]), clue([k2], [i2])]
    """
    
    r = []
    for c in clues:
        t = clue.get_clue_type(c)    
        if t == CLUE_HERMIT:
            breakdown_hermit(c, r)          
        elif t == CLUE_BIRD:
            
            
            r.append(c)
            
            #breakdown_bird(c, r) 
        else:
            r.append(c)
    return r




def compile_others(gmap, hids, budgets, clues_rest):
    
    def opt_hermit(gmap, ghids, budgets, car, cdr, results):
        for dire , ghid in ghids.items():
            if ghid != EMPTY:
                interval = game_map.hermit_sections[dire]
                option_hermit_pos = game_map.search_interval(gmap, HERMITS, interval)
                
                assert len(option_hermit_pos) == 1
                hermit_pos = option_hermit_pos[0]
                
                offsets = clue.get_hermit_offset(car)
                
                old = game_map.copy_gmap(gmap)
                oldB = budget.copyBudget(budgets)
                succ = clue.set_hermit_nearby(gmap, budgets, hermit_pos, offsets)
                
                if succ:
                    compile(gmap, ghids, budgets, cdr, results)
                gmap = old
                budgets = oldB
        
    def place_common_clue(gmap, ghids, budgets, car, cdr, results):
        ks = clue.get_kernels(car)
        assert len(ks) == 1
        k = ks[0]
        base, offsets = clue.get_kernel_offsets(k)
        
        # enumerate including outer edge
        for x, row in enumerate(gmap):
                for y, t in enumerate(row):
                    if t == EMPTY or t == clue.get_terrain_type(base):
                        old = game_map.copy_gmap(gmap)
                        oldB = budget.copyBudget(budgets)
                        # print("offsets:", offsets)
                        succ = clue.set_kernels(gmap, budgets, (x,y), base, offsets)
                        
                        if succ:
                            compile(gmap, ghids, budgets, cdr, results)
                        gmap = old 
                        budgets = oldB
        
        
    def compile(gmap, ghids, budgets, clues_rest, results):
       
        if clues_rest == []: 
            
            # base case 
            r = (game_map.copy_gmap(gmap), dict(ghids), [_ for _ in budgets])
            # print("leaf:",  show_results([r]))
            # breakpoint()
            results.append(r)
            return
        else:
            car = clues_rest[0]
            cdr = clues_rest[1:]
            _type = clue.get_clue_type(car)
            ks = clue.get_kernels(car)
            #print("car:", car,"ks:", ks)
            assert len(ks) == 1
            k = ks[0]
        
            base, offsets = clue.get_kernel_offsets(k)
            
            # extend special
            if _type == CLUE_BIRD:         
                
                """
                hermit seen as plains
                """
                if clue.kernel_has_hermit(k):
                    
                    old = game_map.copy_gmap(gmap)
                    oldB = budget.copyBudget(budgets)
                    opt_hermit(gmap, ghids, budgets, car, cdr, results)
                    gmap = old
                    budgets = oldB
                    
                    alter = clue.get_bird_alternative(car)
                    # print("ALTER:",  z alter)
                    
                    compile(gmap, ghids, budgets, [alter] +cdr , results)
                    gmap = old
                    budgets = oldB

                else:
                    place_common_clue(gmap, ghids, budgets, car, cdr, results)
                   

            elif _type == CLUE_DRYAD:
                old = game_map.copy_gmap(gmap)
                oldB = budget.copyBudget(budgets)
                alters = clue.get_dryad_alternatives(car)
                for alt in alters:
                    # print("alter:", alt)
                    gmap = old
                    budgets = oldB
                
                    compile(gmap, ghids, budgets, [alt] + cdr, results)
                    gmap = old
                    budgets = oldB    
                    # print("ALTER:", alter)        
                    
            elif _type == CLUE_DRYAD_ROT:
                if clue.kernel_has_hermit(k):
                    old = game_map.copy_gmap(gmap)
                    oldB = budget.copyBudget(budgets)
                    opt_hermit(gmap, ghids, budgets, car, cdr, results)
                    gmap = old
                    budgets = oldB
                    
                else:
                    place_common_clue(gmap, ghids, budgets, car, cdr, results)
              
                    
            elif _type == CLUE_OVERLOOK:
                
                alters = clue.get_overlook_alternatives(car)
                print("ALTERS:", alters)
                for alt in alters:
                    # print("alter:", alt)
                    old = game_map.copy_gmap(gmap)
                    oldB = budget.copyBudget(budgets)
                    compile(gmap, ghids, budgets, [alt] + cdr, results)
                    gmap = old
                    budgets = oldB    
                    # print("ALTER:", alter) 
            
            elif _type == CLUE_OVERLOOK_PLACED:
                """
                palced: whole row or column (5 lengths)
                """
                # todo: bug, expect: sat, given: unsat
                print("hit_CLUE_OVERLOOK_PLACED ", car, game_map.string(gmap))
                
                if clue.kernel_has_hermit(k):
                    old = game_map.copy_gmap(gmap)
                    oldB = budget.copyBudget(budgets)
                    opt_hermit(gmap, ghids, budgets, car, cdr, results)
                    gmap = old
                    budgets = oldB
                    
                else:
                    place_common_clue(gmap, ghids, budgets, car, cdr, results)
                    
            else:
                print("UNRECOGNIZED CLUE")
                assert False
            
            
            
        
            
        
    results = []            
    compile(gmap, hids, budgets, clues_rest, results)
    return results

# todo: bug
def compile_rest(gmap, hids, budgets):
    r = []
    def compile(gmap, ghids, budgets, results):
        print(game_map.string(gmap), budgets)
        if budget.empty(budgets):
            # base case 
            t = (game_map.copy_gmap(gmap), dict(ghids), [_ for _ in budgets])
            print("leaf:\n",  game_map.string(gmap), budgets)
            # breakpoint()
            results.append(t)
            return
        
        for x, row in enumerate(gmap):
            for y, block in enumerate(row):
                if block == EMPTY:
                    for terrain, num in enumerate(budgets):
                        if terrain != EMPTY and num > 0:
                            old = game_map.copy_gmap(gmap)
                            oldB = budget.copyBudget(budgets)                       
                            succ = game_map.check_and_set_block(gmap, budgets, x, y, terrain)
                            if succ:
                                compile(gmap, ghids, budgets, results)
                            gmap = old 
                            budgets = oldB
        
    compile(gmap, hids, budgets, r)
    return r


def island_size_min(gmap, terrain):
    def inner(gmap, x, y, terrain):
        if game_map.validate_index(x,y) and game_map.get_block(gmap, x,y) == terrain:    
            game_map.set_block(gmap, x, y, EMPTY)
            return 1 + \
                inner(gmap, x+1,y, terrain)+\
                inner(gmap, x-1,y, terrain)+\
                inner(gmap, x,y+1, terrain)+\
                inner(gmap, x,y-1, terrain)
                    
        else:
            return 0
    



    gmap_cp = game_map.copy_gmap(gmap)            
    
    min_size = 114514
    for x, row  in enumerate(gmap_cp):
            for y, block in enumerate(row):
                if block == terrain:
                    size = inner(gmap_cp, x, y, terrain)
                    min_size = min(size, min_size)
            
    return min_size if min_size < 114514 else 0

def island_num(gmap, terrain):
    def inner(gmap, x, y, terrain):
        if game_map.validate_index(x,y) and game_map.get_block(x,y) == terrain:    
            game_map.set_block(gmap, x, y, EMPTY)
            
            inner(gmap, x+1,y, terrain)
            inner(gmap, x-1,y, terrain)
            inner(gmap, x,y+1, terrain)
            inner(gmap, x,y-1, terrain)
    

    gmap_cp = game_map.copy_gmap(gmap)            
    
    cnt = 0
    for x, row  in enumerate(gmap_cp):
            for y, block in enumerate(row):
                if block == terrain:
                    cnt += 1
                    inner(gmap_cp, x, y, terrain)
           
            
    return cnt

def exist_neighbor(gmap, terrain, neighbor):

    for x, row  in enumerate(gmap):
            for y, block in enumerate(row):
                if block == terrain:
                    
                    for dire in {(-1,0),(1,0),(0,-1),(0,1)}:
                        delta_x = dire[0]
                        delta_y = dire[1]
                        if game_map.get_block(gmap, x+delta_x,y+delta_y) == neighbor:
                            return True
    return False

def cross_island_num(gmap, terrain):
    def inner(gmap, x, y, terrain):
        if game_map.validate_index(x,y) and game_map.get_block(x,y) == terrain:    
            game_map.set_block(gmap, x, y, EMPTY)
            
            inner(gmap, x+1, y+1, terrain)
            inner(gmap, x-1, y-1, terrain)
            inner(gmap, x-1, y+1, terrain)
            inner(gmap, x+1, y-1, terrain)
    

    gmap_cp = game_map.copy_gmap(gmap)            
    
    cnt = 0
    for x, row  in enumerate(gmap_cp):
            for y, block in enumerate(row):
                if block == terrain:
                    cnt += 1
                    inner(gmap_cp, x, y, terrain)
           
            
    return cnt
                            

def check_road(gmap):
    return island_num(gmap, ROAD) == 1 and exist_neighbor(gmap, ROAD, OUTER)

def check_river(gmap):
    return island_size_min(gmap, RIVER) == 2 and island_num(gmap, RIVER) == 2

def check_forest(gmap):
    return not exist_neighbor(gmap, FOREST, FOREST)

def check_village(gmap):
    return cross_island_num(gmap, VILLIAGE) == 1
"""
General Idea: BackTrack Testing

budgets: List[int],  number of each terrian
hermit_clue: 
normal_clue: 
"""
def solve(budgets, clues):
    budget.validateBudgets(budgets)
    cluesp = breakdown_kernels(clues)
    print("AFTER PRE PROCESS:", cluesp)
    # assert False
    clues_hermits = clue.filter_hermits(cluesp)
    clues_rest= list(filter(lambda x: clue.get_clue_type(x)!=CLUE_HERMIT, cluesp))
    
    results = compile_hermits(clues_hermits, budgets)
    # show_results(results)
    
    print("Hermits Done.")
    
    rrr = []
    for result in results:
        gmap = result[0]
        hids = result[1]
        budgets = result[2]
        
        rr = compile_others(gmap, hids, budgets, clues_rest)
        rrr.extend(rr)
    
    print("CLUES Done.")
    show_results(rrr)
    # post_process(rrr)
    
    r_full = []
    for r_final in rrr:
        gmap = r_final[0]
        hids = r_final[1]
        budgets = r_final[2]
        
        r_rest = compile_rest(gmap, hids, budgets)
        r_full.extend(r_rest)
    
    show_results(r_full)
    print("FILLs Done.")
    
    rk = []
    for r in r_full:
        gmap = r_final[0]
        hids = r_final[1]
        budgets = r_final[2]
        if check_river(gmap):
            # check_road(gmap) and \
            # check_forest(gmap) and\
            # check_village(gmap):
            
            rk.append(r)
    
    show_results(rk)
        
                    
            
    
    

def show_gamemap(gmap: list[list[int]]):
    print(f"GameMap: \n{game_map.string(gmap)}")

"""
Display Result 

results: list
"""
def show_results(results:list[tuple]):
    if results == []:
        print("UNSAT.")
    
    for cnt, res in enumerate(results):
        print(f"Result ({cnt})")
        gmap = res[0]
        show_gamemap(gmap)
        h_layout = res[1]
        print(f"Hermits Layout(0 For Empty Space):\n{game_map.string_hermit_layout(h_layout)}")
        print(f"Budgets Rest: \n{res[2]}")
        print()
    
        


def test1():
    my_game_map = game_map.init_game_map()
    print(game_map.string(my_game_map))
    budgets = budget.initBudget()
    print("budget: ", budgets)
    
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
    budgets = budget.initBudget()
    print("budget: ", budgets)
    
    k1 = clue.create_kernel((HERMITS, (0,0)),
                            (ROAD, (1,0)))
    
    k2 = clue.create_kernel((FOREST, (0,0)),
                            (HERMITS, (0,1)))
    
    k3 = clue.create_kernel((HERMITS, (0,0)),
                            (RIVER,(1,0)))
    
    k4 = clue.create_kernel((HERMITS, (0,0)),
                            (VILLIAGE, (1,0)))
    
    k5 = clue.create_kernel((FOREST, (0,0)),
                            (HERMITS, (1,0)))
    
    
    hclue =  clue.create_clue(CLUE_HERMIT, 
                              kernel= [k1,k2],
                              hIds= [1, 4],
                              direction= NO_DIRECTION)
    
    hclue1 =  clue.create_clue(CLUE_HERMIT, 
                              kernel= [k3,k4],
                              hIds= [2, 3],
                              direction= NO_DIRECTION)
    
    hclue2 =  clue.create_clue(CLUE_HERMIT, 
                              kernel= [k5],
                              hIds= [2],
                              direction= NO_DIRECTION)
    
    
    """
    隐者2号在东北
    """
    hclue3 =  clue.create_clue(CLUE_HERMIT, 
                              kernel= [],
                              hIds= [2],
                              direction= NORTH_EAST)
    
    k_bird = clue.create_kernel((HERMITS, (0,0)),
                                 (RIVER,(0,1)),
                                 (PLAINS,(1,0)),
                                 (FOREST,(1,1)))

    cclue = clue.create_clue(CLUE_BIRD, 
                             kernel= [k_bird])
    
    
    #   4
    # 1 2 6
    #   3
    k_dryad = clue.create_kernel((HERMITS, (1,0)),
                                 (RIVER,(0,1)),
                                 (PLAINS,(1,2)),
                                 (FOREST,(1,1)),
                                 (ROAD, (2,1)))

    dclue = clue.create_clue(CLUE_DRYAD, 
                             kernel= [k_dryad])
    
    #    4
    # -1 2 6
    #    3
    k_dryad1 = clue.create_kernel((OUTER, (1,0)),
                                 (RIVER,(0,1)),
                                 (PLAINS,(1,2)),
                                 (FOREST,(1,1)),
                                 (ROAD, (2,1)))

    dclue1 = clue.create_clue(CLUE_DRYAD, 
                             kernel= [k_dryad1])
    
    
    

    
    solve(budgets, [hclue, hclue1, hclue2, hclue3, cclue, dclue, dclue1])

def test3():
    my_game_map = game_map.init_game_map()
    print(game_map.string(my_game_map))
    budgets = budget.initBudget()
    print("budget: ", budgets)
    
    k1 = clue.create_kernel((HERMITS, (0,0)),
                            (ROAD, (1,0)))
    
    k2 = clue.create_kernel((FOREST, (0,0)),
                            (HERMITS, (0,1)))
    
    k3 = clue.create_kernel((HERMITS, (0,0)),
                            (RIVER,(1,0)))
    
    k4 = clue.create_kernel((HERMITS, (0,0)),
                            (VILLIAGE, (1,0)))
    
    k5 = clue.create_kernel((FOREST, (0,0)),
                            (HERMITS, (1,0)))
    
    
    hclue =  clue.create_clue(CLUE_HERMIT, 
                              kernel= [k1,k2],
                              hIds= [1, 4],
                              direction= NO_DIRECTION)
    
    hclue1 =  clue.create_clue(CLUE_HERMIT, 
                              kernel= [k3,k4],
                              hIds= [2, 3],
                              direction= NO_DIRECTION)
    
    hclue2 =  clue.create_clue(CLUE_HERMIT, 
                              kernel= [k5],
                              hIds= [2],
                              direction= NO_DIRECTION)
    
    
    """
    隐者2号在东北
    """
    hclue3 =  clue.create_clue(CLUE_HERMIT, 
                              kernel= [],
                              hIds= [2],
                              direction= NORTH_EAST)
    
    k_bird = clue.create_kernel((HERMITS, (0,0)),
                                 (RIVER,(0,1)),
                                 (PLAINS,(1,0)),
                                 (FOREST,(1,1)))

    cclue = clue.create_clue(CLUE_BIRD, 
                             kernel= [k_bird])
    
    
    #   4
    # 1 2 6
    #   3
    k_dryad = clue.create_kernel((HERMITS, (1,0)),
                                 (RIVER,(0,1)),
                                 (PLAINS,(1,2)),
                                 (FOREST,(1,1)),
                                 (ROAD, (2,1)))

    dclue = clue.create_clue(CLUE_DRYAD, 
                             kernel= [k_dryad])
    
    #    4
    # -1 2 6
    #    3
    k_dryad = clue.create_kernel((OUTER, (1,0)),
                                 (RIVER,(0,1)),
                                 (PLAINS,(1,2)),
                                 (FOREST,(1,1)),
                                 (ROAD, (2,1)))

    dclue1 = clue.create_clue(CLUE_DRYAD, 
                             kernel= [k_dryad])
    
    
    
    # 4
    # 6
    # 6
    # 6
    # 2
    k_overlook = clue.create_kernel((RIVER, (0,0)),
                                 (PLAINS,(1,0)),
                                 (PLAINS,(2,0)),
                                 (PLAINS, (3,0)),
                                 (FOREST,(4,0)),
                                 )
    
    oclue = clue.create_clue(CLUE_OVERLOOK, 
                             kernel= [k_overlook], 
                             direction=SOUTH)
    
    
    
    #solve(budgets, [hclue, hclue1, hclue2, hclue3, dclue, oclue])
    solve(budgets, [hclue, hclue1, dclue, oclue])
    #solve(budgets, [])


if __name__ == '__main__':
    #test1()
    test2()
    test3()
    
    

