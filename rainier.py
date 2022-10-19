import matplotlib.pyplot as plt
import numpy as np

from lips.topology import RipsComplex
from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.plot import plot_rainier, plot_points, plot_rips
from contours.style import COLOR

RES = 337
SHAPE = (1,1)
SURF_PATH = 'data/rainier_sub16.csv'
# SAMP_PATH = 'data/surf-sample_329_2e-1.csv'
# MULT = 1.2

MIN = 265.258441
MAX = 4379.845434

# CUTS = MAX * np.array([0.0, 0.15, 0.28, 0.38, 0.48, 1.0]) + MIN
CUTS = [200, 1000, 1400, 1800, 2200, np.inf]
COLOR_ORDER = ['blue','green','yellow','salmon','purple']
COLORS = [COLOR[k] for k in COLOR_ORDER]

plt.ion()
fig, ax = plt.subplots(figsize=(9,9))

if __name__ == '__main__':
    surf = ScalarFieldData(SURF_PATH, make_grid(RES, SHAPE))

    surf_plt = plot_rainier(ax, surf, CUTS, COLORS, alpha=0.5, zorder=0)
