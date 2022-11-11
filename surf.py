import numpy as np
import argparse
import os, sys

from contours import CONFIG, COLOR
from contours.surface import *
from contours.plot import *

from lips.topology.util import sfa_dio
from lips.geometry.util import lipschitz_grid

RES=8 # 16 # 32 #
DSET='rainier_small' # 'rainier_sub' # 'northwest' #
DIR=os.path.join('data')
DDIR=os.path.join(DIR, DSET)
SAMPLE='rainier_small8-666_1000.csv'

FILE= None # os.path.join(DDIR, f'{DSET}{RES}.csv')
# JSON= None # os.path.join(DDIR, f'{DSET}{RES}.json')
SAMPLE_FILE=None # os.path.join(DDIR, 'samples', SAMPLE)
SUB_FILE= None

parser = argparse.ArgumentParser(prog='surf')

parser.add_argument('surf', default=None, nargs='*', type=str, help='surface specification')
parser.add_argument('--data-dir', default='data', help='data directory')
parser.add_argument('--file', default=FILE, help='surface file')
parser.add_argument('--json', default=None, help='surface config')

parser.add_argument('--sample-file', default=SAMPLE_FILE, help='sample file')
parser.add_argument('--sub-file', default=SUB_FILE, help='subsample file')
parser.add_argument('--tag', default='', help='file tag')

parser.add_argument('--show', action='store_true', help='show plot')
parser.add_argument('--save', action='store_true', help='save plot')
parser.add_argument('--dir', default=os.path.join('figures','surf'), help='figure output directory')
parser.add_argument('--dpi', type=int, default=300, help='image dpi')

# VISUALIZATION ARGS
parser.add_argument('--nosurf', action='store_true', help='hide surf')
parser.add_argument('--color', action='store_true', help='color plot')
parser.add_argument('--cover', action='store_true', help='plot cover')
parser.add_argument('--union', action='store_true', help='plot union of cover')
parser.add_argument('--contours', action='store_true', help='plot contours')

# PROGRAM ARGS
parser.add_argument('--barcode', action='store_true', help='plot barcode')
parser.add_argument('--sample', action='store_true', help='sample surface')
parser.add_argument('--subsample', action='store_true', help='subsample surface')
parser.add_argument('--thresh', type=float, default=None, help='cover radius')


if __name__ == '__main__':
    args = parser.parse_args()

    if len(args.surf):
        args.file = os.path.join(args.data_dir, args.surf[0], f"{''.join(args.surf)}.csv")
    if args.json is None:
        args.json = f'{os.path.splitext(args.file)[0]}.json'

    kwargs = {  'surf'      : { 'zorder' : 0, 'alpha' : 0.5},
                'sample'    : { 'zorder' : 10, 'edgecolors' : 'black', 's' : 5, 'color' : 'black'},
                'cover'     : { 'visible' : True, 'zorder' : 2,
                                'color' : COLOR['red1'] if args.union else COLOR['red'],
                                'alpha' : 1 if args.union else 0.2},
                'barcode'   : { 'lw' : 5}}


    surf = ScalarFieldData(args.file, args.json)
    print(surf.pad)
    if args.sample_file is not None:
        sample = SampleData(args.sample_file, args.thresh)
        if args.thresh is None:
            args.thresh = sample.radius
    # if args.subsample_file is not None:
    #     subsample = SubsampleData(args.subsample_file, sample, args.thresh)

    if args.contours:
        surf_plt = surf.plot_contours(args.show, args.save, args.dir, args.dpi)

    fig, ax = init_surface(surf.shape, surf.extents, surf.pad)
    if not args.nosurf:
        surf_plt = surf.plot(ax, **kwargs['surf'])

    if args.sample:
        surf.sample(fig, ax, args.thresh, sample)
    # if args.subsample:
    #     sample.subsample(fig, ax, args.thresh, subsample)
    elif args.sample_file is not None:
        sample_plt = sample.plot(ax, **kwargs['sample'])
        if args.cover or args.union:
            if args.color:
                del kwargs['cover']['color']
                kwargs['cover']['colors'] = [get_color(f, surf.cuts, surf.colors) for f in sample.function]
                kwargs['cover']['zorders'] = [get_cut(f, surf.cuts, kwargs['cover']['zorder']+1) for f in sample.function]
                del kwargs['cover']['zorder']
            cover_plt = sample.plot_cover(ax, **kwargs['cover'])

    if args.save:
        sample_str = '' if args.sample_file is None else sample.get_tag(args)
        surf.save_plot(args.dir, sample_str, args.dpi)

    if args.barcode:
        bar_fig, bar_ax = init_barcode()
        surf_dgms = sfa_dio(surf.surface)
        barcode_plt = plot_barcode(bar_ax, surf_dgms[1], surf.cuts, surf.colors, **kwargs['barcode'])
        if args.save:
            surf.save_plot(args.dir, 'barcode')

    if args.show:
        plt.show()
