import numpy as np
import argparse
import os, sys

from lips.topology.util import sfa_dio
from lips.topology import RipsComplex, Filtration, Diagram
from contours import CONFIG, COLOR
from contours.surface import *
from contours.plot import *


parser = argparse.ArgumentParser(prog='lips')

parser.add_argument('--file', default='data/surf32.csv', help='surface file')
parser.add_argument('--sample-file', default='data/surf32-sample-1233_1.3e-01.csv', help='sample file')
parser.add_argument('--mult', type=float, default=1., help='thresh mult')
parser.add_argument('--show', action='store_true', help='show plot')
parser.add_argument('--wait', type=float, default=0.5, help='wait')
parser.add_argument('--save', action='store_true', help='save')
parser.add_argument('--dpi', type=int, default=300, help='dpi')
parser.add_argument('--tag', default='', help='file tag')
parser.add_argument('--dir', default='figures', help='dir')
parser.add_argument('--rips', action='store_true', help='run rips')
parser.add_argument('--union', action='store_true', help='run offset union')
parser.add_argument('--barcode', action='store_true', help='run barcode')
parser.add_argument('--color', action='store_true', help='color complex by function values')
parser.add_argument('--noim', action='store_true', help='don\'t do image persistence')
parser.add_argument('--graph', action='store_true', help='just plot graph')
parser.add_argument('--coef', default=2/np.sqrt(3), type=float, help='rips coef')


if __name__ == '__main__':
    args = parser.parse_args()

    CFG = CONFIG[os.path.splitext(os.path.basename(args.file))[0]]
    COLORS = [COLOR[c] for c in CFG['colors']]
    grid = make_grid(CFG['res'], CFG['shape'])
    surf = ScalarFieldData(args.file, grid, CFG['lips'])
    args.dir = os.path.join(args.dir, surf.name, 'rips')

    kwargs = {  'surf'      : { 'zorder' : 0, 'alpha' : 0.5},
                'filt'      : { 'dir' : args.dir, 'save' : args.save, 'wait' : args.wait if args.show else None, 'dpi' : args.dpi},
                'sample'    : { 'zorder' : 10, 'edgecolors' : 'black', 's' : 5, 'color' : 'black'},
                'rips'      : { 'f' : {'visible' : False, 'zorder' : 1, 'color' : COLOR['red'], 'fade' : [1, 0.5, 0 if args.graph else 0.15]}},
                'offset'    : { 'visible' : False, 'zorder' : 2,
                                'color' : COLOR['red1'] if args.union else COLOR['red'],
                                'alpha' : 1 if args.union else 0.1},
                'barcode'   : { 'cuts' : CFG['cuts'], 'colors' : [COLOR[c] for c in CFG['colors']]}}

    sample = SampleData(args.sample_file)
    levels = sample.get_levels(CFG['cuts'])

    union_str = '-union' if args.union else ''
    name = f'{sample.name}_rips{union_str}'

    if args.barcode:
        fig, ax = init_barcode()
        grid = make_grid(CFG['res'], CFG['shape'])
        surf = ScalarFieldData(args.file, grid)

        rips = RipsComplex(sample.points, sample.radius * args.mult * (1 if args.noim else args.coef))
        rips.sublevels(sample)
        filt = Filtration(rips, 'f')
        pivot = filt if args.noim else Filtration(rips, 'f', filter=lambda s: s['dist'] <= sample.radius * args.mult)
        hom =  Diagram(rips, filt, pivot=pivot, verbose=True)

        sample_dgms = hom.get_diagram(rips, filt, pivot)
        surf_dgms = sfa_dio(surf.surface)

        plot_barcode(ax[0], sample_dgms[1], **kwargs['barcode'], lw=CFG['lw'])
        plot_barcode(ax[1], surf_dgms[1], **kwargs['barcode'], lw=CFG['lw'])

        if args.save:
            if not os.path.exists(args.dir):
                print(f'making directory {args.dir}')
                os.makedirs(args.dir)
            im_str = '-noim' if args.noim else ''
            fpath = os.path.join(args.dir, f'{name}_barcode{im_str}.png')
            print(f'saving {fpath}')
            plt.savefig(fpath, dpi=args.dpi, transparent=True)
        if args.show:
            plt.show()
    else:
        if args.show:
            plt.ion()
        fig, ax = init_surface(CFG['shape'], CFG['pad'], 10)
        sample_plt = plot_points(ax, sample, **kwargs['sample'])

        if args.rips or args.graph:
            name = f'{name}_rips' if args.rips else f'{name}_graph'
            # if args.graph:
            #     surf_plt = surf.plot(ax, CFG['cuts'], COLORS, **kwargs['surf'])
            rips = RipsComplex(sample.points, sample.radius * args.mult)
            rips.sublevels(sample)
            if args.color:
                name += '_color'
                del kwargs['rips']['f']['color']
                kwargs['rips']['f']['tri_colors'] = [get_color(sample(t).max(), CFG['cuts'], [COLOR[c] for c in CFG['colors']]) for t in rips(2)]
            rips_plt = plot_rips_filtration(ax, rips, levels, kwargs['rips'], name, **kwargs['filt'])
        else:
            name = f'{name}_offset'
            if args.color:
                del kwargs['offset']['color']
                kwargs['offset']['colors'] = [get_color(f, CFG['cuts'], [COLOR[c] for c in CFG['colors']]) for f in sample.function]
                kwargs['offset']['zorders'] = [get_cut(f, CFG['cuts'], kwargs['offset']['zorder']+1) for f in sample.function]
                del kwargs['offset']['zorder']
            offset_plt = plot_sfa(ax, sample, levels, kwargs['offset'], name, **kwargs['filt'])
