from functools import reduce


def identity(x):
    return x

def diff(p):
    return p[1] - p[0]

def stuple(l, *args, **kw):
    return tuple(sorted(l, *args, **kw))

def grid_coord(coords, n):
    return [coords//n, coords%n]
