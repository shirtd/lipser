import matplotlib.pyplot as plt
import numpy.linalg as la
import numpy as np

from lips.util import lmap
from contours.style import COLOR
# plt.ion()


def plot_surface(ax, surf, cuts, colors, alpha=0.5, zorder=0):
    res = {'surface' : ax.contourf(*surf.grid, surf.surface, levels=cuts, colors=colors, alpha=alpha, zorder=0),
            'contours' : ax.contour(*surf.grid, surf.surface, levels=cuts, colors=colors, zorder=0)}
    ax.axis('off')
    ax.axis('scaled')
    ax.set_ylim(-4,4)
    ax.set_xlim(-5,5)
    plt.tight_layout()
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

def plot_balls(ax, P, F, **kwargs):
    balls = []
    for p,f in zip(P, F):
        s = plt.Circle(p, f, **kwargs)
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

def plot_rips(ax, complex, color=COLOR['red'], edge_color=COLOR['black'], visible=True, dim=2, zorder=1, alpha=0.7, fade=[1, 0.15, 0.05], s=9):
    return {0 : plot_points(ax, complex.P, visible, color='black', s=s, zorder=zorder+2, alpha=alpha*fade[0]),
            1 : plot_edges(ax, complex.P, complex(1), visible, color=edge_color, alpha=alpha*fade[1], zorder=zorder+1, lw=1),
            2 : plot_poly(ax, complex.P, complex(2), visible, color=color, alpha=alpha*fade[2], zorder=zorder)}



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
