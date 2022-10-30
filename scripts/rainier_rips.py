import matplotlib.pyplot as plt
import numpy as np

from lips.topology import RipsComplex
from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.plot import plot_rainier, plot_points, plot_rips, plot_surface
from contours.style import COLOR

RES = 337
SHAPE = (1,1)
SURF_PATH = 'data/rainier_sub16.csv'
SAMP_PATH = 'data/rainier_sub16-sample_1094_1e-1.csv'
MULT = 1

CUTS = [200, 1000, 1400, 1800, 2200, np.inf]
COLOR_ORDER = ['blue','green','yellow','salmon','purple']
COLORS = [COLOR[k] for k in COLOR_ORDER]

plt.ion()
fig, ax = plt.subplots(figsize=(9,9))

if __name__ == '__main__':
    surf = ScalarFieldData(SURF_PATH, make_grid(RES, SHAPE))

    # surf_plt = plot_rainier(ax, surf, CUTS, COLORS, alpha=0.5, zorder=0)

    sample = SampleData(SAMP_PATH)
    rips = RipsComplex(sample.points, sample.radius*MULT)

    for s in rips:
        s.data['f'] = sample(s).max()

    rips_plt = plot_rips(ax, rips, zorder=1, color=COLOR['red'])
    plt.show()
