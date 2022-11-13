import matplotlib.pyplot as plt
import numpy as np
import os

from contours.data import Data, DataFile
from contours.plot import get_sample, init_surface
from lips.util import mk_gauss, down_sample, lmap, format_float
from lips.geometry.util import lipschitz_grid, coords_to_meters, greedysample


class Surface:
    def __init__(self, surface, grid, cuts, colors, pad=0):
        self.cuts, self.colors, self.pad = cuts, colors, pad
        self.surface, self.grid, self.shape = surface, grid, surface.shape
        self.grid_points = np.vstack(lmap(lambda x: x.flatten(), grid)).T
    def get_data(self):
        return np.vstack([self.grid_points.T, self.surface.flatten()]).T
    def init_plot(self):
        return init_surface(self.shape, self.extents, self.pad)
    def plot(self, ax, zorder=0, **kwargs):
        return {'surface' : ax.contourf(*self.grid, self.surface, levels=self.cuts, colors=self.colors, zorder=zorder, **kwargs),
                'contours' : ax.contour(*self.grid, self.surface, levels=self.cuts[1:], colors=self.colors[1:], zorder=zorder+1)}
    def plot_contours(self, show=True, save=False, folder='figures', dpi=300, pad=0, off_alpha=0.1):
        fig, ax = self.init_plot()
        surf_plt = self.plot(ax)
        surf_alpha = [off_alpha for _ in self.colors]
        cont_alpha = surf_alpha.copy()
        surf_plt['surface'].set_alpha(surf_alpha)
        surf_plt['contours'].set_alpha(cont_alpha)
        if show: plt.pause(0.5)
        if save: self.save_plot(folder, format_float(self.cuts[0]), dpi)
        for i, t in enumerate(self.cuts[:-1]):
            cont_alpha[i], surf_alpha[i] = 1., 0.5
            surf_plt['contours'].set_alpha(cont_alpha)
            surf_plt['surface'].set_alpha(surf_alpha)
            if show: plt.pause(0.5)
            if save: self.save_plot(folder, format_float(t), dpi)
        plt.close(fig)
    def save_plot(self, name, folder='./', dpi=300, tag=None, sep='_'):
        tag = '' if (tag is None or not len(tag)) else sep+tag
        folder = os.path.join(folder, name)
        if not os.path.exists(folder):
            print(f'creating directory {folder}')
            os.makedirs(folder)
        file_name = os.path.join(folder, f'{name}{tag}.png')
        print(f'saving {file_name}')
        plt.savefig(file_name, dpi=dpi, transparent=True)
    # update to create a sample object, save using sample object method
    # def sample(self, name, folder, thresh, min_cut=-np.inf, greedy=False, sample=None, mult=0.5):
    #     fig, ax = self.init_plot()
    #     if greedy:
    #         Pidx = [i for i,f in enumerate(self.function) if f >= min_cut]
    #         idx = greedysample(self.grid_points[Pidx], thresh*mult/2)
    #         Q = np.vstack([self.grid_points[Pidx][idx].T, self.function[Pidx][idx]]).T
    #     else:
    #         Q = np.vstack([sample.points.T, sample.function]).T if sample is not None else None
    #     P = get_sample(fig, ax, self.get_data(), thresh, Q)
    #     folder = os.path.join(folder, 'samples')
    #     file_name = os.path.join(folder, f'{name}-sample{len(P)}_{format_float(thresh)}.csv')
    #     if input('save %s (y/*)? ' % file_name) in {'y','Y','yes'}:
    #         if not os.path.exists(fdir):
    #             print(f'creating directory {fdir}')
    #             os.makedirs(fdir)
    #         print('saving %s' % fname)
    #         np.savetxt(fname, P)

class GaussianSurface(Surface):
    def __init__(self, resolution, shape, cuts, colors, pad=0, **kwargs):
        grid = np.meshgrid( np.linspace(-shape[0], shape[0], int(resolution*shape[0])),
                            np.linspace(-shape[1], shape[1], int(resolution*shape[1])))
        surface = mk_gauss(grid[0], grid[1], **kwargs)
        Surface.__init__(self, surface, grid, cuts, colors, pad)

class ScalarField(Surface):
    def __init__(self, surface, extents, cuts, colors, pad=0, lips=None):
        self.extents, self.lips = extents, lips
        self.function = surface.flatten()
        grid = self.get_grid(extents, surface.shape)
        Surface.__init__(self, surface, grid, cuts, colors, pad)
    def __call__(self, i):
        return self.function[i]
    def __getitem__(self, i):
        return self.grid_points[i]
    def get_grid(self, extents, shape):
        return np.stack(np.meshgrid(np.linspace(*extents[0], shape[1]),
                                    np.linspace(*extents[1], shape[0])))

class USGSScalarField(ScalarField, Data):
    def __init__(self, file_name, cuts, colors, pad=0, lips=None, downsample=None):
        folder = os.path.dirname(file_name)
        extents = self.get_extents(file_name)
        surface, name = self.get_surface(file_name, downsample)
        config = {'extents' : extents, 'cuts' : cuts, 'colors' : colors, 'pad' : pad, 'lips' : lips}
        ScalarField.__init__(self, surface, **config)
        Data.__init__(self, name, folder, config)
    def get_extents(self, file):
        with open(file, 'r') as f:
            cols, rows = (int(f.readline().split()[1]), int(f.readline().split()[1]))
            x0, y0 = (float(f.readline().split()[1]), float(f.readline().split()[1]))
            step = float(f.readline().split()[1])
        x1, y1 = x0 + cols*step, y0 + rows*step
        xd = coords_to_meters(x0, y0, x1, y0)
        yd = coords_to_meters(x0, y0, x0, y1)
        return np.array([[0, xd], [0, yd]])
    def get_surface(self, file, downsample):
        name = os.path.basename(os.path.splitext(file)[0])
        print(f'loading {file}')
        surface = np.loadtxt(file, skiprows=6)
        if downsample is not None:
            surface = down_sample(surface, downsample)
            name += str(downsample)
        return surface, name
    def save(self, config=None):
        if self.lips is None:
            self.config['lips'] = lipschitz_grid(self.surface, self.grid)
        Data.save(self, self.surface.tolist())

class ScalarFieldData(ScalarField, DataFile):
    def __init__(self, file_name, json_file=None):
        if json_file is None:
            json_file = f'{os.path.splitext(file_name)[0]}.json'
        DataFile.__init__(self, file_name, json_file)
        ScalarField.__init__(self, self.load_data(), **self.config)
    # TODO
    # def plot_barcode(self, ax, *args, **kwargs):
    #     return ScalarField.plot_barcode(self, ax, self.cuts, self.colors, *args, **kwargs)
