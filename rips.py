import matplotlib.pyplot as plt
import numpy as np

from contours.surface import make_grid, ScalarFieldFile
from contours.plot import plot_surface
from contours.style import COLOR

RES = 32
SHAPE = (2,1)
PATH = 'data/surf32.csv'
#
# CUTS = [0.05, 0.3, 0.55, 0.8, 1.31]
# COLOR_ORDER = ['green', 'blue', 'purple', 'yellow']
CUTS = [0.2, 0.4, 0.6, 0.875, 1.09, 1.31]
COLOR_ORDER = ['blue','green','yellow','salmon','purple']
COLORS = [COLOR[k] for k in COLOR_ORDER]

if __name__ == '__main__':
    surf = ScalarFieldFile(PATH, make_grid(RES, SHAPE))

    # plt.ion()
    fig, ax = plt.subplots(figsize=(10,8))
    plot_surface(ax, surf, CUTS, COLORS)
    plt.show()

    sample = np.loadtxt(fname)
    P, F = sample[:,:2], sample[:,2]
    points = ax.scatter(P[:,0], P[:,1], c='black', zorder=5, s=10)

    K = rips(P, THRESH)
