import matplotlib.pyplot as plt
import numpy as np
import os, json

from contours.config import COLOR
from contours.data import Data, DataFile
from lips.util import lmap, format_float
from contours.plot import get_sample, init_surface, plot_rips
from lips.geometry.util import lipschitz_grid, coords_to_meters, greedysample

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
    def __init__(self, points, function, cuts, colors, pad=0):
        self.points, self.function = points, function
        self.cuts, self.colors, self.pad = cuts, colors, pad
        self.function = function
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


class MetricSample(Sample):
    def __init__(self, points, function, radius, cuts, colors, pad=0):
        Sample.__init__(self, points, function, cuts, colors, pad)
        self.radius = radius
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

class MetricSampleData(MetricSample, DataFile):
    def __init__(self, file_name, json_file, radius=None):
        DataFile.__init__(self, file_name, json_file)
        data, radius = self.load_data(), float(self.name.split('_')[-1]) if radius is None else radius
        cuts, colors, pad = self.config['cuts'], self.config['colors'], self.config['pad']
        MetricSample.__init__(self, data[:,:2], data[:,2], radius, cuts, colors, pad)
    # def get_surface_path(self):
    #     surf_name = os.path.basename(file_name).split('-sample')[0]
    #     surf_dir = os.path.split(os.path.dirname(file_name))
    #     returnos.path.join(surf_dir, f'{surf_name}.csv')
    def get_tag(self, args):
        return  f"{self.name}"\
                f"{'-cover' if args.cover else '-union' if args.union else ''}"\
                f"{'-color' if args.color else ''}"\
                f"{'-surf' if args.surf else ''}"
