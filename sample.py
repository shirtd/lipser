
import matplotlib.pyplot as plt
import numpy as np

# from config.surf import *
# from lips.util.math import mk_gauss
# from plot.mpl import *

from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.plot import plot_rainier, plot_points, plot_rips, plot_balls
from contours.style import COLOR

from scipy.spatial import KDTree

import os, sys


RES = 337
SHAPE = (1,1)
# SAMP_PATH = 'data/surf-sample_329_2e-1.csv'
# MULT = 1.2

MIN = 265.258441
MAX = 4379.845434

# CUTS = MAX * np.array([0.0, 0.15, 0.28, 0.38, 0.48, 1.0]) + MIN
CUTS = [200, 1000, 1400, 1800, 2200, np.inf]
COLOR_ORDER = ['blue','green','yellow','salmon','purple']
COLORS = [COLOR[k] for k in COLOR_ORDER]


import argparse

parser = argparse.ArgumentParser(prog='sample')

parser.add_argument('--dir', default='data', help='dir')
parser.add_argument('--file', default='data/rainier_sub16.csv', help='file')
parser.add_argument('--load', default='data/rainier_sub16-sample_1094_1e-1.csv', help='file')
# parser.add_argument('--name', default='sample', help='name')
parser.add_argument('--thresh', type=float, default=1e-1, help='radius')
parser.add_argument('--no-add', action='store_true', help="load but don't add")

MARGIN = 0 # THRESH/2
LEVELS = 20 # CUTS


def get_sample(fig, ax, S, thresh, P=None, color=COLOR['red'], name='surf-sample', dir='data'):
    P = [] if P is None else P
    T = KDTree(S[:,:2])
    def onclick(event):
        p = S[T.query(np.array([event.xdata,event.ydata]))[1]]
        ax.add_patch(plt.Circle(p, thresh/2, color=color, alpha=0.5, zorder=3))
        ax.scatter(p[0], p[1], c='black', zorder=4, s=10)
        plt.pause(0.1)
        P.append(p)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    fig.canvas.mpl_disconnect(cid)
    return np.vstack(P)


# plt.ion()
fig, ax = plt.subplots(figsize=(9,9))

if __name__ == '__main__':
    args = parser.parse_args()

    surf = ScalarFieldData(args.file, make_grid(RES, SHAPE))
    surf_plt = plot_rainier(ax, surf, CUTS, COLORS, alpha=0.5, zorder=0)

    if args.load is not None:
        sample = SampleData(args.load)
        sample_plt = plot_points(ax, sample, color='black', alpha=0.5, s=5)
        ball_plt = plot_balls(ax, sample, np.ones(len(sample))*sample.radius/2, color=COLOR['salmon'], alpha=0.25)

    P = get_sample(fig, ax, surf.get_data(), args.thresh)
    # if args.load is not None and not args.no_add:
    #     P = np.vstack([sample.points, P])


    thresh_s = np.format_float_scientific(args.thresh, trim='-')
    name = '%s-sample' % surf.name
    fname = os.path.join(args.dir, '%s_%d_%s.csv' % (name, len(P), thresh_s))
    if input('save %s (y/*)? ' % fname) in {'y','Y','yes'}:
        print('saving %s' % fname)
        np.savetxt(fname, P)
