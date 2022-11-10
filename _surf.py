import numpy as np
import argparse
import os, sys

from contours import CONFIG, COLOR
from contours.surface import *
from contours.plot import *

from lips.topology.util import sfa_dio
from lips.geometry.util import lipschitz_grid

# FILE=os.path.join('data', 'surf32.csv')
FILE=os.path.join('data', 'rainier_sub16.csv')
SAMPLE_FILE= None # 'data/surf32-sample-1233_1.25e-01.csv'
# SUB_FILE='data/surf32-sample-1233_1.25e-01-subsample_140.csv'
# SUB_FILE='data/surf32-sample-1233_1.25e-01-subsample_266.csv'
# SUB_FILE='data/surf32-sample-1233_1.3e-01-subsample_336.csv'
SUB_FILE= None # 'data/surf32-sample-1233_1.3e-01-subsample_401.csv'

parser = argparse.ArgumentParser(prog='lips')

parser.add_argument('--file', default=FILE, help='surface file')
parser.add_argument('--sample-file', default=SAMPLE_FILE, help='sample file')
parser.add_argument('--sub-file', default=SUB_FILE, help='subsample file')
parser.add_argument('--data-dir', default='data', help='data directory')
parser.add_argument('--nosurf', action='store_true', help='hide surf')
parser.add_argument('--show', action='store_true', help='show plot')
parser.add_argument('--save', action='store_true', help='save plot')
parser.add_argument('--thresh', type=float, default=None, help='cover radius')
parser.add_argument('--dpi', type=int, default=300, help='image dpi')
parser.add_argument('--tag', default='', help='file tag')
parser.add_argument('--dir', default='figures', help='figure output directory')
parser.add_argument('--sample', action='store_true', help='sample surface')
parser.add_argument('--sub', action='store_true', help='subsample surface')
parser.add_argument('--color', action='store_true', help='color plot')
parser.add_argument('--cover', action='store_true', help='plot cover')
parser.add_argument('--union', action='store_true', help='plot union of cover')
parser.add_argument('--contours', action='store_true', help='plot contours')
parser.add_argument('--barcode', action='store_true', help='plot barcode')


if __name__ == '__main__':
    args = parser.parse_args()


    CFG = CONFIG[os.path.splitext(os.path.basename(args.file))[0]]
    COLORS = [COLOR[c] for c in CFG['colors']]
    kwargs = {  'surf'      : { 'zorder' : 0, 'alpha' : 0.5},
                'sample'    : { 'zorder' : 10, 'edgecolors' : 'black', 's' : 5, 'color' : 'black'},
                'cover'    : { 'visible' : True, 'zorder' : 2,
                                'color' : COLOR['red1'] if args.union else COLOR['red'],
                                'alpha' : 1 if args.union else 0.2},
                'barcode'   : { 'cuts' : CFG['cuts'], 'colors' : COLORS}}

    grid = make_grid(CFG['res'], CFG['shape'])
    surf = ScalarFieldData(args.file, grid, CFG['lips'])
    args.dir = os.path.join(args.dir, surf.name, 'surf')

    # print(lipschitz_grid(surf.surface, surf.grid[0], surf.grid[1]))
    # print(CFG['lips'])

    if args.save and not os.path.exists(args.dir):
        print(f'creating directory {args.dir}')
        os.makedirs(args.dir)

    if args.barcode:
        fig, ax = plt.subplots(1, 1, sharex=True, figsize=(6,3))
        ax.set_yticks([])
        plt.tight_layout()
        surf_dgms = sfa_dio(surf.surface)

        plot_barcode(ax, surf_dgms[1], **kwargs['barcode'], lw=CFG['lw'])

        if args.save:
            fpath = os.path.join(args.dir, f'{surf.name}_barcode.png')
            print(f'saving {fpath}')
            plt.savefig(fpath, dpi=args.dpi, transparent=True)
        if args.show:
            plt.show()
    else:
        fig, ax = init_surface(CFG['shape'], CFG['pad'], 10)
        if args.contours:
            surf_plt = surf.plot_contours(ax, CFG['cuts'], COLORS, args.save, args.dir, args.dpi)
        elif not args.nosurf:
            surf_plt = surf.plot(ax, CFG['cuts'], COLORS, **kwargs['surf'])

        if args.sample_file is not None:
            sample =  SampleData(args.sample_file, args.thresh)
            if args.thresh is None:
                args.thresh = sample.radius
            sample_plt = sample.plot(ax, **kwargs['sample'])
            if args.cover or args.union:
                if args.color:
                    del kwargs['cover']['color']
                    colors = [COLOR[c] for c in CFG['colors']]
                    kwargs['cover']['colors'] = [get_color(f, CFG['cuts'], colors) for f in sample.function]
                    kwargs['cover']['zorders'] = [get_cut(f, CFG['cuts'], kwargs['cover']['zorder']+1) for f in sample.function]
                    del kwargs['cover']['zorder']
                cover_plt = sample.plot_cover(ax, **kwargs['cover'])

        if args.sub or args.sample:
            _P = np.vstack([sample.points.T, sample.function]).T if args.sample_file is not None else None
            if args.sub:
                P = get_subsample(fig, ax, surf.get_data(), args.thresh, _P, args.sub_file)
                fname = os.path.join(args.data_dir, f'{sample.name}-subsample_{len(P)}.csv')
                if input('save %s (y/*)? ' % fname) in {'y','Y','yes'}:
                    print('saving %s' % fname)
                    np.savetxt(fname, P, fmt='%d')
            else:
                P = get_sample(fig, ax, surf.get_data(), args.thresh, _P)
                name = '%s-sample' % surf.name
                thresh_s = np.format_float_scientific(args.thresh, trim='-')
                fname = os.path.join(args.data_dir, '%s-%d_%s.csv' % (name, len(P), thresh_s))
                if input('save %s (y/*)? ' % fname) in {'y','Y','yes'}:
                    print('saving %s' % fname)
                    np.savetxt(fname, P)
        elif args.show:
            plt.show()

        if args.save:
            sample_str = ''
            if args.sample_file is not None:
                cover_str = '-cover' if args.cover else '-union' if args.union else ''
                color_str = '-color' if args.color else ''
                surf_str = '-nosurf' if args.nosurf else ''
                sample_str = f'_{sample.name}{cover_str}{color_str}{surf_str}'
            fname = os.path.join(args.dir, f'{surf.name}{sample_str}.png')
            print(f'saving {fname}')
            plt.savefig(fname, dpi=args.dpi, transparent=True)
