import functools
import tqdm


def tqit(it, verbose=False, desc=None, n=None):
    return tqdm.tqdm(it, desc=desc, total=n) if verbose else it

def lmap(f, l):
    return list(map(f,l))

def insert(l, i, x):
    l[i] += [x]
    return l

def partition(f, l, n):
    return functools.reduce(f, l, [[] for _ in range(n)])
