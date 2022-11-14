import matplotlib.pyplot as plt
import numpy as np
import argparse
import os, sys

from contours.args import parser
from contours.surface import ScalarFieldData
from contours.sample import MetricSampleData
from contours.config import COLOR, KWARGS
from lips.topology import RipsComplex


if __name__ == '__main__':
    args = parser.parse_args()


    surf = ScalarFieldData(args.file, args.json)
    sample = MetricSampleData(args.sample_file, surf.json_file, args.thresh)

    # TODO
    # if args.barcode:
    #     surf_dgms = surf.plot_barcode(args.folder, args.save, args.show, args.dpi, **KWARGS['barcode'])
    #
    # TODO pass a plot object
    # if args.contours:
    #     if args.cover:
    #         sample.plot_contours(args.show, args.save, args.folder, args.dpi)
    #     elif args.union:
    #         # TODO
    #     elif args.rips:
    #         # TODO

    fig, ax = surf.init_plot()
    if args.surf:
        surf_plt = surf.plot(ax, **KWARGS['surf'])
    sample.plot(ax, **KWARGS['sample'])

    if args.cover:
        cover_plt = sample.plot_cover(ax, args.color, **KWARGS['cover'])
    elif args.union:
        cover_plt = sample.plot_cover(ax, args.color, **KWARGS['union'])

    if args.rips or args.graph:
        rips = RipsComplex(sample.points, sample.radius)
        rips.sublevels(sample)
        sample.plot_rips(ax, rips, args.color, **KWARGS['rips' if args.rips else 'graph'])

    if args.save:
        folder = os.path.join(args.folder, surf.name, sample.name)
        surf.save_plot(sample.get_tag(args), folder, args.dpi)

    if args.show:
        plt.show()
