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
        grid = get_grid(resolution, shape)
        surface = mk_gauss(grid[0], grid[1], *args, **kwargs)
        Surface.__init__(self, surface, grid)

class ScalarField(Surface):
    def __init__(self, surface, grid, constant=None):
        self.function = surface.flatten()
        self.constant = lipschitz(self.function, grid) if constant is None else self.constant
        Surface.__init__(self, surface, self._get_grid(surface, grid, self.constant) if grid is None else grid)
    def __call__(self, x):
        return self.function[x]
    def __getitem__(self, i):
        return self.grid_points[i]

class ScalarFieldData(ScalarField, DataFile):
    def __init__(self, file_name, grid=None, constant=None, dir='./'):
        DataFile.__init__(self, file_name, dir)
        ScalarField.__init__(self, self.load(), grid, constant)



#
# G = mk_gauss(X, Y, GAUSS_ARGS)
# _c = args.cmult*3.1443048369350226 #
#
#
# fname = args.file
# dir = os.path.dirname(fname)
# file = os.path.basename(fname)
# label, ext = os.path.splitext(file)
# lname = label.split('_')
# name, NPTS, THRESH = lname[0], lname[1], float(lname[2])
#
# sample = np.loadtxt(fname)
# P, F = sample[:,:2], sample[:,2]
# points = ax.scatter(P[:,0], P[:,1], c='black', zorder=5, s=10)
#
#
# K = rips(P, THRESH)
# K2 = rips(P, args.mult*THRESH) if args.mult > 1 else K
#
#
# Edist = {e : la.norm(P[e[0]] - P[e[1]]) for e in K2[1]}
# Emax = {e : (F[e[0]]+F[e[1]] + _c * Edist[e]) / 2 for e in K[1]}
# # Emax = {e : max(F[e[0]],F[e[1]]) for e in K[1]}
# Emin = {e : (F[e[0]]+F[e[1]] - _c * Edist[e]) / 2 for e in K2[1]}
# Tmax = {t : max(Emax[e] for e in combinations(t,2)) for t in K[2]}
# Tmin = {t : (max if args.comp else min)(Emin[e] for e in combinations(t,2)) for t in K2[2]}
