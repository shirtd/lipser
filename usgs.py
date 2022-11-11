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
# CUTS=[200, 1000, 1400, 1800, 2500, 4500]
CUTS=[1850, 2130, 2585, 3180, 4175, 4500]

parser = argparse.ArgumentParser(prog='rainier')

parser.add_argument('file', help='surface file')
parser.add_argument('--name', default=None, help='data name')
parser.add_argument('--dir', default=None, help='data directory')
parser.add_argument('--downsample', default=None, type=int, help='downsample')
parser.add_argument('--cuts', default=CUTS, nargs='+', type=float, help='cuts')
parser.add_argument('--colors', default=['blue','green','yellow','salmon','purple'], nargs='+', type=str, help='colors')
parser.add_argument('--pad', default=0, help='padding')
parser.add_argument('--lips', default=None, type=float, help='lipschitz constant')
parser.add_argument('--show', action='store_true')
parser.add_argument('--save', action='store_true')


if __name__ == '__main__':
    args = parser.parse_args()
    args.colors = [COLOR[c] for c in args.colors]

    surf = USGSScalarField(args.file, args.dir, args.name, args.downsample)

    if args.show:
        print(surf.shape)
        print(surf.extents)
        fig, ax = init_surface(surf.shape, surf.extents, args.pad)
        surf_plt = surf.plot(ax, args.cuts, args.colors)
        plt.show()

    if args.save:
        surf.save({'cuts' : args.cuts, 'colors' : args.colors, 'pad' : args.pad})
