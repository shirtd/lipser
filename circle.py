import numpy as np
import argparse
import os

from lips.topology import Filtration, Diagram, RipsComplex
from contours import CONFIG, COLOR
from contours.surface import *
from contours.plot import *


parser = argparse.ArgumentParser(prog='circle')

parser.add_argument('--scale', type=int, default=CONFIG['circle']['scale'], help='scale')
parser.add_argument('--seed', type=int, default=CONFIG['circle']['seed'], help='seed')
parser.add_argument('--weight', type=int, default=CONFIG['circle']['weight'], help='weight')
parser.add_argument('--res', type=int, default=CONFIG['circle']['res'], help='number of points')
parser.add_argument('--show', action='store_true', help='show plot')
parser.add_argument('--wait', type=float, default=0.5, help='wait time (if --show)')
parser.add_argument('--save', action='store_true', help='save plot')
parser.add_argument('--dpi', type=int, default=300, help='image dpi')
parser.add_argument('--tag', default=None, help='file tag')
parser.add_argument('--dir', default=os.path.join('figures','circle'), help='output directory')
parser.add_argument('--union', action='store_true', help='run offset union')
parser.add_argument('--rips', action='store_true', help='run rips')
parser.add_argument('--graph', action='store_true', help='run graph')
parser.add_argument('--barcode', action='store_true', help='run barcode')
parser.add_argument('--thresh', type=float, default=2., help='max rips radius')


if __name__ == '__main__':
    args = parser.parse_args()

    kwargs = {  'barcode'   :   {   'lw' : 5, 'lim' : args.thresh/2},
                'sample'    :   {   's' : 9, 'color' : 'black', 'zorder' : 5, 'alpha' : 1},
                'rips'      :   {   'alpha' : 1, 'zorder' : 1, 'fade' : [1, 0.3, 0.15]},
                'graph'     :   {   'alpha' : 1, 'zorder' : 1, 'fade' : [1, 0.3, 0.]},
                'offset'    :   {   'alpha' : 1 if args.union else 0.1, 'zorder' : 0,
                                    'color' : COLOR['red1' if args.union else 'red']}}

    if args.show:
        plt.ion()

    np.random.seed(args.seed)

    X = np.vstack(( np.sin(np.linspace(-np.pi, np.pi, args.res)),
                    np.cos(np.linspace(-np.pi, np.pi, args.res)))).T
    P = X + (np.random.rand(args.res, 2) - 1/2) * args.weight

    if args.save:
        w_str = np.format_float_scientific(args.weight, trim='-')
        # dout = os.path.join(args.dir, f"circle{args.seed}-{args.res}w{w_str}")
        if not os.path.exists(args.dir):
            print(f'making directory {args.dir}')
            os.makedirs(args.dir)

    if args.barcode:
        rips = RipsComplex(P, args.thresh)
        filt = Filtration(rips, 'dist')
        dgm = Diagram(rips, filt, verbose=True)

        ax = plot_barcode(dgm.diagram[1], **kwargs['barcode'])
        if args.save:
            fout = os.path.join(args.dir, f"circle{args.seed}-{args.res}w{w_str}_barcode.png")
            print(f"saving {fout}")
            plt.savefig(fout, dpi=args.dpi, transparent=True)
    else:
        name = 'rips' if args.rips else 'graph' if args.graph else 'offset-union' if args.union else 'offset'
        fig, ax = plt.subplots(figsize=(12,9))
        reset_plot(ax, args.scale)

        for t in CONFIG['circle']['cuts']:
            ax.scatter(P[:,0], P[:,1], **kwargs['sample'])
            if args.rips or args.graph:
                rips = RipsComplex(P, t)
                rips_plt = plot_rips(ax, rips, **kwargs['graph' if args.graph else 'rips'])
            else:
                ax.scatter(P[:,0], P[:,1], **kwargs['sample'])
                balls_plt = plot_balls(ax, P, np.ones(len(P)) * t/2, **kwargs['offset'])

            if args.show:
                plt.pause(args.wait)
            if args.save:
                # t_str = np.format_float_scientific(t, trim='-')
                fout = os.path.join(args.dir, f"circle{args.seed}-{args.res}w{w_str}_{name}{int(t*100)}.png")
                print(f"saving {fout}")
                plt.savefig(fout, dpi=args.dpi, transparent=True)

            ax.cla()
            reset_plot(ax, args.scale)
