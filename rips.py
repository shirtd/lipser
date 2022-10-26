import numpy as np
import argparse
import os,sys

from contours.surface import make_grid, ScalarFieldData, SampleData
from lips.topology import RipsComplex
from contours.config import CONFIG
from contours.style import COLOR
from contours.plot import *





parser = argparse.ArgumentParser(prog='sample')

parser.add_argument('--dir', default=os.path.join('figures','sfa'), help='dir')
parser.add_argument('--file', default='data/surf-sample_329_2e-1.csv', help='sample file')

parser.add_argument('--dpi', type=int, default=300, help='dpi')
parser.add_argument('--save', action='store_true', help='save')
parser.add_argument('--mult', type=float, default=1.15, help='thresh mult')
parser.add_argument('--wait', type=float, default=0.5, help='wait')
parser.add_argument('--tag', default=None, help='tag directory and file')

plt.ion()
fig, ax = plt.subplots(figsize=(10,8))

if __name__ == '__main__':
    args = parser.parse_args()

    args.tag = "" if args.tag is None else f"_{args.tag}"
    args.dir = f"{args.dir}{args.tag}"

    kwargs = {'dir' : args.dir, 'save' : args.save, 'wait' : args.wait, 'dpi' : args.dpi}
    keys = {'f' : {'visible' : False, 'color' : COLOR['red'], 'edge_color' : COLOR['red'], 'zorder' : 2}}
    CFG = CONFIG['rainier' if 'rainier' in  args.file else 'surf']

    fig, ax = plt.subplots(figsize=(10*CFG['shape'][0],10*CFG['shape'][1]))
    xl, yl = CFG['shape'][0]*CFG['pad'][0], CFG['shape'][1]*CFG['pad'][1]
    COLORS = [COLOR[k] for k in CFG['colors']]
    init_surface(ax, (-xl,xl), (-yl,yl))

    sample = SampleData(args.file)
    rips = RipsComplex(sample.points, sample.radius*args.mult)
    rips.sublevels(sample)

    levels = sample.get_levels(CFG['cuts'])
    name = f'{sample.name}_lips_tri{args.tag}'

    sample_plt = plot_points(ax, sample, zorder=4, c='black', s=9)
    rips_plt = plot_rips_filtration(ax, rips, levels, keys, name, **kwargs)
