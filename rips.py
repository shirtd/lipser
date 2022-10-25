import matplotlib.pyplot as plt
import numpy as np

from lips.topology import RipsComplex
from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.plot import plot_surface, plot_points, plot_rips, init_surface
from contours.style import COLOR
import os,sys

LABELS = ['A', 'B', 'C', 'D', 'E']
CUTS = [0.05, 0.2, 0.45, 0.875, 1.09, 1.31]
COLOR_ORDER = ['blue','green','yellow','salmon','purple']
#
# LABELS = ['A', 'B', 'C', 'D']
# CUTS = [0.05, 0.3, 0.55, 0.8, 1.3]
# COLOR_ORDER = ['green', 'blue', 'purple', 'yellow']

RES = 32
SHAPE = (2,1)
COLORS = [COLOR[k] for k in COLOR_ORDER]
CUT_ARGS = {l : {'min' : a, 'max' : b, 'color' : c} for l,(a,b),c in zip(LABELS,zip(CUTS[:-1], CUTS[1:]),COLORS)}

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

import argparse

parser = argparse.ArgumentParser(prog='sample')

parser.add_argument('--dir', default=os.path.join('figures','sfa'), help='dir')
parser.add_argument('--surf', default='data/surf32.csv', help='surface file')
parser.add_argument('--file', default='data/surf-sample_329_2e-1.csv', help='sample file')
parser.add_argument('--dpi', type=int, default=300, help='dpi')
parser.add_argument('--save', action='store_true', help='save')
parser.add_argument('--mult', type=float, default=1., help='thresh mult')
parser.add_argument('--wait', type=float, default=0.5, help='wait')
parser.add_argument('--lips', type=float, default=3.1443048369350226, help='lipschitz constant')
parser.add_argument('--cmult', type=float, default=1., help='c mult')

plt.ion()
fig, ax = plt.subplots(figsize=(10,8))
init_surface(ax, (-3,3), (-2,2))
# init_surface(ax, (-1,1), (-1,1))

if __name__ == '__main__':
    args = parser.parse_args()
    # surf = ScalarFieldData(SURF_PATH, make_grid(RES, SHAPE))
    sample = SampleData(args.file)
    rips = RipsComplex(sample.points, sample.radius*args.mult)
    for s in rips:
        s.data['f'] = sample(s).max()

    sample_plt = plot_points(ax, sample, zorder=4, c='black', s=9)
    rips_plt = plot_rips(ax, rips, COLOR['red'], COLOR['red'], False, zorder=2)

    if args.save and not os.path.exists(args.dir):
        os.makedirs(args.dir)

    fmin, fmax = sample.function.min(), sample.function.max()
    levels = [fmin-fmax/2] + CUTS + [1.3*fmax]
    for i, t in enumerate(levels):
        for d in (1,2):
            for s in rips(d):
                if s.data['f'] <= t:
                    rips_plt[d][s].set_visible(True)
        plt.pause(args.wait)
        if args.save:
            cmult_s = ('cx' + np.format_float_scientific(args.cmult, trim='-')) if int(args.cmult) != args.mult else ''
            plt.savefig(os.path.join(args.dir, '%s_lips_tri%d%s.png' % (sample.name, i, cmult_s)), dpi=args.dpi, transparent=True)
