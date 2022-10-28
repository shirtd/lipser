import matplotlib.pyplot as plt

import numpy as np

from lips.topology import RipsComplex
from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.plot import plot_surface, plot_points, plot_rips, plot_balls
from contours.style import COLOR
from lips.topology import Filtration, Diagram

from lips.util import format_float

import os


SCALE = 2.8
WEIGHT = 0.5
RESOLUTION = 256
CUTS = [0, 0.07, 0.15, 0.2, 0.27, 0.4, 0.6, 0.75]

DPI = 300

# EPSILON = 0.3

def plot_barcode(dgm, color=COLOR['red'], lw=5, thresh=1e-2, lim=0.3, *args, **kwargs):
    dgm = np.array([p for p in dgm if p[1]-p[0] > thresh])

    if not len(dgm):
        return None
    fig, ax = plt.subplots(1, 1, *args, **kwargs)
    for i, (birth, death) in enumerate(dgm):
        if death == np.inf:
            ax.plot([birth, lim], [i, i], c=color, lw=lw, zorder=1)
            ax.plot([lim, lim*1.1], [i, i], c='black', linestyle='dotted', zorder=0)
        else:
            ax.plot([birth, death], [i, i], c=color, lw=lw)
    ax.get_yaxis().set_visible(False)
    plt.tight_layout()
    return ax

# plt.ion()
fig, ax = plt.subplots(figsize=(12,9))


if __name__ == '__main__':

    X = np.vstack(( np.sin(np.linspace(-np.pi, np.pi, RESOLUTION)),
                    np.cos(np.linspace(-np.pi, np.pi, RESOLUTION)))).T


    # ax.plot(X[:,0], X[:,1])


    # TODO union of balls

    plt.ion()
    SEED = 0
    np.random.seed(SEED)

    P = X + (np.random.rand(RESOLUTION,2)-1/2) * WEIGHT
    # ax.scatter(P[:,0], P[:,1], s=5, color='black', alpha=1, zorder=1)

    # EPSILON = 2
    # rips = RipsComplex(P, EPSILON)
    # filt = Filtration(rips, 'dist')
    # dgm = Diagram(rips, filt, verbose=True)

    ax.axis('off')
    ax.axis('equal')
    if SCALE is not None:
        ax.set_xlim(-SCALE, SCALE)
        ax.set_ylim(-SCALE, SCALE)


    # NAME = 'barcode'
    # ax = plot_barcode(dgm.diagram[1], lw=5,lim=EPSILON/2)
    #
    # DIR = "figures"
    # NAME = "barcode"
    # dout = os.path.join(DIR)
    # if not os.path.exists(dout):
    #     os.makedirs(dout)
    # fout = os.path.join(dout, f"{NAME}{SEED}-{RESOLUTION}w{int(10*WEIGHT)}d{int(100*EPSILON)}.png")
    # print(f"saving {fout}")
    # plt.savefig(fout, dpi=DPI)

    CLR = 'pink1'

    for EPSILON in CUTS:
        # rips = RipsComplex(P, EPSILON)
        # rips_plt = plot_rips(ax, rips, alpha=1/(1+EPSILON), zorder=1, fade=[1,0.15, 0.1]) # , alpha=1/MULT)
        ax.scatter(P[:,0], P[:,1], s=7, color='black', alpha=1, zorder=5)
        # balls_plt = plot_balls(ax, P, np.ones(len(P))*EPSILON/2, facecolor=COLOR['red'], edgecolor='none', zorder=0, alpha=0.1)
        balls_plt = plot_balls(ax, P, np.ones(len(P))*EPSILON/2, facecolor=COLOR[CLR], edgecolor='none', zorder=0, alpha=1)

        DIR = "figures"
        # NAME = 'rips'
        # NAME = "graph"
        NAME = f"offset-{CLR}"
        dout = os.path.join(DIR, f"circle_{NAME}{SEED}w{int(10*WEIGHT)}")
        if not os.path.exists(dout):
            os.makedirs(dout)

        fout = os.path.join(dout, f"{NAME}{SEED}-{RESOLUTION}w{int(10*WEIGHT)}d{int(100*EPSILON)}.png")
        print(f"saving {fout}")
        plt.savefig(fout, dpi=DPI, transparent=True)

        ax.cla()
        ax.axis('off')
        ax.axis('equal')
        if SCALE is not None:
            ax.set_xlim(-SCALE, SCALE)
            ax.set_ylim(-SCALE, SCALE)


    # for seed in range(10):
    #     ax.axis('off')
    #     ax.axis('equal')
    #     if SCALE is not None:
    #         ax.set_xlim(-SCALE, SCALE)
    #         ax.set_ylim(-SCALE, SCALE)
    #
    #     SEED = seed
    #     np.random.seed(seed)
    #
    #     P = X + (np.random.rand(RESOLUTION,2)-1/2) * WEIGHT
    #     # ax.scatter(P[:,0], P[:,1], s=5, color='black', alpha=1, zorder=1)
    #
    #     for EPSILON in CUTS:
    #         # rips = RipsComplex(P, EPSILON)
    #         # rips_plt = plot_rips(ax, rips, alpha=1/(1+EPSILON), zorder=1) # , alpha=1/MULT)
    #         ax.scatter(P[:,0], P[:,1], s=9, color='black', alpha=0.7, zorder=1)
    #         balls_plt = plot_balls(ax, P, np.ones(len(P))*EPSILON/2, color=COLOR['red'], zorder=0, alpha=0.1)
    #
    #         DIR = "figures"
    #         NAME = "balls"
    #         dout = os.path.join(DIR, f"circle_{NAME}{SEED}w{int(10*WEIGHT)}")
    #         if not os.path.exists(dout):
    #             os.makedirs(dout)
    #
    #         fout = os.path.join(dout, f"{NAME}{SEED}-{RESOLUTION}w{int(10*WEIGHT)}d{int(100*EPSILON)}.png")
    #         print(f"saving {fout}")
    #         plt.savefig(fout, dpi=DPI)
    #
    #         ax.cla()
    #         ax.axis('off')
    #         ax.axis('equal')
    #         if SCALE is not None:
    #             ax.set_xlim(-SCALE, SCALE)
    #             ax.set_ylim(-SCALE, SCALE)
