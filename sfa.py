import numpy as np
import argparse
import os, sys

from lips.topology.util import sfa_dio
from lips.topology import RipsComplex, Filtration, Diagram
from contours import CONFIG, COLOR
from contours.surface import *
from contours.plot import *


parser = argparse.ArgumentParser(prog='lips')

parser.add_argument('--surf', default='data/surf32.csv', help='surface file')
parser.add_argument('--file', default='data/surf-sample_1067_1.3e-1.csv', help='sample file')
parser.add_argument('--mult', type=float, default=1., help='thresh mult')
parser.add_argument('--show', action='store_true', help='show plot')
parser.add_argument('--wait', type=float, default=0.5, help='wait')
parser.add_argument('--save', action='store_true', help='save')
parser.add_argument('--dpi', type=int, default=300, help='dpi')
parser.add_argument('--tag', default='', help='file tag')
parser.add_argument('--dir', default=os.path.join('figures', 'rips'), help='dir')
parser.add_argument('--rips', action='store_true', help='run rips')
parser.add_argument('--union', action='store_true', help='run offset union')
parser.add_argument('--barcode', action='store_true', help='run barcode')
parser.add_argument('--color', action='store_true', help='color complex by function values')


if __name__ == '__main__':
    args = parser.parse_args()

    CFG = CONFIG['rainier' if 'rainier' in  args.file else 'surf']
    COLORS = [COLOR[c] for c in CFG['colors']]
    kwargs = {  'filt'      : { 'dir' : args.dir, 'save' : args.save, 'wait' : args.wait if args.show else None, 'dpi' : args.dpi},
                'sample'    : { 'zorder' : 4, 'edgecolors' : 'black', 's' : 9, 'color' : 'black'},
                'rips'      : { 'f' : {'visible' : False, 'zorder' : 1, 'color' : COLOR['red']}}, # 'fade' : [1, 0.5, 0.3]}},
                'offset'    : { 'visible' : False, 'zorder' : 2,
                                'color' : COLOR['red1'] if args.union else COLOR['red'],
                                'alpha' : 1 if args.union else 0.1},
                'barcode'   : { 'cuts' : CFG['cuts'], 'colors' : [COLOR[c] for c in CFG['colors']]}}

    sample = SampleData(args.file)
    levels = sample.get_levels(CFG['cuts'])

    union_str = '-union' if args.union else ''
    name = f'{sample.name}_rips{union_str}'

    if args.barcode:
        fig, ax = init_barcode()
        grid = make_grid(CFG['res'], CFG['shape'])
        surf = ScalarFieldData(args.surf, grid)

        rips = RipsComplex(sample.points, sample.radius * args.mult)
        rips.sublevels(sample)
        filt = Filtration(rips, 'f')
        hom =  Diagram(rips, filt, pivot=filt, verbose=True)

        sample_dgms, _ = hom.get_diagram(rips, filt, filt)
        surf_dgms = sfa_dio(surf.surface)

        plot_barcode(ax[0], sample_dgms[1], **kwargs['barcode'])
        plot_barcode(ax[1], surf_dgms[1], **kwargs['barcode'])

        if args.save:
            if not os.path.exists(args.dir):
                print(f'making directory {args.dir}')
                os.makedirs(args.dir)
            fpath = os.path.join(args.dir, f'{name}_barcode.png')
            print(f'saving {fpath}')
            plt.savefig(fpath, dpi=args.dpi, transparent=True)
        if args.show:
            plt.show()
    else:
        # if args.show:
        plt.ion()
        fig, ax = init_surface(CFG['shape'], CFG['pad'], 10)
        sample_plt = plot_points(ax, sample, **kwargs['sample'])

        if args.rips:
            name = f'{name}_rips'
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
            offset_plt = plot_sfa(ax, sample, levels, kwargs['offset'], name, **kwargs['filt'])
