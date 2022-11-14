import matplotlib.pyplot as plt
import numpy as np
import argparse
import os, sys

from contours import COLOR, KWARGS
from contours.surface import USGSScalarField


DATA_DIR = os.path.join('data','test')
CUTS=[200, 1000, 1400, 1800, 2500, 4500]
COLORS=[COLOR[c] for c in ['blue','green','yellow','salmon','purple']]

parser = argparse.ArgumentParser(prog='parse')

parser.add_argument('file', help='surface file')
parser.add_argument('--downsample', default=None, type=int, help='downsample')
parser.add_argument('--cuts', default=CUTS, nargs='+', type=float, help='cuts')
parser.add_argument('--colors', default=COLORS, nargs='+', type=str, help='colors')
parser.add_argument('--pad', default=0, help='padding')
parser.add_argument('--lips', default=None, type=float, help='lipschitz constant')
parser.add_argument('--show', action='store_true')
parser.add_argument('--save', action='store_true')


if __name__ == '__main__':
    args = parser.parse_args()

    surf = USGSScalarField(args.file, args.cuts, args.colors, args.pad, args.lips, args.downsample)

    if args.show:
        fig, ax = surf.init_plot()
        surf_plt = surf.plot(ax, **KWARGS['surf'])
        plt.show()

    if args.save:
        surf.save()
