import matplotlib.pyplot as plt
import numpy as np
import argparse
import os, sys

from contours.args import parser
from contours.surface import ScalarFieldFile
from contours.config import COLOR, KWARGS


if __name__ == '__main__':
    args = parser.parse_args()

    surf = ScalarFieldFile(args.file, args.json)
    args.folder = os.path.join(args.folder, surf.name)

    if args.barcode:
        surf_dgms = surf.plot_barcode(args.folder, args.save, args.show, args.dpi, **KWARGS['barcode'])

    if args.contours:
        surf.plot_contours(args.show, args.save, args.folder, args.dpi)

    if args.sample:
        # if args.thresh is None:
        #     args.thresh = 1000
        # sample = surf.sample(args.thresh, args.greedy, args.sample_file)
        sample = surf.greedy_sample(args.thresh, args.mult)
        if args.save:# or input('save %s (y/*)? ' % sample.name) in {'y','Y','yes'}:
            sample.save(sample.get_data())

    fig, ax = surf.init_plot()
    surf_plt = surf.plot(ax, **KWARGS['surf'])

    if args.save:
        if args.sample_file is None:
            surf.save_plot(args.folder, args.dpi)
        else:
            sample.save_plot(os.path.join(args.folder, sample.name), args.dpi)

    if args.show:
        plt.show()
