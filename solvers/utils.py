import itertools

def pick_elements(collection, N):
    # Get all combinations of size N
    combinations = list(itertools.combinations(collection, N))
    return combinations

def flatMap(func, iterable):
    return list(itertools.chain.from_iterable(map(func, iterable)))

def flatten(iterable):
    return flatMap(lambda x: x, iterable)