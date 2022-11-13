import numpy as np
import argparse
import os, sys

from contours import CONFIG, COLOR
from contours.surface import *
from contours.plot import *

from lips.topology.util import sfa_dio
from lips.topology import RipsComplex, Filtration, Diagram
from lips.geometry.util import lipschitz_grid, greedysample

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
# parser.add_argument('--subsample', action='store_true', help='subsample surface')
parser.add_argument('--thresh', type=float, default=None, help='cover radius')

# RIPS
parser.add_argument('--wait', type=float, default=0.5, help='wait')
parser.add_argument('--rips', action='store_true', help='run rips')
parser.add_argument('--graph', action='store_true', help='just plot graph')
parser.add_argument('--coef', default=1.)#MULT*2/np.sqrt(3), type=float, help='rips coef')

# LIPS
parser.add_argument('--lips', action='store_true', help='run lips')
parser.add_argument('--sfa', action='store_true', help='run sfa')
parser.add_argument('--greedy', action='store_true', help='greedy sample')

LW=0.3
SIZE=1

if __name__ == '__main__':
    args = parser.parse_args()

    if len(args.surf):
        args.file = os.path.join(args.data_dir, args.surf[0], f"{''.join(args.surf)}.csv")
    if args.json is None:
        args.json = f'{os.path.splitext(args.file)[0]}.json'

    kwargs = {  'surf'      : { 'zorder' : 0, 'alpha' : 0.5},
                'sample'    : { 'zorder' : 10, 'edgecolors' : 'black', 's' : SIZE, 'color' : 'black'},
                'cover'     : { 'visible' : True, 'zorder' : 2, 'alpha' : 1 if args.union else 0.2,
                                'color' : COLOR['red1'] if args.union else COLOR['red']},
                'offset'    : { 'visible' : False, 'zorder' : 2,
                                'color' : COLOR['red1'] if args.union else COLOR['red'],
                                'alpha' : 1 if args.union else 0.3},
                'filt'      : { 'dir' : args.dir, 'save' : args.save,
                                'wait' : args.wait if args.show else None, 'dpi' : args.dpi},
                'rips'      : { 'f' : {'visible' : False, 'zorder' : 1, 'color' : COLOR['red'],
                                        'fade' : [1, 1, 0 if args.graph else 0.6], 'lw' : LW}},
                'barcode'   : { 'lw' : 5}}

    surf = ScalarFieldData(args.file, args.json)
    if args.sample_file is not None:
        sample = SampleData(args.sample_file, args.thresh)
        levels = sample.get_levels(surf.cuts)
        if args.thresh is None:
            args.thresh = sample.radius
    else:
        sample = None

    if args.contours:
        surf_plt = surf.plot_contours(args.show, args.save, args.dir, args.dpi)

    fig, ax = init_surface(surf.shape, surf.extents, surf.pad)
    if not args.nosurf:
        surf_plt = surf.plot(ax, **kwargs['surf'])

    if args.sample:
        surf.sample(fig, ax, args.thresh, surf.cuts[0], args.greedy, sample)
    elif args.sample_file is not None:
        sample_plt = sample.plot(ax, **kwargs['sample'])
        if args.cover or args.union:
            if args.color:
                del kwargs['cover']['color']
                kwargs['cover']['colors'] = [get_color(f, surf.cuts, surf.colors) for f in sample.function]
                kwargs['cover']['zorders'] = [get_cut(f, surf.cuts, kwargs['cover']['zorder']+1) for f in sample.function]
                del kwargs['cover']['zorder']
            cover_plt = sample.plot_cover(ax, **kwargs['cover'])

        if args.rips or args.graph:
            rips = RipsComplex(sample.points, sample.radius*args.coef, verbose=True)
            rips.sublevels(sample)
            if args.color:
                del kwargs['rips']['f']['color']
                kwargs['rips']['f']['tri_colors'] = [get_color(sample(t).max(), surf.cuts, surf.colors) for t in rips(2)]
            print(' plotting rips...')
            rips_plt = {k : plot_rips(ax, rips, **v) for k,v in kwargs['rips'].items()}
            print('\tdone')
            for i, t in enumerate(levels):
                for d in (1,2):
                    for s in rips(d):
                        for k,v in rips_plt.items():
                            if s.data[k] <= t:
                                rips_plt[k][d][s].set_visible(not kwargs['rips'][k]['visible'])
                if args.show and args.wait is not None:
                    plt.pause(args.wait)
                if args.save:
                    sample_str = '' if args.sample_file is None else sample.get_tag(args)
                    surf.save_plot(args.dir, dpi=args.dpi, name=sample_str, tag=format_float(t))
        elif args.sfa:
            name = f'{surf.name}_offset'
            if args.color:
                del kwargs['offset']['color']
                kwargs['offset']['colors'] = [get_color(f, surf.cuts, surf.colors) for f in sample.function]
                kwargs['offset']['zorders'] = [get_cut(f, surf.cuts, kwargs['offset']['zorder']+1) for f in sample.function]
                del kwargs['offset']['zorder']
            offset_plt = plot_sfa(ax, sample, levels, kwargs['offset'], name, **kwargs['filt'])

    if args.save:
        sample_str = surf.name if args.sample_file is None else sample.get_tag(args)
        surf.save_plot(args.dir, dpi=args.dpi, name=sample_str)

    if args.barcode:
        bar_fig, bar_ax = init_barcode()
        surf_dgms = sfa_dio(surf.surface)
        barcode_plt = plot_barcode(bar_ax, surf_dgms[1], surf.cuts, surf.colors, **kwargs['barcode'])
        if args.save:
            surf.save_plot(args.dir, 'barcode')

    if args.show:
        plt.show()
