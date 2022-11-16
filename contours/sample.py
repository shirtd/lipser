from scipy.spatial import KDTree
import matplotlib.pyplot as plt
import numpy as np
import os, json

from contours.config import COLOR, KWARGS
from contours.data import Data, DataFile
from lips.util import lmap, format_float
from lips.topology import RipsComplex, Diagram, Filtration
from contours.plot import get_sample, init_surface, plot_rips, plot_points, plot_balls, init_barcode, plot_barcode
from lips.geometry.util import lipschitz_grid, coords_to_meters, greedysample


class Sample:
    def __init__(self, points, function, cuts, colors, pad, parent):
        self.points, self.function = points, function
        self.cuts, self.colors, self.pad = cuts, colors, pad
        self.parent = parent
    def get_data(self):
        return np.vstack([self.points.T, self.function]).T
    def get_cut(self, f):
        for i, (a,b) in enumerate(zip(self.cuts[:-1], self.cuts[1:])):
            if a <= f < b:
                return i
        return 0
    def get_levels(self):
        cuts = [int(a+(b-a)/2) for a,b in zip(self.cuts[:-1], self.cuts[1:])]
        return [x for t in zip(self.cuts, cuts) for x in t] + [self.cuts[-1]]
    def __getitem__(self, i):
        return self.points[i]
    def __call__(self, i):
        return self.function[i]
    def __iter__(self):
        for p in self.points:
            yield p
    def __len__(self):
        return len(self.points)
    def plot(self, ax, visible=True, plot_color=False, **kwargs):
        if plot_color:
            kwargs['color'] = [self.colors[self.get_cut(f)] for f in self.function]
        p = ax.scatter(self[:,0], self[:,1], **kwargs)
        p.set_visible(visible)
        return p

class MetricSample(Sample):
    def __init__(self, points, function, radius, extents, cuts, colors, pad=0, lips=1., parent='test'):
        Sample.__init__(self, points, function, cuts, colors, pad, parent)
        self.extents, self.radius = extents, radius
    def plot_cover(self, ax, plot_colors=False, color=COLOR['red'], zorder=0, radius=None, **kwargs):
        balls = []
        radius = self.radius if radius is None else radius
        kwargs['edgecolor'] = 'none'
        for p,f in zip(self.points, self.function):
            cut = self.get_cut(f)
            c = self.colors[cut] if plot_colors else color
            s = plt.Circle(p, radius / 2, facecolor=c, zorder=zorder+cut, **kwargs)
            balls.append(s)
            ax.add_patch(s)
        return balls
    def plot_balls(self, ax, radii, plot_colors=False, color=COLOR['red'], zorder=0, **kwargs):
        balls = []
        kwargs['edgecolor'] = 'none'
        for p,f,r in zip(self.points, self.function, radii):
            cut = self.get_cut(f)
            c = self.colors[cut] if plot_colors else color
            s = plt.Circle(p, r / 2, facecolor=c, zorder=zorder+cut, **kwargs)
            balls.append(s)
            ax.add_patch(s)
        return balls
    def plot_rips(self, ax, rips, plot_colors=False, color=COLOR['red'], **kwargs):
        if plot_colors:
            kwargs['tri_colors'] = [self.colors[self.get_cut(self(t).max())] for t in rips(2)]
        else:
            kwargs['color'] = color
        return plot_rips(ax, rips, **kwargs)

class SurfaceSampleData(MetricSample, Data):
    def __init__(self, points, function, radius, surface, config=None):
        _config = {'radius' : radius, 'parent' : surface.name}
        config = {**surface.config, **_config, **({} if config is None else config)}
        name = f'{surface.name}-sample{len(function)}_{format_float(radius)}'
        Data.__init__(self, name, os.path.join(surface.folder, 'samples'), config=config)
        MetricSample.__init__(self, points, function, **config)

