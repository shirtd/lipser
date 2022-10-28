import matplotlib.pyplot as plt
import numpy as np
import os

from contours.surface import make_grid
from lips.util.math import mk_gauss
from contours.surface import *
from contours.plot import *

from contours.style import COLOR
from contours.config import CONFIG

plt.ion()

SAVE = True
DIR = 'data'
NAME = 'surf-close'
EXT = 'csv'

RES = 32
SHAPE = (2,1)
# GAUSS_ARGS = [  (1,     [-0.2, 0.2],    [0.3, 0.3]),
#                 (0.5,   [-1.3, -0.1],   [0.15, 0.15]),
#                 (0.7,   [-0.8, -0.4],   [0.2, 0.2]),
#                 (0.8,   [-0.8, -0],     [0.4, 0.4]),
#                 (0.4,   [0.6, 0.0],     [0.4, 0.2]),
#                 (0.7,   [1.25, 0.3],    [0.25, 0.25])]

GAUSS_ARGS = [  (1,     [-0.2, 0.2],    [0.3, 0.3]),
                (0.5,   [-1.3, -0.1],   [0.15, 0.15]),
                (0.7,   [-0.8, -0.4],   [0.2, 0.2]),
                (0.6,   [-0.8, -0],     [0.4, 0.4]),
                (0.4,   [0.6, 0.0],     [0.4, 0.2]),
                (0.8,   [1.25, 0.3],    [0.25, 0.25])]


if __name__ == '__main__':
    grid = make_grid(RES, SHAPE)
    surface = mk_gauss(grid[0], grid[1], GAUSS_ARGS)

    if SAVE:
        if not os.path.exists('data'):
            os.makedirs('data')
        np.savetxt(os.path.join(DIR, '%s%d.%s' % (NAME,RES,EXT)), surface)

    CFG = CONFIG['surf']
    fig, ax = plt.subplots(figsize=(10*CFG['shape'][0],10*CFG['shape'][1]))
    xl, yl = CFG['shape'][0]*CFG['pad'][0], CFG['shape'][1]*CFG['pad'][1]
    COLORS = [COLOR[k] for k in CFG['colors']]
    init_surface(ax, (-xl,xl), (-yl,yl))

    surf = ScalarField(surface, grid)
    COLORS = [COLOR[k] for k in CFG['colors']]
    surf_plt = plot_surface(ax, surf, CFG['cuts'], COLORS)

    _grid = make_grid(CFG['res'], CFG['shape'])
    _surf = ScalarFieldData('data/surf32.csv', _grid, CFG['lips'])
    _surf_plt = plot_surface(ax, _surf, CFG['cuts'], COLORS, alpha=0., contour_color='black')
