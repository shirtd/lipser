import numpy as np
import os

from contours.data import make_grid
from lipser.util.math import mk_gauss


SAVE = True
DIR = 'data'
NAME = 'surf'
EXT = 'csv'

RES = 32
SHAPE = (2,1)
GAUSS_ARGS = [  (1,     [-0.2, 0.2],    [0.3, 0.3]),
                (0.5,   [-1.3, -0.1],   [0.15, 0.15]),
                (0.7,   [-0.8, -0.4],   [0.2, 0.2]),
                (0.8,   [-0.8, -0],     [0.4, 0.4]),
                (0.4,   [0.6, 0.0],     [0.4, 0.2]),
                (0.7,   [1.25, 0.3],    [0.25, 0.25])]


if __name__ == '__main__':
    grid = make_grid(RES, SHAPE)
    surface = mk_gauss(grid[0], grid[1], GAUSS_ARGS)

    if SAVE:
        if not os.path.exists('data'):
            os.makedirs('data')
        np.savetxt(os.path.join(DIR, '%s%d.%s' % (NAME,RES,EXT)), surface)
