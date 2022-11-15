from scipy.spatial import KDTree
import matplotlib.pyplot as plt
import numpy as np
import os, json

from contours.config import COLOR
from contours.data import Data, DataFile
from lips.util import lmap, format_float
from contours.plot import get_sample, init_surface, plot_rips, plot_points, plot_balls
from lips.geometry.util import lipschitz_grid, coords_to_meters, greedysample

# def sample_surface(thresh, greedy=False, sample_file=None, mult=0.5):
#     Q = None
#     fig, ax = self.init_plot()
#     surf_plt = self.plot(ax, alpha=0.5)
#     if greedy:
#
#     elif sample_file is not None:
#         sample = SampleData(sample_file, thresh)
#         thresh = sample.radius if thresh is None else thresh
#         Q = np.vstack([sample.points.T, sample.function]).T
#     P = get_sample(fig, ax, self.get_data(), thresh, Q)
#     if P is not None:
#         folder = os.path.join(self.folder, 'samples')
#         file_name = os.path.join(self.folder, f'{self.name}-sample{len(P)}_{format_float(thresh)}.csv')
#         if input('save %s (y/*)? ' % file_name) in {'y','Y','yes'}:
#             if not os.path.exists(folder):
#                 print(f'creating directory {folder}')
#                 os.makedirs(folder)
#             print('saving %s' % file_name)
#             np.savetxt(file_name, P)
#     plt.close(fig)
#     return P

def sample_surface(surf, data, thresh, points=None):
    fig, ax = surf.init_plot()
    if points is None:
        points = []
    else:
        plot_points(ax, points, color='black', zorder=4, s=5)
        plot_balls(ax, points, np.ones(len(points))*thresh/2, alpha=1., color='gray', zorder=2)
        points = list(points)
    tree = KDTree(data[:,:2])
    def onclick(e):
        p = data[tree.query(np.array([e.xdata, e.ydata]))[1]]
        ax.add_patch(plt.Circle(p, thresh/2, color=COLOR['red1'], zorder=3, alpha=1))
        ax.scatter(p[0], p[1], c='black', zorder=4, s=5)
        plt.pause(0.01)
        points.append(p)
    cid = fig.canvas.mpl_connect('button_press_event', onclick)
    plt.show()
    fig.canvas.mpl_disconnect(cid)
    plt.close(fig)
    if len(points):
        return np.vstack(sorted(points, key=lambda x: x[2]))
    return None

# TODO
# # TODO
# # class _Sample:
# #     def __init__(self, points, function):
# #         self.points, self.function = points, function
# #     def __len__(self):
# #         return len(self.function)
# #     def __iter__(self):
# #         yield from self.points
# #     def __getitem__(self, i):
# #         return self.points[i]
# #     def __call__(self, i):
# #         return self.function[i]
#
#
class Sample:
    def __init__(self, points, function, cuts, colors, pad, parent):
        self.points, self.function = points, function
        self.cuts, self.colors, self.pad = cuts, colors, pad
        self.parent = parent
    def get_data(self):
        return np.vstack([self.points.T, self.function]).T
    def get_levels(self, margin=200):
        it = zip([self.cuts[0]-margin]+self.cuts, self.cuts+[self.cuts[-1]+margin])
        _cuts = [int(a+(b-a)/2) for a,b in it]
        return [x for t in zip(_cuts, self.cuts) for x in t]
    def __getitem__(self, i):
        return self.points[i]
    def __call__(self, i):
        return self.function[i]
    def __iter__(self):
        for p in self.points:
            yield p
    def __len__(self):
        return len(self.points)
    def plot(self, ax, visible=True, **kwargs):
        p = ax.scatter(self[:,0], self[:,1], **kwargs)
        p.set_visible(visible)
        return p

# class SurfaceSample(MetricSample):
#     def __init__(self, X, thresh, sample=None):
#         if sample is None:
#             points = []
#         else:
#             plot_points(ax, points, color='black', zorder=3, s=5)
#             plot_balls(ax, points, np.ones(len(P))*thresh/2, alpha=1., color='gray', zorder=2)
#             points = list(sample)
#         T = KDTree(X[:,:2])
#
#
#     def get_sample(fig, ax, S, thresh, P=None, color=COLOR['pink1']):
#         if P is not None:
#             plot_points(ax, P, color='black', zorder=3, s=5)
#             plot_balls(ax, P, np.ones(len(P))*thresh/2, alpha=1., color='gray', zorder=2)
#             P = list(P)
#         else:
#             P = []
#         def onclick(event):
#             p = S[T.query(np.array([event.xdata,event.ydata]))[1]]
#             ax.add_patch(plt.Circle(p, thresh/2, color=color, zorder=3, alpha=1))
#             ax.scatter(p[0], p[1], c='black', zorder=4, s=5)
#             plt.pause(0.1)
#             P.append(p)
#         cid = fig.canvas.mpl_connect('button_press_event', onclick)
#         plt.show()
#         fig.canvas.mpl_disconnect(cid)
#         P = sorted(P, key=lambda x: x[1])
#         return np.vstack(P) if len(P) else None
#     def __init__(self, surface, thresh, greedy=False, sample_file=None, mult=0.5):
#         if greedy:
#             S = surface.get_data()[surface.function > surface.cuts[0]]
#             Q = S[greedysample(S[:,:2], thresh*mult/2)]
#
#     def get_greedy_sample(self, surface, thresh, mult=0.5):
#
#
#     def get_sample(self, thresh, gree)




