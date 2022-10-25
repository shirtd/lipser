import matplotlib.pyplot as plt
import numpy as np

from lips.topology import RipsComplex
from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.plot import plot_surface, plot_points, plot_rips, init_surface
from contours.style import COLOR
from contours.config import CONFIG
import os,sys

import argparse

parser = argparse.ArgumentParser(prog='sample')

parser.add_argument('--dir', default=os.path.join('figures','sfa'), help='dir')
parser.add_argument('--surf', default='data/surf32.csv', help='surface file')
parser.add_argument('--file', default='data/surf-sample_329_2e-1.csv', help='sample file')
parser.add_argument('--dpi', type=int, default=300, help='dpi')
parser.add_argument('--save', action='store_true', help='save')
parser.add_argument('--mult', type=float, default=1., help='thresh mult')
parser.add_argument('--wait', type=float, default=0.5, help='wait')
parser.add_argument('--cmult', type=float, default=1., help='c mult')

plt.ion()
fig, ax = plt.subplots(figsize=(10,8))

if __name__ == '__main__':
    args = parser.parse_args()

    CFG = CONFIG['rainier' if 'rainier' in  args.surf else 'surf']
    RES, SHAPE, LIPS = CFG['res'], CFG['shape'], CFG['lips']
    CUTS, COLOR_ORDER, LABELS = CFG['cuts'], CFG['colors'], CFG['labels']
    xl,yl = CFG['shape'][0]*1.25, CFG['shape'][1]*1.25
    COLORS = [COLOR[k] for k in COLOR_ORDER]
    init_surface(ax, (-xl,xl), (-yl,yl))


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
    levels = [(a+b)/2 for a,b in zip(levels[:-1],levels[1:])]
    for i, t in enumerate(levels):
        for d in (1,2):
            for s in rips(d):
                if s.data['f'] <= t:
                    rips_plt[d][s].set_visible(True)
        plt.pause(args.wait)
        if args.save:
            cmult_s = ('cx' + np.format_float_scientific(args.cmult, trim='-')) if int(args.cmult) != args.mult else ''
            plt.savefig(os.path.join(args.dir, '%s_lips_tri%d%s.png' % (sample.name, i, cmult_s)), dpi=args.dpi, transparent=True)
