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

class SampleData(Sample, DataFile):
    def __init__(self, file_name, radius=None):
        DataFile.__init__(self, file_name)
        data = self.load()
        Sample.__init__(self, data[:,:2], data[:,2])
        self.radius = float(self.name.split('_')[-1]) if radius is None else radius


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
