import matplotlib.pyplot as plt
import numpy as np
import argparse
import os, sys

from contours.args import parser
from contours.sample import MetricSampleFile
from contours.surface import ScalarFieldFile
from contours.config import COLOR, KWARGS


if __name__ == '__main__':
    args = parser.parse_args()

    surf = ScalarFieldFile(args.file, args.json)
    args.folder = os.path.join(args.folder, surf.name, 'surf')


    if args.barcode:
        surf_dgms = surf.plot_barcode(args.folder, args.save, args.show, args.dpi, **KWARGS['barcode'])

    if args.contours:
        surf.plot_contours(args.show, args.save, args.folder, args.dpi)

    sample = None
    if args.greedy:
        sample = surf.greedy_sample(args.thresh, args.mult)
    elif args.sample_file is not None:
        sample = MetricSampleFile(args.sample_file)

    if args.sample:
        sample = surf.sample(args.thresh, sample)

    fig, ax = surf.init_plot()
    surf_plt = surf.plot(ax, **KWARGS['surf'])

    if sample is not None:
        sample.plot(ax, **KWARGS['sample'])
        sample.plot_cover(ax, **KWARGS['union' if args.union else 'cover'])
        if args.save:
            sample.save_plot(args.folder, args.dpi)
        if args.show:
            plt.pause(0.1)
        if args.force or input(f'save {sample.name} (y/*)? ') == 'y':
            sample.save(sample.get_data())
    else:
        if args.save:
            surf.save_plot(args.folder, args.dpi)
        if args.show:
            plt.show()
