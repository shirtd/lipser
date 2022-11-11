import matplotlib.pyplot as plt
import numpy as np
import os, json

from contours import COLOR
from lips.util import lmap
from lips.util.math import mk_gauss
from lips.util.array import down_sample
from lips.geometry.util import lipschitz, lipschitz_grid

def make_grid(resolution=32, shape=(2,1)):
    return np.meshgrid( np.linspace(-shape[0], shape[0], int(resolution*shape[0])),
                        np.linspace(-shape[1], shape[1], int(resolution*shape[1])))

def _get_extents(cols, rows, step, x0, y0):
    x1 = x0 + cols*step
    y1 = y0 + rows*step
    xd = measure(x0, y0, x1, y0)
    yd = measure(x0, y0, x0, y1)
    return [[0, xd], [0, yd]]

def measure(lon1, lat1, lon2, lat2):
    R = 6378.137
    dLat = lat2 * np.pi / 180 - lat1 * np.pi / 180
    dLon = lon2 * np.pi / 180 - lon1 * np.pi / 180;
    a = (np.sin(dLat/2) * np.sin(dLat/2) + np.cos(lat1 * np.pi / 180)
        * np.cos(lat2 * np.pi / 180) * np.sin(dLon/2) * np.sin(dLon/2))
    return 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a)) * R * 1000

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
    def plot(self, ax, cuts, colors, zorder=0, alpha=0.5, contour_color=None, invert=False):
        if invert:
            contour_kw = {'colors' : [colors[0]]+ colors} if contour_color is None else {'color' : contour_color}
        else:
            contour_kw = {'colors' : colors + [colors[-1]]}
            if contour_color is not None:
                contour_kw = {'color' : contour_color}
        return {'surface' : ax.contourf(*self.grid, self.surface, levels=cuts, colors=colors, zorder=zorder, alpha=alpha),
                'contours' : ax.contour(*self.grid, self.surface, levels=cuts, zorder=zorder, **contour_kw)}
    def plot_contours(self, ax, cuts, colors, save=False, dir='figures', dpi=300):
        surf_plt = self.plot(ax, cuts, colors, zorder=0, alpha=None)
        surf_alpha = [0 for _ in colors]
        cont_alpha = [1] + surf_alpha
        surf_plt['surface'].set_alpha(surf_alpha)
        surf_plt['contours'].set_alpha(cont_alpha)
        for i, t in enumerate(cuts[:-1]):
            if save:
                fname = os.path.join(dir, f'{self.name}_{int(t*100)}.png')
                print(f'saving {fname}')
                plt.savefig(fname, dpi=dpi, transparent=True)
            else:
                plt.pause(0.5)
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
    def plot_cover(self, ax, alpha=0.2, color=None, colors=None, zorder=None, zorders=None, **kwargs):
        colors = [color for _ in self] if colors is None else colors
        zorders = [zorder for _ in F] if zorders is None else zorders
        balls = []
        for p,c,z in zip(self.points, colors, zorders):
            s = plt.Circle(p, self.radius / 2, alpha=alpha, facecolor=c, edgecolor='none', zorder=z, **kwargs)
            balls.append(s)
            ax.add_patch(s)
        return balls

class SubsampleData(Sample, DataFile):
    def __init__(self, file_name, subsample_file, radius=None):
        DataFile.__init__(self, file_name)
        data = self.load()
        idx = list(np.loadtxt(subsample_file, dtype=int))
        Sample.__init__(self, data[idx,:2], data[idx,2])
        self.radius = float(self.name.split('_')[-1]) if radius is None else radius

class GaussianSurface(Surface):
    def __init__(self, resolution, shape, *args, **kwargs):
        grid = make_grid(resolution, shape)
        surface = mk_gauss(grid[0], grid[1], *args, **kwargs)
        Surface.__init__(self, surface, grid)

class ScalarField(Surface):
    def __init__(self, surface, grid, lips=None):
        self.function = surface.flatten()
        Surface.__init__(self, surface, grid)
        self.lips = lips
    def __call__(self, x):
        return self.function[x]
    def __getitem__(self, i):
        return self.grid_points[i]



class USGSScalarField(ScalarField):
    def __init__(self, surface, extents, lips=None):
        surface, self.extents = surface, extents
        grid = self.get_grid(extents, surface.shape)
        ScalarField.__init__(self, surface, grid, lips)
    def get_grid(self, extents, shape):
        return np.meshgrid( np.linspace(*extents[0], shape[1]),
                            np.linspace(*extents[1], shape[0]))
                            # indexing='ij')

class USGSScalarFieldData(USGSScalarField):
    def __init__(self, fname, jname=None):
        surface = np.loadtxt(fname)
        if jname is None:
            jname = f'{os.path.splitext(fname)[0]}.json'
        with open(jname, 'r') as f:
            data = json.load(f)
        USGSScalarField.__init__(self, surface, data['extents'], data['lips'])
        self.cuts, self.colors, self.pad = data['cuts'], data['colors'], data['pad']


class USGSScalarFieldRaw(USGSScalarField):
    def __init__(self, file, dir=None, name=None, downsample=None, lips=None):
        self.dir = os.path.dirname(file) if dir is None else dir
        surface, self.name = self.get_surface(file, name, downsample)
        extents = self.get_extents(file)
        USGSScalarField.__init__(self, surface, extents, lips)
    def get_extents(self, file):
        with open(file, 'r') as f:
            cols, rows = (int(f.readline().split()[1]), int(f.readline().split()[1]))
            xl, yl = (float(f.readline().split()[1]), float(f.readline().split()[1]))
            step = float(f.readline().split()[1])
        return _get_extents(cols, rows, step, xl, yl)
                    # lon1, lat1, lon2, lat2
        # xd = measure(xl, yl, xl+cols*step, yl)
        # yd = measure(xl, yl, xl, yl+rows*step)
        # return [[0, xd], [0, yd]]
        # return [[-xd/2, xd/2], [-yd/2, yd/2]]
        # return [[xl, xl + cols * step], [yl, yl + rows * step]]
    def get_surface(self, file, name, downsample):
        name = os.path.basename(os.path.splitext(file)[0]) if name is None else name
        surface = np.loadtxt(file, skiprows=6)
        if downsample is not None:
            surface = down_sample(surface, downsample)
            name += str(downsample)
        return surface, name
    def save(self, config=None):
        # config = {} if config is None else config
        if config is not None:
            config['shape'] = self.surface.shape
            config['extents'] = self.extents
            if self.lips is None:
                self.lips = lipschitz_grid(self.surface, self.grid[0], self.grid[1])
            config['lips'] = self.lips
            hname = os.path.join(self.dir, f'{self.name}.json')
            # out = {'cuts' : cuts, 'pad' : pad, 'lips' : lips,
            #         'colors' : [COLOR[c] for c in colors],
            #         'shape' : self.surface.shape,
            #         'extents' : self.extents}
            print(f'saving {hname}')
            with open(hname, 'w') as f:
                json.dump(config, f, indent=2)
        fname = os.path.join(self.dir, f'{self.name}.csv')
        print(f'saving {fname}')
        np.savetxt(fname, self.surface)

class ScalarFieldData(ScalarField, DataFile):
    def __init__(self, file_name, grid=None, constant=None, dir='./'):
        DataFile.__init__(self, file_name, dir)
        ScalarField.__init__(self, self.load(), grid, constant)
