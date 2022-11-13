import matplotlib.pyplot as plt
import numpy as np
import os, json

from contours import COLOR
from contours.data import DataFile
from lips.util import lmap, format_float
from contours.plot import get_sample, init_surface
from lips.geometry.util import lipschitz_grid, coords_to_meters, greedysample


class Sample:
    def __init__(self, points, function):
        self.points = points
        self.function = function
    def get_levels(self, cuts, margin=200):
        _cuts = [int(a+(b-a)/2) for a,b in zip([cuts[0]-margin]+cuts, cuts+[cuts[-1]+margin])]
        return [x for t in zip(_cuts, cuts) for x in t]
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
    def __init__(self, points, function, radius):
        Sample.__init__(self, points, function)
        self.radius = radius
    def plot_cover(self, ax, alpha=0.2, color=None, colors=None, zorder=None, zorders=None, **kwargs):
        colors = [color for _ in self] if colors is None else colors
        zorders = [zorder for _ in self] if zorders is None else zorders
        balls = []
        for p,c,z in zip(self.points, colors, zorders):
            s = plt.Circle(p, self.radius / 2, alpha=alpha, facecolor=c, edgecolor='none', zorder=z, **kwargs)
            balls.append(s)
            ax.add_patch(s)
        return balls

class MetricSampleData(MetricSample, DataFile):
    def __init__(self, file_name, json_file=None, radius=None):
        DataFile.__init__(self, file_name)
        data = self.load()
        radius = float(self.name.split('_')[-1]) if radius is None else radius
        MetricSample.__init__(self, data[:,:2], data[:,2], radius)
    def get_tag(self, args):
        return  f"{self.name}"\
                f"{'-cover' if args.cover else '-union' if args.union else ''}"\
                f"{'-color' if args.color else ''}"\
                f"{'-surf' if args.surf else ''}"
