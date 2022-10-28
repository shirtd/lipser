import numpy as np
import argparse
import os,sys

from contours.surface import make_grid, ScalarFieldData, SampleData
from lips.topology import RipsComplex
from contours.config import CONFIG
from contours.style import COLOR
from contours.plot import *





parser = argparse.ArgumentParser(prog='sample')

parser.add_argument('--dir', default=os.path.join('figures','sfa'), help='dir')
parser.add_argument('--file', default='data/surf-sample_329_2e-1.csv', help='sample file')
parser.add_argument('--surf', default='data/surf32.csv', help='surf file')
parser.add_argument('--dpi', type=int, default=300, help='dpi')
parser.add_argument('--save', action='store_true', help='save')
parser.add_argument('--mult', type=float, default=1.15, help='thresh mult')
parser.add_argument('--wait', type=float, default=0.5, help='wait')
parser.add_argument('--tag', default=None, help='tag directory and file')

plt.ion()
fig, ax = plt.subplots(figsize=(10,8))

if __name__ == '__main__':
    args = parser.parse_args()

    args.tag = "" if args.tag is None else f"_{args.tag}"
    args.dir = f"{args.dir}{args.tag}"

    kwargs = {'dir' : args.dir, 'save' : args.save, 'wait' : args.wait, 'dpi' : args.dpi}
    keys = {'facecolor' : COLOR['pink1'], 'edgecolor' : 'none', 'zorder' : 2}
    keys = {'facecolor' : COLOR['pink1'], 'edgecolor' : 'none', 'zorder' : 2}
    CFG = CONFIG['rainier' if 'rainier' in  args.file else 'surf']

    fig, ax = plt.subplots(figsize=(10*CFG['shape'][0],10*CFG['shape'][1]))
    xl, yl = CFG['shape'][0]*CFG['pad'][0], CFG['shape'][1]*CFG['pad'][1]
    COLORS = [COLOR[k] for k in CFG['colors']]
    init_surface(ax, (-xl,xl), (-yl,yl))

    sample = SampleData(args.file)
    # rips = RipsComplex(sample.points, 1.75*sample.radius)
    rips = RipsComplex(sample.points, sample.radius*args.mult)
    rips.sublevels(sample)

    levels = sample.get_levels(CFG['cuts'])
    name = f'{sample.name}_sfa-offset{args.tag}'

    # edge_colors = [get_color(sample(t).max(), CFG['cuts'], COLORS) for t in rips(1)]
    # tri_colors = [get_color(sample(t).max(), CFG['cuts'], COLORS) for t in rips(2)]
    # rips_plt = plot_rips(ax, rips, edge_color=COLOR['black'], visible=True, dim=2, zorder=1, alpha=1., fade=[1, 0.7, 0.4], s=9, tri_colors=tri_colors)
    # rips_plt = plot_rips(ax, rips, edge_color=COLOR['black'], visible=True, dim=2, zorder=1, alpha=1., fade=[1, 0.5, 0.3], s=9, tri_colors=tri_colors)


    # if args.surf is not None:
    #     grid = make_grid(CFG['res'], CFG['shape'])
    #     surf = ScalarFieldData(args.surf, grid, CFG['lips'])
    #     surf_plt = plot_surface(ax, surf, CFG['cuts'], COLORS, alpha=0.5)
    #     # offset_plt = plot_balls(ax, sample.points, 1.2*np.ones(len(sample.points)) * sample.radius / 2, color=COLOR['red'], alpha=0.2, zorder=1)
    grid = make_grid(CFG['res'], CFG['shape'])
    surf = ScalarFieldData(args.surf, grid, CFG['lips'])
    surf_plt = {'surface' : ax.contourf(*surf.grid, surf.surface, levels=CFG['cuts'], colors=COLORS, zorder=0),
                'contours' : ax.contour(*surf.grid, surf.surface, linewidths=[3,3,3,3,3], levels=CFG['cuts'], zorder=0, colors=[COLORS[0]] + COLORS)}
    # surf_plt = {'surface' : ax.contourf(*surf.grid, surf.surface, levels=CFG['cuts'], colors=[COLOR['gray'] for _ in COLORS], zorder=0),
    #             'contours' : ax.contour(*surf.grid, surf.surface, linewidths=[3,3,3,3,3], levels=CFG['cuts'], zorder=0, colors=['black' for _ in COLORS])}
    surf_plt['contours'].set_alpha([0,1,0,0,0])
    surf_plt['surface'].set_alpha([0.5,0,0,0])

    # # sample_plt = plot_points(ax, sample, zorder=4, c='black', s=9)
    # idx = [i for i,f in enumerate(sample.function) if f <= CFG['cuts'][1]]
    # sample_plt = ax.scatter(sample.points[idx,0], sample.points[idx,1], zorder=4, c='black', s=9)


    # l = surf_plt['contours'].allsegs[0][0]
    # # l = np.vstack([l[-50:], l, l[:20]])
    # ax.plot(l[:,0], l[:,1], lw=100, alpha=0.3, color='black', solid_capstyle='round')

    # boundary_plt = ax.contourf(*surf.grid, surf.surface, levels levels=CFG['cuts'], zorder=0, colors=['black' for _ in COLORS])}

    # sample_plt = plot_points(ax, sample, zorder=4, c='black', s=9)
    # offset_plt = plot_sfa(ax, sample, levels, keys, name, **kwargs)
    # rips = RipsComplex(sample.points, 1.75*sample.radius)
    # rips_plt = plot_rips(ax, rips, color=COLOR['red'], edge_color=COLOR['black'], visible=True, dim=2, zorder=1, alpha=0.7, fade=[1, 0.5, 0.], s=9)
    # offset_plt = plot_balls(ax, sample.points, np.ones(len(sample.points)) * sample.radius / 2, color=COLOR['red'], alpha=0.2, zorder=1)
