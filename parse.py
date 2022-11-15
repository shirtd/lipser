import matplotlib.pyplot as plt
import numpy as np
import argparse
import os, sys


from contours.args import parser
from contours.surface import USGSScalarFieldData
from contours.config import COLOR, KWARGS


if __name__ == '__main__':
    args = parser.parse_args()

    surf = USGSScalarFieldData(args.file, args.cuts, args.colors, args.pad, args.lips, args.downsample)

    if args.show:
        fig, ax = surf.init_plot()
        surf_plt = surf.plot(ax, **KWARGS['surf'])
        plt.show()

    if args.save:
        surf.save()
