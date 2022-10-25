import matplotlib.pyplot as plt
import numpy.linalg as la
import numpy as np

from itertools import combinations
from lips.topology import RipsComplex
from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.plot import plot_surface, plot_points, plot_rips, get_color, init_surface, plot_balls
from contours.style import COLOR
from contours.config import CONFIG
import os, sys
from scipy.spatial import KDTree

import dionysus as dio

import argparse

parser = argparse.ArgumentParser(prog='sample')

parser.add_argument('--dir', default=os.path.join('figures','lips'), help='dir')
parser.add_argument('--surf', default='data/surf32.csv', help='surface file')
parser.add_argument('--file', default='data/surf-sample_1067_1.2e-1.csv', help='sample file')
parser.add_argument('--dpi', type=int, default=300, help='dpi')
parser.add_argument('--save', action='store_true', help='save')
parser.add_argument('--mult', type=float, default=1.1, help='thresh mult')
parser.add_argument('--wait', type=float, default=0.5, help='wait')
parser.add_argument('--rips', action='store_true', help='plot rips not balls')
parser.add_argument('--tag', default=None, help='tag directory and file')


plt.ion()
fig, ax = plt.subplots(figsize=(10,8))

if __name__ == '__main__':
    args = parser.parse_args()

    args.tag = "" if args.tag is None else f"_{args.tag}"
    args.dir = f"{args.dir}{args.tag}"

    CFG = CONFIG['rainier' if 'rainier' in  args.surf else 'surf']
    RES, SHAPE, LIPS = CFG['res'], CFG['shape'], CFG['lips']
    CUTS, COLOR_ORDER, LABELS = CFG['cuts'], CFG['colors'], CFG['labels']
    xl, yl = CFG['shape'][0]*1.25, CFG['shape'][1]*1.25
    COLORS = [COLOR[k] for k in COLOR_ORDER]
    init_surface(ax, (-xl,xl), (-yl,yl))

    surf = ScalarFieldData(args.surf, make_grid(RES, SHAPE), LIPS)
    # surf_plt = plot_surface(ax, surf, CUTS, COLORS, zorder=0)

    sample = SampleData(args.file)
    # subsample_colors = [get_color(f, CUTS, COLORS) for f in subsample.function]

    sample_plt = plot_points(ax, sample, zorder=4, c='black', s=9)

    if args.save and not os.path.exists(args.dir):
        os.makedirs(args.dir)

    fmin, fmax = sample.function.min(), sample.function.max()
    levels = [fmin-fmax/2] + CUTS + [1.3*fmax]
    levels = [(a+b)/2 for a,b in zip(levels[:-1],levels[1:])]

    if args.rips:
        rips = RipsComplex(sample.points, sample.radius*args.mult)
        max_plot = plot_rips(ax, rips, COLOR['blue'], COLOR['blue'], False, zorder=2)
        min_plot = plot_rips(ax, rips, COLOR['red'], COLOR['red'], True, zorder=1)

        for s in rips(1):
            sf = sample(s[0]) + sample(s[1])
            sd = surf.constant * s.data['dist']
            s.data['max'] = (sf + sd) / 2
            s.data['min'] = (sf - sd) / 2
        for s in rips(2):
            s.data['max'] = max(rips[e].data['max'] for e in combinations(s,2))
            s.data['min'] = min(rips[e].data['min'] for e in combinations(s,2))

        for i, t in enumerate(levels):
            for d in (1,2):
                for s in rips(d):
                    if s.data['max'] <= t:
                        max_plot[d][s].set_visible(True)
                    if s.data['min'] <= t:
                        min_plot[d][s].set_visible(False)
            plt.pause(args.wait)
            if args.save:
                fname = f'{sample.name}_lips_rips{args.tag}{i}.png'
                fpath = os.path.join(args.dir, fname)
                print(f'saving {fpath}')
                plt.savefig(fpath, dpi=args.dpi, transparent=True)
    else:
        balls_max = plot_balls(ax, sample, 2 * sample.function/surf.constant, color=COLOR['blue'], zorder=3, alpha=0.15)
        balls_min = plot_balls(ax, sample, 2 * sample.function/surf.constant, color=COLOR['red'], zorder=3, alpha=0.15)

        for i, t in enumerate(levels):
            for f, mn, mx in zip(sample.function, balls_min, balls_max):
                fmax = (t - f) / surf.constant
                fmin = (f - t) / surf.constant
                mn.set_radius(fmin if fmin > 0 else 0)
                mx.set_radius(fmax if fmax > 0 else 0)
            plt.pause(args.wait)
            if args.save:
                tag = "" if args.tag is None else f"_{args.tag}"
                fname = f'{sample.name}_lips_balls{args.tag}{i}.png'
                fpath = os.path.join(args.dir, fname)
                print(f'saving {fpath}')
                plt.savefig(fpath, dpi=args.dpi, transparent=True)
