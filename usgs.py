import numpy as np
import argparse
import os, sys, json

from contours import CONFIG, COLOR
from contours.surface import *
from contours.plot import *

from lips.topology.util import sfa_dio
from lips.geometry.util import lipschitz_grid
from lips.util.array import down_sample

DATA_DIR = os.path.join('data','rainier')
CUTS=[200, 1000, 1400, 1800, 2500, 4500]
# CUTS=[1850, 2130, 2585, 3180, 4175, 4500]

parser = argparse.ArgumentParser(prog='rainier')

parser.add_argument('file', help='surface file')
parser.add_argument('--name', default=None, help='data name')
parser.add_argument('--dir', default=None, help='data directory')
parser.add_argument('--downsample', default=None, type=int, help='downsample')
parser.add_argument('--cuts', default=CUTS, nargs='+', type=float, help='cuts')
parser.add_argument('--colors', default=['blue','green','yellow','salmon','purple'], nargs='+', type=str, help='colors')
parser.add_argument('--pad', default=[1.3, 1.3], nargs=2, help='padding')
parser.add_argument('--lips', default=None, type=float, help='lipschitz constant')
parser.add_argument('--show', action='store_true')
parser.add_argument('--save', action='store_true')


if __name__ == '__main__':
    args = parser.parse_args()
    args.colors = [COLOR[c] for c in args.colors]

    surf = USGSScalarFieldRaw(args.file, args.dir, args.name, args.downsample)

    if args.show:
        fig, ax = init_surface(surf.surface.shape, surf.extents)
        surf_plt = plot_surface(ax, surf, args.cuts, args.colors, zorder=0, alpha=0.5)
        plt.show()

    if args.save:
        surf.save({'cuts' : args.cuts, 'colors' : args.colors, 'pad' : args.pad})



# def measure(lon1, lat1, lon2, lat2):
#     R = 6378.137
#     dLat = lat2 * np.pi / 180 - lat1 * np.pi / 180
#     dLon = lon2 * np.pi / 180 - lon1 * np.pi / 180;
#     a = (np.sin(dLat/2) * np.sin(dLat/2) + np.cos(lat1 * np.pi / 180)
#         * np.cos(lat2 * np.pi / 180) * np.sin(dLon/2) * np.sin(dLon/2))
#     return 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)) * R * 1000

# def deg_to_meters(extents):
#     return[[0, measure(extents[0][0],extents[1][0],extents[0][1],extents[1][0])],
#             [0],0,extents[0][0],extents[1][0])
#     ya = measure(0,0,extents[0][0],extents[1][1])
