import matplotlib.pyplot as plt
import numpy as np
import argparse
import os, sys

from contours.args import parser
from contours.surface import ScalarFieldData
from contours.config import COLOR, KWARGS

# from contours import KWARGS, COLOR
# from contours.surface import *
# from contours.sample import *
# from contours.plot import *
#
# from lips.topology.util import sfa_dio
# from lips.topology import RipsComplex, Filtration, Diagram


if __name__ == '__main__':
    args = parser.parse_args()


    surf = ScalarFieldData(args.file, args.json)

    if args.contours:
        surf.plot_contours(args.show, args.save, args.folder, args.dpi)

    fig, ax = surf.init_plot()
    surf_plt = surf.plot(ax, **KWARGS['surf'])

    # TODO
    # still need to refactor Sample as a subclass of Data/DataFile
    # need to pass json to sample!
    # if args.sample:
    #     if args.sample_file is not None:
    #         sample = SampleData(args.sample_file, args.thresh)
    #         if args.thresh is None:
    #             args.thresh = sample.radius
    #     else:
    #         sample = None
    #     surf.sample(fig, ax, args.thresh, surf.cuts[0], args.greedy, sample)

    if args.save:
        name = surf.name if args.sample_file is None else sample.get_tag(args)
        surf.save_plot(name, args.folder, args.dpi)

    # TODO
    # surf.barcode(bar_ax, surf_dgms[1], **kwargs['barcode'])
    # if args.barcode:
    #     bar_fig, bar_ax = init_barcode()
    #     surf_dgms = sfa_dio(surf.surface)
    #     barcode_plt = plot_barcode(bar_ax, surf_dgms[1], surf.cuts, surf.colors, **kwargs['barcode'])
    #     if args.save:
    #         surf.save_plot(args.dir, 'barcode')

    if args.show:
        plt.show()
