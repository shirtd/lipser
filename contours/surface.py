import matplotlib.pyplot as plt
import numpy as np
import os, json

from contours import COLOR
from lips.util import lmap, format_float
from lips.util.math import mk_gauss
from contours.plot import get_sample, init_surface
from lips.util.array import down_sample
from lips.geometry.util import lipschitz_grid, coords_to_meters


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
        self.surface, self.grid, self.shape = surface, grid, surface.shape
        self.grid_points = np.vstack(lmap(lambda x: x.flatten(), self.grid)).T
    def get_data(self):
        return np.vstack([self.grid_points.T, self.surface.flatten()]).T
    def plot(self, ax, cuts, colors, zorder=0, alpha=0.5):
        return {'surface' : ax.contourf(*self.grid, self.surface, levels=cuts, colors=colors, zorder=zorder, alpha=alpha),
                'contours' : ax.contour(*self.grid, self.surface, levels=cuts[1:], colors=colors[1:], zorder=zorder+1)}
    def plot_contours(self, ax, cuts, colors, show=True, save=False, dir='figures', dpi=300, off_alpha=0.1):
        surf_plt ={'surface' : ax.contourf(*self.grid, self.surface, levels=cuts, colors=colors, zorder=0),
                    'contours' : ax.contour(*self.grid, self.surface, levels=cuts[1:], colors=colors[1:], zorder=1)}
        surf_alpha = [off_alpha for _ in colors]
        cont_alpha = surf_alpha.copy()
        surf_plt['surface'].set_alpha(surf_alpha)
        surf_plt['contours'].set_alpha(cont_alpha)
        for i, t in enumerate(cuts[:-1]):
            if save:
                self.save_plot(dir, format_float(t), dpi)
            if show:
                plt.pause(0.5)
            cont_alpha[i] = 1.
            surf_plt['contours'].set_alpha(cont_alpha)
            surf_alpha[i] = 0.5
            surf_plt['surface'].set_alpha(surf_alpha)
        if save:
            self.save_plot(dir, format_float(cuts[-1]), dpi)
        if show:
            plt.pause(0.5)
        return surf_plt
    def save_plot(self, dir='./', tag=None, dpi=300, sep='_'):
        tag = '' if (tag is None or not len(tag)) else sep+tag
        dir = os.path.join(dir, self.name)
        if not os.path.exists(dir):
            print(f'creating directory {dir}')
            os.makedirs(dir)
        fpath = os.path.join(dir, f'{self.name}{tag}.png')
        print(f'saving {fpath}')
        plt.savefig(fpath, dpi=dpi, transparent=True)
    def sample(self, fig, ax, thresh, sample=None):
        Q = np.vstack([sample.points.T, sample.function]).T if sample is not None else None
        P = get_sample(fig, ax, self.get_data(), thresh, Q)
        fdir = os.path.join(self.folder, 'samples')
        fname = os.path.join(fdir, f'{self.name}-{len(P)}_{format_float(thresh)}.csv')
        if input('save %s (y/*)? ' % fname) in {'y','Y','yes'}:
            if not os.path.exists(fdir):
                print(f'creating directory {fdir}')
                os.makedirs(fdir)
            print('saving %s' % fname)
            np.savetxt(fname, P)

class GaussianSurface(Surface):
    def __init__(self, resolution, shape, *args, **kwargs):
        grid = np.meshgrid( np.linspace(-shape[0], shape[0], int(resolution*shape[0])),
                            np.linspace(-shape[1], shape[1], int(resolution*shape[1])))
        surface = mk_gauss(grid[0], grid[1], *args, **kwargs)
        Surface.__init__(self, surface, grid)

class ScalarField(Surface):
    def __init__(self, surface, extents, lips=None):
        self.extents, self.lips = extents, lips
        self.function = surface.flatten()
        grid = self.get_grid(extents, surface.shape)
        Surface.__init__(self, surface, grid)
    def __call__(self, x):
        return self.function[x]
    def __getitem__(self, i):
        return self.grid_points[i]
    def get_grid(self, extents, shape):
        return np.stack(np.meshgrid(np.linspace(*extents[0], shape[1]),
                                    np.linspace(*extents[1], shape[0])))

