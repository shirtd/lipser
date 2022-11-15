import matplotlib.pyplot as plt
import numpy as np
import argparse
import os, sys

from contours.args import parser
# from contours.surface import ScalarFieldFile
from contours.sample import MetricSampleFile
from contours.config import COLOR, KWARGS
from lips.topology import RipsComplex


if __name__ == '__main__':
    args = parser.parse_args()

    color_str = '-color' if args.color else ''

    # surf = ScalarFieldData(args.file, args.json)
    sample = MetricSampleFile(args.file) #, surf.json_file, args.thresh)
    args.folder = os.path.join(args.folder, sample.parent, sample.name)

    if args.cover or args.union:
        key = 'cover' if args.cover else 'union'
    elif args.rips or args.graph:
        key = 'rips' if args.rips else 'graph'
        rips = RipsComplex(sample.points, sample.radius)
        rips.sublevels(sample)


    if args.contours:
        if args.cover or args.union:
            sample.plot_cover_filtration(args.show, args.save, args.folder, args.color, args.dpi, f'{key}{color_str}', **KWARGS[key])
        elif args.rips or args.graph:
            sample.plot_rips_filtration(rips, args.show, args.save, args.folder, args.color, args.dpi, f'{key}{color_str}', **KWARGS[key])

    # TODO
    # if args.barcode:
    #     surf_dgms = surf.plot_barcode(args.folder, args.save, args.show, args.dpi, **KWARGS['barcode'])

    fig, ax = sample.init_plot()
    # if args.surf:
    #     surf_plt = surf.plot(ax, **KWARGS['surf'])
    sample.plot(ax, **KWARGS['sample'])

    if args.cover or args.union:
        cover_plt = sample.plot_cover(ax, args.color, **KWARGS[key])
        if args.save:
            sample.save_plot(args.folder, args.dpi, f"{key}{color_str}", '-')
    elif args.rips or args.graph:
        rips_plt = sample.plot_rips(ax, rips, args.color, **KWARGS[key])
        if args.save:
            sample.save_plot(args.folder, args.dpi, f"{key}{color_str}", '-')

    if args.show:
        print('close plot to exit')
        plt.show()
