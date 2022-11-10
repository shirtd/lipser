import numpy as np
import argparse
import os, sys, json

from contours import CONFIG, COLOR
from contours.surface import *
from contours.plot import *

from lips.topology.util import sfa_dio
from lips.geometry.util import lipschitz_grid


FILE=os.path.join('data', 'rainier_sub' 'rainier_sub.csv')
JSON=None # os.path.join('data', 'rainier_sub' 'rainier_sub.json')
SAMPLE_FILE= None
SUB_FILE= None

parser = argparse.ArgumentParser(prog='lips')

parser.add_argument('file', default=FILE, help='surface file')
parser.add_argument('json', default=JSON, help='json file')
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

    surf = USGSScalarFieldData(args.file, args.json)

    plt.ion()
    # fig, ax = init_surface(surf.surface.shape, extents=surf.extents)
    # surf_plt = surf.plot(ax, surf.surface, surf.cuts, surf.colors, alpha=0.5)

    fig, ax = get_fig((surf.surface.shape[1] / surf.surface.shape[0], 1), 10)
    ax.axis('scaled')
    ax.set_xlim(*surf.extents[0])
    ax.set_ylim(*surf.extents[1])
    ax.invert_yaxis()
    ax.axis('off')
    plt.tight_layout()
    surf_plt = plot_surface(ax, surf, surf.cuts, surf.colors, zorder=0, alpha=0.5)


    # if args.json is None:
    #     args.json = f'{os.path.splitext(args.file)[0]}.json'
    #
    # surface = np.loadtxt(args.file)
    # with open(args.json, 'r') as f:
    #     data = json.load(f)
    #
    # grid = np.meshgrid( np.linspace(*data['extents'][0], data['shape'][0]),
    #                     np.linspace(*data['extents'][1], data['shape'][1]))
    #
    # surf = ScalarField(surface, grid, data['lips'])
    #
    # plt.ion()
    # fig, ax = init_surface(data['shape'], extents=data['extents'])
    # surf_plt = plot_surface(ax, surf, data['cuts'], data['colors'], zorder=0, alpha=0.5)