class MetricSampleFile(MetricSample, DataFile):
    def __init__(self, file_name, json_file=None, radius=None):
        DataFile.__init__(self, file_name, json_file)
        data, radius = self.load_data(), float(self.name.split('_')[-1]) if radius is None else radius
        MetricSample.__init__(self, data[:,:2], data[:,2], **self.config)
    def get_tag(self, args):
        return  f"sample{len(self)}_{format_float(self.radius)}"\
                f"{'-cover' if args.cover else '-union' if args.union else ''}"\
                f"{'-color' if args.color else ''}"\
                f"{'-surf' if args.surf else ''}"
    def init_plot(self):
        return init_surface(self.config['extents'], self.pad)
    def plot_rips_filtration(self, rips, config, tag=None, show=True, save=True, folder='figures', plot_colors=False, dpi=300, subsample=None):
        fig, ax = self.init_plot()
        if subsample is None:
            self.plot(ax, **KWARGS['sample'])
        else:
            self.plot(ax, **KWARGS['supsample'])
            subsample.plot(ax, plot_color=plot_colors, **KWARGS['subsample'])
        rips_plt = {k : self.plot_rips(ax, rips, plot_colors, **v) for k,v in config.items()}
        for i, t in enumerate(self.get_levels()):
            for d in (1,2):
                for s in rips(d):
                    for k,v in rips_plt.items():
                        if s.data[k] <= t:
                            v[d][s].set_visible(not config[k]['visible'])
            if show:
                plt.pause(0.5)
            if save:
                self.save_plot(folder, dpi, f"{tag}{format_float(t)}")
        plt.close(fig)
    def plot_cover_filtration(self, tag=None, show=True, save=True, folder='figures', plot_colors=False, dpi=300, **kwargs):
        fig, ax = self.init_plot()
        self.plot(ax, **KWARGS['sample'])
        offset_plt = self.plot_cover(ax, plot_colors, visible=False, **kwargs)
        for i, t in enumerate(self.get_levels()):
            for j,f in enumerate(self.function):
                if f <= t:
                    offset_plt[j].set_visible(True)
            if show:
                plt.pause(0.5)
            if save:
                self.save_plot(folder, dpi, f"{tag}{format_float(t)}")
        plt.close(fig)
    def plot_lips_filtration(self, config, tag=None, show=True, save=True, folder='figures', plot_colors=False, dpi=300, **kwargs):
        fig, ax = self.init_plot()
        self.plot(ax, **KWARGS['sample'])
        offset_plt = {  'max' : self.plot_balls(ax, 2*self.function/self.config['lips'], plot_colors, **config['max']),
                        'min' : self.plot_balls(ax, 2*self.function/self.config['lips'], plot_colors, **config['min'])}
        for i, t in enumerate(self.get_levels()):
            for j,f in enumerate(self.function):
                fs = {'max' : (t - f) / self.config['lips'], 'min' : (f - t) / self.config['lips']}
                for k,v in offset_plt.items():
                    v[j].set_radius(fs[k] if fs[k] > 0 else 0)
            if show:
                plt.pause(0.5)
            if save:
                self.save_plot(folder, dpi, f"lips-{tag}{format_float(t)}")
        plt.close(fig)
    def plot_barcode(self, folder='./', save=False, show=False, dpi=300, sep='_', relative=False, **kwargs):
        fig, ax = init_barcode()
        rips = RipsComplex(self.points, self.radius * 2 / np.sqrt(3), verbose=True)
        rips.sublevels(self)
        filt = Filtration(rips, 'f')
        pivot = Filtration(rips, 'f', filter=lambda s: s['dist'] <= self.radius)
        hom =  Diagram(rips, filt, pivot=pivot, verbose=True)
        smoothing = None # lambda p: [p[0]+self.config['lips']*self.radius, p[1]-self.config['lips']*self.radius]
        dgms = hom.get_diagram(rips, filt, pivot, smoothing)
        barode_plt = plot_barcode(ax, dgms[1], self.cuts, self.colors, **kwargs)
        tag = f"barcode{'-relative' if relative else ''}"
        if save: self.save_plot(folder, dpi, tag, sep)
        if show: plt.show()
        plt.close(fig)
        return dgms
    def plot_lips_barcode(self, subsample, folder='./', save=False, show=False, dpi=300, sep='_', relative=False, **kwargs):
        fig, ax = init_barcode()
        rips = RipsComplex(self.points, self.radius * 2 / np.sqrt(3), verbose=True)
        rips.lips_sub(subsample, self.config['lips'])
        filt = Filtration(rips, 'min')
        pivot = Filtration(rips, 'max', filter=lambda s: s['dist'] <= self.radius)
        hom =  Diagram(rips, filt, pivot=pivot, verbose=True)
        smoothing = None # lambda p: [p[0]+self.config['lips']*self.radius, p[1]-self.config['lips']*self.radius]
        dgms = hom.get_diagram(rips, filt, pivot, smoothing)
        barode_plt = plot_barcode(ax, dgms[1], self.cuts, self.colors, **kwargs)
        tag = f"barcode-lips{'-relative' if relative else ''}"
        if save: self.save_plot(folder, dpi, tag, sep)
        if show: plt.show()
        plt.close(fig)
        return dgms
