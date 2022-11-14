import numpy as np
import argparse
import os, sys

from contours import KWARGS, COLOR
from contours.surface import *
from contours.sample import *
from contours.plot import *

from lips.topology.util import sfa_dio
from lips.topology import RipsComplex, Filtration, Diagram

RES=8 # 16 # 32 #
DSET='rainier_small' # 'rainier_sub' # 'northwest' #
DIR=os.path.join('data')
DDIR=os.path.join(DIR, DSET)
SAMPLE='rainier_small8-sample666_1000.csv'

FILE=os.path.join(DDIR, f'{DSET}{RES}.csv') # None #
# JSON= None # os.path.join(DDIR, f'{DSET}{RES}.json')
SAMPLE_FILE=None # os.path.join(DDIR, 'samples', SAMPLE) #
SUB_FILE= None

MULT=1. # 4/3

parser = argparse.ArgumentParser(prog='surf')

parser.add_argument('file', default=FILE, help='surface file')
parser.add_argument('--json', default=None, help='surface config')

parser.add_argument('--sample-file', default=SAMPLE_FILE, help='sample file')
parser.add_argument('--tag', default='', help='file tag')

parser.add_argument('--show', action='store_true', help='show plot')
parser.add_argument('--save', action='store_true', help='save plot')
parser.add_argument('--folder', default=os.path.join('figures','surf'), help='figure output directory')
parser.add_argument('--dpi', type=int, default=300, help='image dpi')

parser.add_argument('--contours', action='store_true', help='plot contours')

# PROGRAM ARGS
parser.add_argument('--barcode', action='store_true', help='plot barcode')
parser.add_argument('--sample', action='store_true', help='sample surface')
parser.add_argument('--thresh', type=float, default=None, help='cover radius')
parser.add_argument('--greedy', action='store_true', help='greedy sample')


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
