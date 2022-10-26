from scipy.spatial import KDTree
import numpy.linalg as la
import dionysus as dio
import numpy as np
import argparse
import os, sys

from itertools import combinations
from lips.topology import RipsComplex
from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.config import CONFIG
from contours.style import COLOR
from contours.plot import *


parser = argparse.ArgumentParser(prog='sample')

parser.add_argument('--dir', default=os.path.join('figures','lips'), help='dir')
parser.add_argument('--file', default='data/surf-sample_1067_1.2e-1.csv', help='sample file')
parser.add_argument('--dpi', type=int, default=300, help='dpi')
parser.add_argument('--save', action='store_true', help='save')
parser.add_argument('--mult', type=float, default=1.1, help='thresh mult')
parser.add_argument('--wait', type=float, default=0.5, help='wait')
parser.add_argument('--rips', action='store_true', help='plot rips not balls')
parser.add_argument('--tag', default=None, help='tag directory and file')

plt.ion()

if __name__ == '__main__':
    args = parser.parse_args()

    args.tag = "" if args.tag is None else f"_{args.tag}"
    args.dir = f"{args.dir}{args.tag}"

    kwargs = {'dir' : args.dir, 'save' : args.save, 'wait' : args.wait, 'dpi' : args.dpi}
    keys = {'max' : {'visible' : False, 'color' : COLOR['blue'], 'zorder' : 2},
            'min' : {'visible' : True, 'color' : COLOR['red'], 'zorder' : 1}}
    CFG = CONFIG['rainier' if 'rainier' in  args.file else 'surf']
    
    fig, ax = plt.subplots(figsize=(10*CFG['shape'][0],10*CFG['shape'][1]))
    xl, yl = CFG['shape'][0]*CFG['pad'][0], CFG['shape'][1]*CFG['pad'][1]
    COLORS = [COLOR[k] for k in CFG['colors']]
    init_surface(ax, (-xl,xl), (-yl,yl))

    sample = SampleData(args.file)
    sample_plt = plot_points(ax, sample, zorder=4, c='black', s=9)

    name = f'{sample.name}_subsample_lips{args.tag}'
    levels = sample.get_levels(CFG['cuts'])

    if args.rips:
        name = f'{sample.name}_lips_rips{args.tag}'
        keys['max']['edge_color'] = keys['max']['color']
        keys['min']['edge_color'] = keys['min']['color']

        rips = RipsComplex(sample.points, sample.radius*args.mult)
        rips.lips(sample, CFG['lips'])

        rips_plt = plot_rips_filtration(ax, rips, levels, keys, name, **kwargs)
    else:
        name = f'{sample.name}_lips_balls{args.tag}'
        keys['max']['visible'] = True
        offset_plt = plot_offset_filtration(ax, sample, CFG['lips'], levels, keys, name, **kwargs)
