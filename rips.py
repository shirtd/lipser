import matplotlib.pyplot as plt
import numpy as np

from lips.topology import RipsComplex
from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.plot import plot_surface, plot_points, plot_rips
from contours.style import COLOR

RES = 32
SHAPE = (2,1)
SURF_PATH = 'data/surf32.csv'
SAMP_PATH = 'data/surf-sample_329_2e-1.csv'
MULT = 1.2

# CUTS = [0.05, 0.3, 0.55, 0.8, 1.31]
# COLOR_ORDER = ['green', 'blue', 'purple', 'yellow']
CUTS = [0.05, 0.2, 0.45, 0.875, 1.09, 1.31]
COLOR_ORDER = ['blue','green','yellow','salmon','purple']
COLORS = [COLOR[k] for k in COLOR_ORDER]

if __name__ == '__main__':
    surf = ScalarFieldData(SURF_PATH, make_grid(RES, SHAPE))
    sample = SampleData(SAMP_PATH)
    rips = RipsComplex(sample.points, sample.radius*MULT)
    for s in rips:
        s.data['f'] = sample(s).max()

    plt.ion()
    fig, ax = plt.subplots(figsize=(10,8))
    surf_plt = plot_surface(ax, surf, CUTS, COLORS)
    rips_plt = plot_rips(ax, rips, zorder=1, color=COLOR['red'], alpha=1/MULT)
    plt.show()
