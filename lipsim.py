import matplotlib.pyplot as plt
import numpy.linalg as la
import numpy as np

from itertools import combinations
from lips.topology import RipsComplex, Filtration, Diagram
from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.plot import plot_surface, plot_points, plot_rips, get_color, init_surface, plot_barcode
from contours.config import CONFIG
from contours.style import COLOR
import os, sys
from scipy.spatial import KDTree

import dionysus as dio

import argparse

parser = argparse.ArgumentParser(prog='sample')

parser.add_argument('--dir', default=os.path.join('figures'), help='dir')
parser.add_argument('--surf', default='data/surf32.csv', help='surface file')
parser.add_argument('--file', default='data/surf-sample_1067_1.2e-1.csv', help='sample file')
parser.add_argument('--sub', default='data/surf-sample_329_2e-1.csv', help='subsample file')
parser.add_argument('--dpi', type=int, default=300, help='dpi')
parser.add_argument('--save', action='store_true', help='save')
parser.add_argument('--mult', type=float, default=1.1, help='thresh mult')
parser.add_argument('--cmult', type=float, default=1., help='c mult')
parser.add_argument('--tag', default=None, help='tag directory and file')


# plt.ion()

fig, ax = plt.subplots(2,1,sharex=True, sharey=True,figsize=(6,4))
ax[0].invert_yaxis()
plt.tight_layout()



if __name__ == '__main__':
    args = parser.parse_args()

    args.tag = "" if args.tag is None else f"_{args.tag}"
    # args.dir = f"{args.dir}{args.tag}"

    CFG = CONFIG['rainier' if 'rainier' in  args.surf else 'surf']
    RES, SHAPE, LIPS = CFG['res'], CFG['shape'], CFG['lips']
    CUTS, COLOR_ORDER, LABELS = CFG['cuts'], CFG['colors'], CFG['labels']

    COLORS = [COLOR[k] for k in COLOR_ORDER]
    CUT_ARGS = {l : {'min' : a, 'max' : b, 'color' : c} for l,(a,b),c in zip(LABELS, zip(CUTS[:-1], CUTS[1:]), COLORS)}

    surf = ScalarFieldData(args.surf, make_grid(RES, SHAPE), args.cmult*LIPS)

    sample, subsample = SampleData(args.file), SampleData(args.sub)
    # subsample_colors = [get_color(f, CUTS, COLORS) for f in subsample.function]

    rips = RipsComplex(sample.points, 2*sample.radius*args.mult)

    for p, s in zip(sample, rips(0)):
        if s.data['dist'] <= sample.radius*args.mult:
            s.data['max'] = min(f + surf.constant*la.norm(p - s) for s,f in zip(subsample, subsample.function))
        else:
            s.data['max'] = np.inf
        s.data['min'] = max(f - surf.constant*la.norm(p - s) for s,f in zip(subsample, subsample.function))

    for s in rips(1)+rips(2):
        s.data['max'] = max(rips(0)[v].data['max'] for v in s) if s.data['dist'] <= sample.radius*args.mult else np.inf
        s.data['min'] = max(rips(0)[v].data['min'] for v in s)

    min_filt = Filtration(rips, 'min')
    max_filt = Filtration(rips, 'max')
    hom =  Diagram(rips, min_filt, pivot=max_filt, verbose=True)
    dgm,_ = hom.get_diagram(rips, min_filt, max_filt)


    plot_barcode(ax[0], dgm[1], CUT_ARGS)

    filt = dio.fill_freudenthal(surf.surface)
    hom = dio.homology_persistence(filt)
    dgms = dio.init_diagrams(hom, filt)
    np_dgms = [np.array([[p.birth, p.death if p.death < np.inf else -0.1] for p in d]) if len(d) else np.ndarray((0,2)) for d in dgms]

    plot_barcode(ax[1], np_dgms[1], CUT_ARGS)

    ax[1].set_xticks([])
    ax[1].set_ylim(5,-1)

    if args.save and not os.path.exists(args.dir):
        os.makedirs(args.dir)

    if args.save:
        mult_s = np.format_float_scientific(args.mult, trim='-') if int(args.mult) != args.mult else str(int(args.mult))
        cmult_s = ('cx' + np.format_float_scientific(args.cmult, trim='-')) if int(args.cmult) != args.mult else ''
        fname = f'barcode_{sample.name}_subsample_lips{args.tag}{mult_s}{cmult_s}.png'
        fpath = os.path.join(args.dir, fname)
        print(f'saving {fpath}')
        plt.savefig(fpath, dpi=args.dpi, transparent=True)
        plt.show()
