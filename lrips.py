import matplotlib.pyplot as plt
import numpy.linalg as la
import numpy as np

from itertools import combinations
from lips.topology import RipsComplex
from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.plot import plot_surface, plot_points, plot_rips, get_color, init_surface
from contours.style import COLOR
import os, sys
from scipy.spatial import KDTree

import dionysus as dio

import argparse


RES = 32
SHAPE = (2,1)
CUTS = [0.05, 0.2, 0.45, 0.875, 1.09, 1.31]
COLOR_ORDER = ['blue','green','yellow','salmon','purple']
COLORS = [COLOR[k] for k in COLOR_ORDER]

# RES = 337
# SHAPE = (1,1)
#
# MIN = 265.258441
# MAX = 4379.845434
#
# # CUTS = MAX * np.array([0.0, 0.15, 0.28, 0.38, 0.48, 1.0]) + MIN
# CUTS = [200, 1000, 1400, 1800, 2200, np.inf]
# COLOR_ORDER = ['blue','green','yellow','salmon','purple']
# COLORS = [COLOR[k] for k in COLOR_ORDER]

parser = argparse.ArgumentParser(prog='sample')

parser.add_argument('--dir', default=os.path.join('figures','lips_sub'), help='dir')
parser.add_argument('--surf', default='data/surf32.csv', help='surface file')
parser.add_argument('--file', default='data/surf-sample_1067_1.2e-1.csv', help='sample file')
parser.add_argument('--sub', default='data/surf-sample_329_2e-1.csv', help='subsample file')
parser.add_argument('--dpi', type=int, default=300, help='dpi')
parser.add_argument('--save', action='store_true', help='save')
parser.add_argument('--mult', type=float, default=1.1, help='thresh mult')
parser.add_argument('--wait', type=float, default=0.5, help='wait')
parser.add_argument('--lips', type=float, default=3.1443048369350226, help='lipschitz constant')
# parser.add_argument('--lips', type=float, default=25483.938340730343, help='lipschitz constant')
parser.add_argument('--cmult', type=float, default=1., help='c mult')

plt.ion()
fig, ax = plt.subplots(figsize=(10,8))
init_surface(ax, (-3,3), (-2,2))

if __name__ == '__main__':
    args = parser.parse_args()

    surf = ScalarFieldData(args.surf, make_grid(RES, SHAPE), args.cmult*args.lips)
    surf_plt = plot_surface(ax, surf, CUTS, COLORS, zorder=0)

    sample, subsample = SampleData(args.file), SampleData(args.sub)
    # subsample_colors = [get_color(f, CUTS, COLORS) for f in subsample.function]

    sample_plt = plot_points(ax, sample, zorder=4, edgecolors='black', facecolors='none', s=5)
    subsample_plt = plot_points(ax, subsample, c='black', s=10, zorder=5)

    rips = RipsComplex(sample.points, sample.radius*args.mult)

    for p, s in zip(sample, rips(0)):
        s.data['max'] = min(f + surf.constant*la.norm(p - s) for s,f in zip(subsample, subsample.function))
        s.data['min'] = max(f - surf.constant*la.norm(p - s) for s,f in zip(subsample, subsample.function))

    max_rips_plt = plot_rips(ax, rips, COLOR['blue'], COLOR['blue'], False, zorder=2)
    min_rips_plt = plot_rips(ax, rips, COLOR['red'], COLOR['red'], False, zorder=1)

    for s in rips(1)+rips(2):
        s.data['max'] = max(rips(0)[v].data['max'] for v in s)
        s.data['min'] = max(rips(0)[v].data['min'] for v in s)

    if args.save and not os.path.exists(args.dir):
        os.makedirs(args.dir)

    fmin, fmax = subsample.function.min(), subsample.function.max()
    levels = [fmin-fmax/2] + CUTS + [1.3*fmax]
    for i, t in enumerate(levels):
        for d in (1,2):
            for s in rips(d):
                if s.data['max'] <= t:
                    max_rips_plt[d][s].set_visible(True)
                if s.data['min'] <= t:
                    min_rips_plt[d][s].set_visible(True)
        plt.pause(args.wait)
        if args.save:
            cmult_s = ('cx' + np.format_float_scientific(args.cmult, trim='-')) if int(args.cmult) != args.mult else ''
            plt.savefig(os.path.join(args.dir, '%s_subsample_lips%d%s.png' % (subsample.name, i, cmult_s)), dpi=args.dpi, transparent=True)

    # plt.savefig(os.path.join(args.dir, '%s_subsample_lips_sample.png' % (subsample.name)), dpi=args.dpi, transparent=True)
    # plt.savefig(os.path.join(args.dir, '%s_subsample_lips_subsample.png' % (subsample.name)), dpi=args.dpi, transparent=True)
    # plt.savefig(os.path.join(args.dir, '%s_subsample_lips_both.png' % (subsample.name)), dpi=args.dpi, transparent=True)
