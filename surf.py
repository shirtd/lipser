import matplotlib.pyplot as plt
import numpy as np
import argparse
import os, sys

from contours.args import parser
from contours.surface import ScalarFieldData
from contours.config import COLOR, KWARGS


if __name__ == '__main__':
    args = parser.parse_args()

    surf = ScalarFieldData(args.file, args.json)

    if args.barcode:
        surf_dgms = surf.plot_barcode(args.folder, args.save, args.show, args.dpi, **KWARGS['barcode'])

    if args.contours:
        surf.plot_contours(args.show, args.save, args.folder, args.dpi)

    if args.sample:
        surf.sample(args.thresh, args.greedy, args.sample_file)

    fig, ax = surf.init_plot()
    surf_plt = surf.plot(ax, **KWARGS['surf'])

    if args.save:
        folder = os.path.join(args.folder, surf.name)
        name = surf.name if args.sample_file is None else sample.get_tag(args)
        surf.save_plot(name, folder, args.dpi)

    if args.show:
        plt.show()
