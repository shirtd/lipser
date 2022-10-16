import matplotlib.pyplot as plt
import numpy as np
import os


def plot_cell(axis, D, s, color, ord):
    if s.dim == 0:
        return [axis.scatter(D.P[s,0], D.P[s,1], s=1, c=color, zorder=ord)]
    elif s.dim == 1:
        return axis.plot(D.P[s,0], D.P[s,1], c=color, zorder=ord-1, alpha=0.7, lw=0.5)
    elif s.dim == 2:
        return [axis.add_patch(plt.Polygon(D.P[s], color=color, alpha=0.4, zorder=ord-2, ec=None))]

def plot_voronoi(axis, V, s, color, ord):
    if s.dim == 0:
        return [] # [axis.scatter(V.P[s,0], V.P[s,1], s=1, c=color, zorder=ord)]
    elif s.dim == 1 and len(s) > 1:
        return [] # axis.plot(V.P[s,0], V.P[s,1], c=color, zorder=ord-1, alpha=0.7, lw=0.5)
    elif s.dim == 2:
        return [axis.add_patch(plt.Polygon(V.P[V.orient_face(s)], color=color, alpha=0.4, zorder=ord-2, ec=None))]
    return []

def plot_field(axis, f, bounds, thresh=None, cmap='gray', **kw):
    if thresh is not None:
        f = np.ma.masked_where(f > thresh, f)
    try:
        return axis.imshow(f.mask * f, cmap, origin='lower', extent=bounds.flatten(), **kw)
    except TypeError as err:
        print(f)
        print(f.mask)
        print(thresh)
        return f

# def plot_breaks(all_axes, K, field, breaks, bounds, save=False, figdir='figures', label='alpha'):
#     axes = all_axes[2]
#     for axis in axes:
#         axis.axis('off')
#         axis.set_xlim(*bounds[0])
#         axis.set_ylim(*bounds[1])
#     plt.tight_layout()
#     if save:
#         if not os.path.exists(figdir):
#             os.mkdir(figdir)
#     for i, alpha in enumerate(breaks):
#         for axes
#         elems = [plot_field(axes[2], field, bounds, alpha, alpha=0.5, zorder=0)]
#         for s in K:
#             for axis, key, color, ord in [(axes[0], 'maxext', 'purple', 6), (axes[1], 'minext','green', 5)]:
#                 if s(key) <= alpha:
#                     elems += plot_cell(axis, K.P, s, color, ord)
#         plt.pause(0.1)
#         if save:
#             fname = os.path.join(figdir, '%s%de-2.png' % (label, int(alpha*100)))
#             print('saving %s' % fname)
#             plt.savefig(fname, dpi=300, transparent=True)
#         else:
#             input('%s: %0.2f' % (label, alpha))
#         for e in elems:
#             e.remove()
