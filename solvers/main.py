import sys
import cv 
import solver, budget

def runWithCV(path='./imgs'):
    tasks = cv.process_directory(path, cv.getClueTask)
    _clues = []
    for t in tasks:
        path, clueType, dire = t
        clue = cv.parseClue(clueType, dire, path)
        _clues.append(clue)
    
    solve(_clues)
    # for r in _clues:
    #     print("RESULT:", r)

def solve(_clues):
    budgets = budget.initBudget()
    solver.solve(budgets, _clues)
    

# with open("clues.txt", "r") as f:
#     s = f.read()
#     l = eval(s)
#     print(l,"\n\n",s)
#     solve(l)
    
argc = len(sys.argv)
print(argc)
if argc <= 2:
    runWithCV()    
elif argc > 2:
    path = sys.argv[1]
    runWithCV(path=path)

    