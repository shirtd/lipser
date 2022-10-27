import matplotlib.pyplot as plt
import numpy.linalg as la
import numpy as np
import os

from lips.util import lmap
from contours.style import COLOR
# plt.ion()

def plot_barcode(ax, dgm, cuts, lw=5, thresh=0, *args, **kwargs):
    dgm = np.array([p for p in dgm if p[1]-p[0] > thresh and p[1] != np.inf])
    if not len(dgm):
        return None
    for i, (birth, death) in enumerate(dgm):
        for name, v in cuts.items():
            a, b, c = v['min'], v['max'], v['color']
            if a < birth and death <= b:
                ax.plot([birth, death], [i, i], c=c, lw=lw)
            elif birth < a and death > a and death <= b:
                ax.plot([a, death], [i, i], c=c, lw=lw)
            elif birth > a and birth < b and death > b:
                ax.plot([birth, b], [i, i], c=c, lw=lw)
            elif birth <= a and b < death:
                ax.plot([b, a], [i, i], c=c, lw=lw)
            # if death == np.inf:
            #       ax.plot([lim, lim+0.1], [i, i], c='black', linestyle='dotted')
    ax.get_yaxis().set_visible(False)
    plt.tight_layout()
    return ax

def get_color(f, cuts, colors, default=COLOR['black']):
    for (a,b), c in zip(zip(cuts[:-1],cuts[1:]), colors):
        if a <= f < b:
            return c
    return default

def init_surface(ax, xlim=(-3,3), ylim=(-2,2)):
    ax.axis('off')
    ax.axis('scaled')
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    plt.tight_layout()

def plot_surface(ax, surf, cuts, colors, alpha=0.5, zorder=0, xlim=(-3,3), ylim=(-2,2), init=False):
    res = {'surface' : ax.contourf(*surf.grid, surf.surface, levels=cuts, colors=colors, alpha=alpha, zorder=0),
            'contours' : ax.contour(*surf.grid, surf.surface, levels=cuts, colors=colors, zorder=0)}
    if init:
        init_surface(ax, xlim, ylim)
    return res

def plot_rainier(ax, surf, cuts, colors, alpha=0.5, zorder=0):
    res = {'surface' : ax.contourf(*surf.grid, surf.surface, levels=cuts, colors=colors, alpha=alpha, zorder=0),
            'contours' : ax.contour(*surf.grid, surf.surface, levels=cuts, colors=colors, zorder=0)}
    ax.axis('off')
    ax.axis('scaled')
    plt.tight_layout()
    return res

def plot_points(ax, points, visible=True, **kwargs):
    p = ax.scatter(points[:,0], points[:,1], **kwargs)
    p.set_visible(visible)
    return p

def plot_balls(ax, P, F, alpha=0.2, **kwargs):
    balls = []
    for p,f in zip(P, F):
        s = plt.Circle(p, f, alpha=alpha, **kwargs)
        balls.append(s)
        ax.add_patch(s)
    return balls

def plot_poly(ax, P, T, visible=True, **kwargs):
    tp = {t : plt.Polygon(P[t,:], **kwargs) for t in T}
    lmap(lambda t: ax.add_patch(t), tp.values())
    if not visible:
        for t,p in tp.items():
            p.set_visible(False)
    return tp

def plot_edges(ax, P, E, visible=True, **kwargs):
    ep = {e : ax.plot(P[e,0], P[e,1], **kwargs)[0] for e in E}
    if not visible:
        for e,p in ep.items():
            p.set_visible(False)
    return ep

def plot_rips(ax, complex, color=COLOR['red'], edge_color=COLOR['black'], visible=True, dim=2, zorder=1, alpha=0.7, fade=[1, 0.6, 0.3], s=9):
    return {0 : plot_points(ax, complex.P, visible, color='black', s=s, zorder=zorder+2, alpha=alpha*fade[0]),
            1 : plot_edges(ax, complex.P, complex(1), visible, color=edge_color, alpha=alpha*fade[1], zorder=zorder+1, lw=1),
            2 : plot_poly(ax, complex.P, complex(2), visible, color=color, alpha=alpha*fade[2], zorder=zorder)}

def plot_rips_filtration(ax, rips, levels, keys, name, dir='figures', save=True, wait=0.5, dpi=300, hide={}):
    rips_plt = {k : plot_rips(ax, rips, **v) for k,v in keys.items()}
    if save and not os.path.exists(dir):
        os.makedirs(dir)
    for i, t in enumerate(levels):
        for d in (1,2):
            for s in rips(d):
                for k,v in rips_plt.items():
                    if not hide[k]:
                        if s.data[k] <= t:
                            rips_plt[k][d][s].set_visible(not keys[k]['visible'])
        plt.pause(wait)
        if save:
            fname = os.path.join(dir, f'{name}{i}.png')
            print(f'saving {fname}')
            plt.savefig(fname, dpi=dpi, transparent=True)
    return rips_plt

def plot_offset_filtration(ax, sample, constant, levels, keys, name, dir='figures', save=True, wait=0.5, dpi=300, hide={}):
    if 'min' in hide and hide['min'] and 'min' in keys:
        keys['min']['visible'] = False

    offset_plt = {  'max' : plot_balls(ax, sample, 2 * sample.function/constant, **keys['max']),
                    'min' : plot_balls(ax, sample, 2 * sample.function/constant, **keys['min'])}
    if save and not os.path.exists(dir):
        os.makedirs(dir)
    for i, t in enumerate(levels):
        for j,f in enumerate(sample.function):
            fs = {'max' : (t - f) / constant, 'min' : (f - t) / constant}
            for k,v in offset_plt.items():
                if not hide[k]:
                    v[j].set_radius(fs[k] if fs[k] > 0 else 0)
        plt.pause(wait)
        if save:
            fname = os.path.join(dir, f'{name}{i}.png')
            print(f'saving {fname}')
            plt.savefig(fname, dpi=dpi, transparent=True)
    return offset_plt


# max_plot = plot_rips(ax, P[:,:2], K, THRESH, COLOR['blue'], False, zorder=2)
# min_plot = plot_rips(ax, P[:,:2], K2, args.mult*THRESH, COLOR['red'], not args.comp, zorder=1)
#
#
#
# if args.save and not os.path.exists(args.dir):
#     os.makedirs(args.dir)
#
# Fmin, Fmax = F.min(), F.max()
# levels = [Fmin-Fmax/2] + CUTS + [1.3*Fmax]
# for i, t in enumerate(levels):
#     # if args.no_max:
#     for s in K[2]:
#         if Tmax[s] <= t:
#             max_plot[2][s].set_visible(True)
#     for s in K[1]:
#         if Emax[s] <= t:
#             max_plot[1][s].set_visible(True)
#     # if args.no_min:
#     if args.comp:
#         for s in K2[2]:
#             if Tmin[s] <= t:
#                 min_plot[2][s].set_visible(True)
#         for s in K2[1]:
#             if Emin[s] <= t:
#                 min_plot[1][s].set_visible(True)
#     else:
#         for s in K2[2]:
#             if Tmin[s] <= t:
#                 min_plot[2][s].set_visible(False)
#         for s in K2[1]:
#             if Emin[s] <= t:
#                 min_plot[1][s].set_visible(False)
#     plt.pause(args.wait)
#     if args.save:
#         cmult_s = ('cx' + np.format_float_scientific(args.cmult, trim='-')) if int(args.cmult) != args.mult else ''
#         plt.savefig(os.path.join(args.dir, '%s_lips_tri%s%d%s.png' % (label, '_comp' if args.comp else '',i,cmult_s)), dpi=args.dpi)
