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
OUT = os.path.join('figures','surf')
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

# GAUSS_ARGS = [  (1,     [-0.2, 0.2],    [0.3, 0.3]),
#                 (0.5,   [-1.3, -0.1],   [0.15, 0.15]),
#                 (0.7,   [-0.8, -0.4],   [0.2, 0.2]),
#                 (0.6,   [-0.8, -0],     [0.4, 0.4]),
#                 (0.4,   [0.6, 0.0],     [0.4, 0.2]),
#                 (0.8,   [1.25, 0.3],    [0.25, 0.25])]


EPSILON = 0.20

if __name__ == '__main__':
    grid = make_grid(RES, SHAPE)
    surface = mk_gauss(grid[0], grid[1], GAUSS_ARGS)

    if SAVE:
        if not os.path.exists('data'):
            os.makedirs('data')
        np.savetxt(os.path.join(DIR, '%s%d.%s' % (NAME,RES,EXT)), surface)

    CFG = CONFIG['surf']
    # CFG['cuts'] = [0.0, 0.3, 0.55, 0.8, 1.35]
    # CFG['cuts'] = [0.0, 0.3 - EPSILON, 0.55 - EPSILON, 0.8 - EPSILON, 1.35 - EPSILON]
    # CFG['cuts'] = [0.0, 0.3 + EPSILON, 0.55 + EPSILON, 0.8 + EPSILON, 1.35 + EPSILON]
    COLORS = [COLOR[k] for k in CFG['colors']]
    fig, ax = init_surface(CFG['shape'], CFG['pad'])

    surf = ScalarField(surface, grid)
    COLORS = [COLOR[k] for k in CFG['colors']]
    # surf_plt = plot_surface(ax, surf, [0.0,  0.05], [[1,1,1,1], [0,0,0,0]])
    # surf_plt = plot_surface(ax, surf, [0.0, 0.8], [COLOR['purple']+(0.5,), COLOR['yellow']+(0,)])
    surf_plt = plot_surface(ax, surf, CFG['cuts'], COLORS)

    name = os.path.join(OUT, f'{NAME}{RES}')
    fname = f'{name}.png'
    print(f'saving {fname}')
    plt.savefig(fname, dpi=300, transparent=True)
    #
    #
    surf_alpha = [0.5, 0.5, 0.5, 0.5]
    cont_alpha = [0, 0, 0, 0, 0]
    surf_plt['surface'].set_alpha(surf_alpha)
    surf_plt['contours'].set_alpha(cont_alpha)
    plt.savefig(f'{name}.png', dpi=300, transparent=True)
    # # cont_alpha[0] = 1
    # for i in range(len(CFG['cuts'])-1):
    #     surf_alpha[i], cont_alpha[i+1] = 0.5, 1.
    #     surf_plt['surface'].set_alpha(surf_alpha)
    #     surf_plt['contours'].set_alpha(cont_alpha)
    #     fname = f'{name}-{i}.png'
    #     print(f'saving {fname}')
    #     plt.savefig(fname, dpi=300, transparent=True)
    #     cont_alpha[i+1] = 0

    # _grid = make_grid(CFG['res'], CFG['shape'])
    # _surf = ScalarFieldData('data/surf32.csv', _grid, CFG['lips'])
    # _surf_plt = plot_surface(ax, _surf, CFG['cuts'], COLORS, alpha=0., contour_color='black')
