import numpy as np
import argparse
import os, sys

from lips.topology.util import sfa_dio
from lips.topology import RipsComplex, Filtration, Diagram
from contours import CONFIG, COLOR
from contours.surface import *
from contours.plot import *

from lips.geometry.util import lipschitz_grid


FILE='data/rainier_small/rainier_small8.csv'
SAMPLE_FILE='data/rainier_small/samples/rainier_small8-sample999_800.csv'
SUB_FILE=None

RHO=2/np.sqrt(3)
MULT=1. # RHO*2/np.sqrt(3)

parser = argparse.ArgumentParser(prog='lips')

parser.add_argument('surf', default=None, nargs='*', type=str, help='surface specification')
parser.add_argument('--data-dir', default='data', help='data directory')
parser.add_argument('--file', default=FILE, help='surface file')
parser.add_argument('--json', default=None, help='surface config')

# MODEL VARIABLES
parser.add_argument('--coef', type=float, default=RHO, help='rips coef')
parser.add_argument('--mult', type=float, default=MULT, help='radius multiplier')
parser.add_argument('--sub', action='store_true', help='run subsample rips')

# I/O VARIABLES
# parser.add_argument('--file', default=FILE, help='surface file')
parser.add_argument('--sample-file', default=SAMPLE_FILE, help='sample file')
parser.add_argument('--sub-file', default=SUB_FILE, help='subsample file')
parser.add_argument('--save', action='store_true', help='save plot')
parser.add_argument('--dpi', type=int, default=300, help='image dpi')
parser.add_argument('--tag', default='', help='file tag')
parser.add_argument('--dir', default='figures', help='output directory')

# VIZ VARIABLES
parser.add_argument('--nomin', action='store_true', help='dont plot min extension')
parser.add_argument('--nomax', action='store_true', help='dont plot max extension')
parser.add_argument('--show', action='store_true', help='show plot')
parser.add_argument('--wait', type=float, default=0.5, help='wait time (if --show)')

# PROGRAM VARIABLES
parser.add_argument('--barcode', action='store_true', help='run barcode')
parser.add_argument('--union', action='store_true', help='run offset union')
parser.add_argument('--rips', action='store_true', help='run rips')
parser.add_argument('--cover', action='store_true', help='just plot cover')
parser.add_argument('--nosample', action='store_true', help='just plot subsample')
parser.add_argument('--nosub', action='store_true', help='just plot sample')
parser.add_argument('--color', action='store_true', help='color complex by function values')
parser.add_argument('--partial', action='store_true', help='save partial sample')
parser.add_argument('--noim', action='store_true', help='don\'t do image persistence')
parser.add_argument('--surf', action='store_true', help='plot surface')


