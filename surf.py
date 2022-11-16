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

    if args.sample or args.greedy:
        sample.plot(ax, **KWARGS['sample'])
        sample.plot_cover(ax, **KWARGS['union' if args.union else 'cover'])

    if args.save:
        if args.sample_file is None:
            surf.save_plot(args.folder, args.dpi)
        else:
            sample.save_plot(os.path.join(args.folder, sample.name), args.dpi)

    if args.show:
        if sample is None:
            plt.show()
        else:
            plt.pause(0.1)
            if args.force or input(f'save {sample.name} (y/*)? ') == 'y':
                sample.save(sample.get_data())
