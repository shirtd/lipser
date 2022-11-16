import matplotlib.pyplot as plt
import numpy as np
import argparse
import os, sys


from contours.args import parser
from contours.surface import USGSScalarFieldData, GaussianScalarFieldData
from contours.config import COLOR, KWARGS


if __name__ == '__main__':
    args = parser.parse_args()

    if args.gauss:
        name = 'surf'
        folder = os.path.join('data', name)
        colors = ['green', 'blue', 'purple', 'yellow']
        colors = [COLOR[c] for c in colors]
        cuts = [0.05, 0.3, 0.55, 0.8, 1.35]
        # cuts = [5, 30, 55, 80, 135]
        pad = 1.5 #  150 # 1.5
        # extents = [[-200, 200], [-100, 100]]
        extents = [[-2, 2], [-1, 1]]
        lips = None # 3.1554220918348532
        gauss_args = [  (1,     [-0.2, 0.2],    [0.3, 0.3]),
                        (0.5,   [-1.3, -0.1],   [0.15, 0.15]),
                        (0.7,   [-0.8, -0.4],   [0.2, 0.2]),
                        (0.8,   [-0.8, -0],     [0.4, 0.4]),
                        (0.4,   [0.6, 0.0],     [0.4, 0.2]),
                        (0.7,   [1.25, 0.3],    [0.25, 0.25])]
        scale = 1
        surf = GaussianScalarFieldData(name, folder, gauss_args, extents, args.resolution,
                                        cuts, colors, pad, args.downsample, lips, scale)
    else:
        surf = USGSScalarFieldData(args.file, args.cuts, args.colors, args.pad, args.downsample)

    if args.show:
        fig, ax = surf.init_plot()
        surf_plt = surf.plot(ax, **KWARGS['surf'])
        plt.show()

    if args.save:
        surf.save()