if __name__ == '__main__':
    args = parser.parse_args()

    if len(args.surf):
        args.file = os.path.join(args.data_dir, args.surf[0], f"{''.join(args.surf)}.csv")
    if args.json is None:
        args.json = f'{os.path.splitext(args.file)[0]}.json'

    # plt.ion()

    # CFG = CONFIG[os.path.splitext(os.path.basename(args.file))[0]]
    # COLORS = [COLOR[c] for c in CFG['colors']]
    # grid = make_grid(CFG['res'], CFG['shape'])
    # surf = ScalarFieldData(args.file, grid, CFG['lips'])
    # args.dir = os.path.join(args.dir, surf.name, 'lips')

    kwargs = {  'filt'      : { 'dir' : args.dir, 'save' : args.save, 'wait' : args.wait if args.show else None,
                                'dpi' : args.dpi, 'hide'  : { 'min' : args.nomin, 'max' : args.nomax}},
                'sample'    : { 'zorder' : 4, 'edgecolors' : 'black', 's' : 20 if args.sub else 5,
                                'facecolors' : 'none' if args.sub else 'black'},
                'subsample' : { 'c' : 'black', 's' : 5, 'zorder' : 5},
                'rips'      : { 'max'   : { 'visible' : False, 'zorder' : 2, 'color' : COLOR['blue']},
                                'min'   : { 'visible' : not (args.sub or args.nomin), 'zorder' : 1, 'color' : COLOR['red']}},
                'offset'    : { 'max'   : { 'visible' : not args.nomax, 'zorder' : 2, 'alpha' : 1 if args.union else 0.1,
                                            'color' : COLOR['blue1'] if args.union else COLOR['blue']},
                                'min'   : { 'visible' : True, 'zorder' : 1, 'alpha' : 1 if args.union else 0.1,
                                            'color' : COLOR['red1'] if args.union else COLOR['red']}},
                'cover'      : { 'visible' : True, 'zorder' : 1,
                                'color' : COLOR['red1'] if args.union else COLOR['red'],
                                'alpha' : 1 if args.union else 0.1},
                'barcode'   : { 'lw' : 3}}



    surf = ScalarFieldData(args.file, args.json)
    sample = SampleData(args.sample_file)
    levels = sample.get_levels(surf.cuts)

    if args.sub_file is not None:
        subsample = SampleData(args.sub_file, args.thresh)

    fig, ax = init_surface(surf.shape, surf.extents, surf.pad)

    if args.surf:
        surf_plt = surf.plot(ax, **kwargs['surf'])

    sub_str = f'sub-{subsample.name}' if args.sub else ''
    union_str = '-union' if args.union else ''
    no_str = 'min' if args.nomax else 'max' if args.nomin else ''
    no_str += '-nosub' if args.nosub else  ''
    no_str += '-sample' if args.nosample else ''
    color_str = '-color' if args.color else ''
    surf_str = '-color' if args.color else ''
    name = f'{sample.name}_{sub_str}lips{union_str}{no_str}{color_str}{surf_str}{args.tag}'

    if not args.nosample:
        sample_plt = sample.plot(ax, **kwargs['sample'])

    if args.rips:
        name = f'{name}_rips'
        rips = RipsComplex(sample.points, sample.radius * args.mult)
        if args.sub:
            subsample_plt = subsample.plot(ax, **kwargs['subsample'])
            rips.lips_sub(subsample, surf.lips)
        else:
            rips.lips(sample, surf.lips)
        rips_plt = plot_rips_filtration(ax, rips, levels, kwargs['rips'], name, **kwargs['filt'])
    # elif args.cover:
    #     name = f'{name}_cover'
    #     if args.sub:
    #         if not args.nosub:
    #             subsample_plt = plot_points(ax, subsample, **kwargs['subsample'])
    #         if args.color:
    #             del kwargs['cover']['color']
    #             colors = [COLOR[c] for c in CFG['colors']]
    #             kwargs['cover']['colors'] = [get_color(f, CFG['cuts'], colors) for f in subsample.function]
    #         cover_plt = plot_balls(ax, subsample, np.ones(len(subsample)) * sample.radius / 2 * args.mult, **kwargs['cover'])
    #     else:
    #         cover_plt = plot_balls(ax, sample, np.ones(len(sample)) * sample.radius / 2 * args.mult, **kwargs['cover'])
    #     if args.save:
    #         # t_str = np.format_float_scientific(t, trim='-')
    #         fname = os.path.join(args.dir, f'{name}.png')
    #         print(f'saving {fname}')
    #         plt.savefig(fname, dpi=args.dpi, transparent=True)
    else:
        name = f'{name}_offset'
        if args.sub:
            subsample_plt = subsample.plot(ax, **kwargs['subsample'])
            offset_plt = plot_offset_filtration(ax, subsample, surf.lips, levels, kwargs['offset'], name, **kwargs['filt'])
        else:
            offset_plt = plot_offset_filtration(ax, sample, surf.lips, levels, kwargs['offset'], name, **kwargs['filt'])

    # if args.barcode:
    #     fig, ax = init_barcode()
    #     grid = make_grid(CFG['res'], CFG['shape'])
    #     surf = ScalarFieldData(args.file, grid)
    #
    #     rips = RipsComplex(sample.points, sample.radius * args.mult * (1 if args.noim else args.coef))
    #     rips.lips_sub(subsample, CFG['lips'])
    #     if args.noim:
    #         max_filt = Filtration(rips, 'max')
    #     else:
    #         max_filt = Filtration(rips, 'max', filter=lambda s: s['dist'] <= sample.radius * args.mult)
    #     min_filt = Filtration(rips, 'min')
    #     hom = Diagram(rips, min_filt, pivot=max_filt, verbose=True)
    #
    #     smoothing = lambda p: [p[0]+CFG['lips']*sample.radius/4, p[1]-CFG['lips']*sample.radius/4]
    #     sample_dgms = hom.get_diagram(rips, min_filt, max_filt)#, smoothing=smoothing)
    #     surf_dgms = sfa_dio(surf.surface)
    #
    #     plot_barcode(ax[0], sample_dgms[1], **kwargs['barcode'], lw=CFG['lw'])
    #     plot_barcode(ax[1], surf_dgms[1], **kwargs['barcode'], lw=CFG['lw'])
    #
    #     if args.save:
    #         if not os.path.exists(args.dir):
    #             print(f'making directory {args.dir}')
    #             os.makedirs(args.dir)
    #         im_str = '-noim' if args.noim else ''
    #         fpath = os.path.join(args.dir, f'{name}_barcode{im_str}.png')
    #         print(f'saving {fpath}')
    #         plt.savefig(fpath, dpi=args.dpi, transparent=True)
    #     if args.show:
    #         plt.show()
