import matplotlib.pyplot as plt

import numpy as np

from lips.topology import RipsComplex
from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.plot import plot_surface, plot_points, plot_rips
from contours.style import COLOR

from lips.util import format_float

import os


SCALE = None
WEIGHT = 1
RESOLUTION = 256
CUTS = [0, 0.07, 0.15, 0.2, 0.27, 0.4, 0.6, 0.75]

DPI = 500

# EPSILON = 0.3

# plt.ion()
fig, ax = plt.subplots(figsize=(12,9))


if __name__ == '__main__':

    X = np.vstack(( np.sin(np.linspace(-np.pi, np.pi, RESOLUTION)),
                    np.cos(np.linspace(-np.pi, np.pi, RESOLUTION)))).T


    # ax.plot(X[:,0], X[:,1])


    # TODO union of balls


    for seed in range(10):
        ax.axis('off')
        if SCALE is not None:
            ax.set_xlim(-SCALE, SCALE)
            ax.set_ylim(-SCALE, SCALE)
        else:
            ax.axis('equal')

        SEED = seed
        np.random.seed(seed)

        P = X + (np.random.rand(RESOLUTION,2)-1/2) * WEIGHT
        # ax.scatter(P[:,0], P[:,1], s=5, color='black', alpha=1, zorder=1)

        for EPSILON in CUTS:
            rips = RipsComplex(P, EPSILON)
            rips_plt = plot_rips(ax, rips, alpha=1/(1+EPSILON), zorder=1) # , alpha=1/MULT)

            DIR = "figures"
            dout = os.path.join(DIR, f"circle{SEED}w{int(10*WEIGHT)}")
            if not os.path.exists(dout):
                os.makedirs(dout)

            fout = os.path.join(dout, f"{SEED}-{RESOLUTION}w{int(10*WEIGHT)}d{int(10*EPSILON)}.png")
            print(f"saving {fout}")
            plt.savefig(fout, dpi=DPI)

        ax.cla()
