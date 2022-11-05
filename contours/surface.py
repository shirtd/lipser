import matplotlib.pyplot as plt
import numpy as np
import os

from lips.util import lmap
from lips.util.math import mk_gauss
from lips.geometry.util import lipschitz

def make_grid(resolution=32, shape=(2,1)):
    return np.meshgrid( np.linspace(-shape[0], shape[0], resolution*shape[0]),
                        np.linspace(-shape[1], shape[1], resolution*shape[1]))

class DataFile:
    def __init__(self, file_name, dir='./'):
        self.path = os.path.join(dir, file_name)
        self.file = os.path.basename(file_name)
        self.folder = os.path.dirname(file_name)
        self.name, self.extension = os.path.splitext(self.file)
    def load(self):
        return np.loadtxt(self.path)

class Surface:
    def __init__(self, surface, grid):
        self.surface, self.grid = surface, grid
        self.grid_points = np.vstack(lmap(lambda x: x.flatten(), self.grid)).T
    def get_data(self):
        return np.vstack([self.grid_points.T, self.surface.flatten()]).T
    def plot(self, ax, cuts, colors, zorder=0, alpha=0.5, contour_color=None):
        contour_kw = {'colors' : [colors[0]]+ colors} if contour_color is None else {'color' : contour_color}
        return {'surface' : ax.contourf(*self.grid, self.surface, levels=cuts, colors=colors, zorder=zorder, alpha=alpha),
                'contours' : ax.contour(*self.grid, self.surface, levels=cuts, zorder=zorder, **contour_kw)}
    def plot_contours(self, ax, cuts, colors, save=False, dir='figures', dpi=300):
        surf_plt = self.plot(ax, cuts, colors, zorder=0, alpha=None)
        surf_alpha = [0 for _ in colors]
        cont_alpha = [1] + surf_alpha
        surf_plt['surface'].set_alpha(surf_alpha)
        surf_plt['contours'].set_alpha(cont_alpha)
        for i, t in enumerate(cuts[:-1]):
            plt.pause(0.5)
            if save:
                fname = os.path.join(dir, f'{self.name}_{int(t*100)}.png')
                print(f'saving {fname}')
                plt.savefig(fname, dpi=dpi, transparent=True)
            surf_alpha[i], cont_alpha[i+1] =  0.5, 1
            surf_plt['surface'].set_alpha(surf_alpha)
            surf_plt['contours'].set_alpha(cont_alpha)
        return surf_plt

class Sample:
    def __init__(self, points, function):
        self.points = points
        self.function = function
    def get_levels(self, cuts, margin=0.5):
        fmin = self.function.min()
        fmax = self.function.max()
        diff = fmax - fmin
        levels = [fmin-diff*margin] + cuts + [fmax+diff*margin]
        return [(a+b)/2 for a,b in zip(levels[:-1],levels[1:])]
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
        p = ax.scatter(self.points[:,0], self.points[:,1], **kwargs)
        p.set_visible(visible)
        return p


class SampleData(Sample, DataFile):
    def __init__(self, file_name, radius=None):
        DataFile.__init__(self, file_name)
        data = self.load()
        Sample.__init__(self, data[:,:2], data[:,2])
        self.radius = float(self.name.split('_')[-1]) if radius is None else radius
    def plot_cover(self, ax, alpha=0.2, color=None, colors=None, **kwargs):
        colors = [color for _ in self] if colors is None else colors
        balls = []
        for p,c in zip(self.points, colors):
            s = plt.Circle(p, self.radius / 2, alpha=alpha, facecolor=c, edgecolor='none', **kwargs)
            balls.append(s)
            ax.add_patch(s)
        return balls

class GaussianSurface(Surface):
    def __init__(self, resolution, shape, *args, **kwargs):
        grid = make_grid(resolution, shape)
        surface = mk_gauss(grid[0], grid[1], *args, **kwargs)
        Surface.__init__(self, surface, grid)

class ScalarField(Surface):
    def __init__(self, surface, grid, constant=None):
        self.function = surface.flatten()
        Surface.__init__(self, surface, grid)
        self.constant = constant
    def __call__(self, x):
        return self.function[x]
    def __getitem__(self, i):
        return self.grid_points[i]

class ScalarFieldData(ScalarField, DataFile):
    def __init__(self, file_name, grid=None, constant=None, dir='./'):
        DataFile.__init__(self, file_name, dir)
        ScalarField.__init__(self, self.load(), grid, constant)
