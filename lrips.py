from itertools import combinations
from scipy.spatial import KDTree
import numpy.linalg as la
import numpy as np
import argparse
import os, sys

from lips.topology import RipsComplex
from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.config import CONFIG
from contours.style import COLOR
from contours.plot import *


parser = argparse.ArgumentParser(prog='sample')

parser.add_argument('--dir', default=os.path.join('figures','lips-sub'), help='dir')
parser.add_argument('--file', default='data/surf-sample_1067_1.2e-1.csv', help='sample file')
parser.add_argument('--sub', default='data/surf-sample_329_2e-1.csv', help='subsample file')
parser.add_argument('--dpi', type=int, default=300, help='dpi')
parser.add_argument('--save', action='store_true', help='save')
parser.add_argument('--mult', type=float, default=1.2, help='thresh mult')
parser.add_argument('--wait', type=float, default=0.5, help='wait')
parser.add_argument('--tag', default=None, help='tag directory and file')

plt.ion()

if __name__ == '__main__':
    args = parser.parse_args()

    args.tag = "" if args.tag is None else f"_{args.tag}"
    args.dir = f"{args.dir}{args.tag}"

    kwargs = {'dir' : args.dir, 'save' : args.save, 'wait' : args.wait, 'dpi' : args.dpi}
    keys = {'max' : {'visible' : False, 'color' : COLOR['blue'], 'edge_color' : COLOR['blue'], 'zorder' : 2},
            'min' : {'visible' : False, 'color' : COLOR['red'], 'edge_color' : COLOR['red'], 'zorder' : 1}}
    CFG = CONFIG['rainier' if 'rainier' in  args.file else 'surf']

    fig, ax = plt.subplots(figsize=(10*CFG['shape'][0],10*CFG['shape'][1]))
    xl, yl = CFG['shape'][0]*CFG['pad'][0], CFG['shape'][1]*CFG['pad'][1]
    COLORS = [COLOR[k] for k in CFG['colors']]
    init_surface(ax, (-xl,xl), (-yl,yl))

    sample, subsample = SampleData(args.file), SampleData(args.sub)
    rips = RipsComplex(sample.points, sample.radius*args.mult)
    rips.lips_sub(subsample, CFG['lips'])

    levels = subsample.get_levels(CFG['cuts'])
    name = f'{sample.name}_subsample_lips{args.tag}'

    sample_plt = plot_points(ax, sample, zorder=4, edgecolors='black', facecolors='none', s=5)
    subsample_plt = plot_points(ax, subsample, c='black', s=10, zorder=5)
    rips_plt = plot_rips_filtration(ax, rips, levels, keys, name, **kwargs)