class MetricSample(Sample):
    def __init__(self, points, function, radius, extents, cuts, colors, pad=0, lips=1., parent='test'):
        Sample.__init__(self, points, function, cuts, colors, pad, parent)
        self.extents, self.radius = extents, radius
    def get_cut(self, f):
        for i, (a,b) in enumerate(zip(self.cuts[:-1], self.cuts[1:])):
            if a <= f < b:
                return i
        return 0
    def plot_cover(self, ax, plot_colors=False, color=COLOR['red'], zorder=0, **kwargs):
        balls = []
        kwargs['edgecolor'] = 'none'
        for p,f in zip(self.points, self.function):
            cut = self.get_cut(f)
            c = self.colors[cut] if plot_colors else color
            s = plt.Circle(p, self.radius / 2, facecolor=c, zorder=zorder+cut, **kwargs)
            balls.append(s)
            ax.add_patch(s)
        return balls
    def plot_rips(self, ax, rips, plot_colors=False, color=COLOR['red'], **kwargs):
        if plot_colors:
            kwargs['tri_colors'] = [self.colors[self.get_cut(self(t).max())] for t in rips(2)]
        else:
            kwargs['color'] = color
        return plot_rips(ax, rips, **kwargs)
    def plot_rips_filtration(self, rips, show=True, save=True, folder='figures', dpi=300, tag=None, **kwargs):
        rips_plt = plot_rips(ax, rips, visible=False, **kwargs)
        for i, t in enumerate(self.get_levels()):
            for d in (1,2):
                for s in rips(d):
                    if s.data[k] <= t:
                        rips_plt[k][d][s].set_visible(not keys[k]['visible'])
            if show: plt.pause(0.5)
            if save: self.save_plot(folder, dpi, f"{tag}_rips{format_float(t)}.png")
        return rips_plt

class SurfaceSampleData(MetricSample, Data):
    def __init__(self, points, function, radius, surface, config=None):
        _config = {'radius' : radius, 'parent' : surface.name}
        config = {**surface.config, **_config, **({} if config is None else config)}
        name = f'{surface.name}-sample{len(function)}_{format_float(radius)}'
        Data.__init__(self, name, os.path.join(surface.folder, 'samples'), config=config)
        MetricSample.__init__(self, points, function, radius, surface.cuts, surface.colors, surface.pad)


class MetricSampleFile(MetricSample, DataFile):
    def __init__(self, file_name, json_file=None, radius=None):
        DataFile.__init__(self, file_name, json_file)
        data, radius = self.load_data(), float(self.name.split('_')[-1]) if radius is None else radius
        # cuts, colors, pad = self.config['cuts'], self.config['colors'], self.config['pad']
        MetricSample.__init__(self, data[:,:2], data[:,2], **self.config)
    # def get_surface_path(self):
    #     surf_name = os.path.basename(file_name).split('-sample')[0]
    #     surf_dir = os.path.split(os.path.dirname(file_name))
    #     returnos.path.join(surf_dir, f'{surf_name}.csv')
    def init_plot(self):
        return init_surface(self.config['extents'], self.pad)
    def get_tag(self, args):
        return  f"sample{len(self)}_{format_float(self.radius)}"\
                f"{'-cover' if args.cover else '-union' if args.union else ''}"\
                f"{'-color' if args.color else ''}"\
                f"{'-surf' if args.surf else ''}"

# class MetricSampleFile(MetricSample, DataFile):
#     def __init__(self, file_name, json_file, radius=None):
#         DataFile.__init__(self, file_name, json_file)
#         data, radius = self.load_data(), float(self.name.split('_')[-1]) if radius is None else radius
#         cuts, colors, pad = self.config['cuts'], self.config['colors'], self.config['pad']
#         MetricSample.__init__(self, data[:,:2], data[:,2], radius, cuts, colors, pad)
#     # def get_surface_path(self):
#     #     surf_name = os.path.basename(file_name).split('-sample')[0]
#     #     surf_dir = os.path.split(os.path.dirname(file_name))
#     #     returnos.path.join(surf_dir, f'{surf_name}.csv')
#     def get_tag(self, args):
#         return  f"{self.name}"\
#                 f"{'-cover' if args.cover else '-union' if args.union else ''}"\
#                 f"{'-color' if args.color else ''}"\
#                 f"{'-surf' if args.surf else ''}"