class USGSScalarField(ScalarField):
    def __init__(self, file_name, dir=None, name=None, downsample=None, lips=None):
        self.dir = os.path.dirname(file_name) if dir is None else dir
        surface, self.name = self.get_surface(file_name, name, downsample)
        extents = self.get_extents(file_name)
        ScalarField.__init__(self, surface, extents, lips)
    def get_extents(self, file):
        with open(file, 'r') as f:
            cols, rows = (int(f.readline().split()[1]), int(f.readline().split()[1]))
            x0, y0 = (float(f.readline().split()[1]), float(f.readline().split()[1]))
            step = float(f.readline().split()[1])
        x1, y1 = x0 + cols*step, y0 + rows*step
        xd = coords_to_meters(x0, y0, x1, y0)
        yd = coords_to_meters(x0, y0, x0, y1)
        return np.array([[0, xd], [0, yd]])
    def get_surface(self, file, name, downsample):
        name = os.path.basename(os.path.splitext(file)[0]) if name is None else name
        surface = np.loadtxt(file, skiprows=6)
        if downsample is not None:
            surface = down_sample(surface, downsample)
            name += str(downsample)
        return surface, name
    def save(self, config=None):
        if config is not None:
            config['shape'] = self.surface.shape
            config['extents'] = self.extents.tolist()
            if self.lips is None:
                self.lips = lipschitz_grid(self.surface, self.grid)
            config['lips'] = self.lips
            hname = os.path.join(self.dir, f'{self.name}.json')
            print(f'saving {hname}')
            with open(hname, 'w') as f:
                json.dump(config, f, indent=2)
        fname = os.path.join(self.dir, f'{self.name}.csv')
        print(f'saving {fname}')
        np.savetxt(fname, self.surface)

class ScalarFieldData(ScalarField, DataFile):
    def __init__(self, file_name, json_file=None, dir='./'):
        DataFile.__init__(self, file_name, dir)
        surface, config = self.load(), self.load_json(json_file)
        ScalarField.__init__(self, surface, config['extents'], config['lips'])
        self.cuts, self.colors, self.pad = config['cuts'], config['colors'], config['pad']
    def load_json(self, json_file):
        if json_file is None:
            json_file = f'{os.path.join(self.folder, self.name)}.json'
        with open(json_file, 'r') as f:
            config = json.load(f)
        return config
    def plot(self, ax, *args, **kwargs):
        return ScalarField.plot(self, ax, self.cuts, self.colors, *args, **kwargs)
    def plot_contours(self, show=True, save=False, dir='./', dpi=300):
        fig, ax = init_surface(self.shape, self.extents, self.pad)
        ScalarField.plot_contours(self, ax, self.cuts, self.colors, show, save, dir, dpi)
        plt.close(fig)
    # TODO
    # def plot_barcode(self, ax, *args, **kwargs):
    #     return ScalarField.plot_barcode(self, ax, self.cuts, self.colors, *args, **kwargs)

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
    # def subsample(self, fig, ax, thresh, sample=None, subsample=None):
    #     surf.get_data(), args.thresh, _P, args.sub_file)
    #     Q = np.vstack([sample.points.T, sample.function]).T if sample is not None else None
    #     P = get_subsample(fig, ax, self.get_data(), thresh, Q)
    #     ax, S, thresh, P, sub_file=None, color=COLOR['pink1']):
    #     fdir = os.path.join(self.folder, 'samples')
    #     fname = os.path.join(fdir, f'{self.name}-{len(P)}_{format_float(thresh)}.csv')
    #     if input('save %s (y/*)? ' % fname) in {'y','Y','yes'}:
    #         if not os.path.exists(fdir):
    #             print(f'creating directory {fdir}')
    #             os.makedirs(fdir)
    #         print('saving %s' % fname)
    #         np.savetxt(fname, P)
    #     # P = get_subsample(fig, ax, surf.get_data(), args.thresh, _P, args.sub_file)
    #     # fname = os.path.join(args.data_dir, f'{sample.name}-subsample_{len(P)}.csv')
    #     # if input('save %s (y/*)? ' % fname) in {'y','Y','yes'}:
    #     #     print('saving %s' % fname)
    #     #     np.savetxt(fname, P, fmt='%d')

class SampleData(Sample, DataFile):
    def __init__(self, file_name, radius=None):
        DataFile.__init__(self, file_name)
        data = self.load()
        Sample.__init__(self, data[:,:2], data[:,2])
        self.radius = float(self.name.split('_')[-1]) if radius is None else radius
    def plot_cover(self, ax, alpha=0.2, color=None, colors=None, zorder=None, zorders=None, **kwargs):
        colors = [color for _ in self] if colors is None else colors
        zorders = [zorder for _ in self] if zorders is None else zorders
        balls = []
        for p,c,z in zip(self.points, colors, zorders):
            s = plt.Circle(p, self.radius / 2, alpha=alpha, facecolor=c, edgecolor='none', zorder=z, **kwargs)
            balls.append(s)
            ax.add_patch(s)
        return balls
    def get_tag(self, args):
        return f"""{self.name if self is None else ''}
                {'-cover' if args.cover else '-union' if args.union else ''}
                {'-color' if args.color else ''}
                {'-nosurf' if args.nosurf else ''}"""

# class SubsampleData(Sample, DataFile):
#     def __init__(self, file_name, subsample_file, radius=None):
#         DataFile.__init__(self, file_name)
#         data = self.load()
#         idx = list(np.loadtxt(subsample_file, dtype=int))
#         Sample.__init__(self, data[idx,:2], data[idx,2])
#         self.radius = float(self.name.split('_')[-1]) if radius is None else radius
