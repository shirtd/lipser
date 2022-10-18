import matplotlib.pyplot as plt

import numpy as np

from lips.topology import RipsComplex
from contours.surface import make_grid, ScalarFieldData, SampleData
from contours.plot import plot_surface, plot_points, plot_rips
from contours.style import COLOR

import os

#
# https://stackoverflow.com/questions/55143976/python-how-to-record-system-audiothe-output-from-the-speaker
#

import soundcard as sc
import time

# get a list of all speakers:
speakers = sc.all_speakers()
# get the current default speaker on your system:
default_speaker = sc.default_speaker()

# get a list of all microphones:v
mics = sc.all_microphones(include_loopback=True)
# get the current default microphone on your system:
default_mic = mics[1]


# RES = 32
# SHAPE = (2,1)
# SURF_PATH = 'data/surf32.csv'
# SAMP_PATH = 'data/surf-sample_329_2e-1.csv'
# MULT = 1.2
#
# # CUTS = [0.05, 0.3, 0.55, 0.8, 1.31]
# # COLOR_ORDER = ['green', 'blue', 'purple', 'yellow']
# CUTS = [0.05, 0.2, 0.45, 0.875, 1.09, 1.31]
# COLOR_ORDER = ['blue','green','yellow','salmon','purple']
# COLORS = [COLOR[k] for k in COLOR_ORDER]

import argparse

parser = argparse.ArgumentParser(prog='circler')

parser.add_argument('--dir', default=os.path.join('figures','lips'), help='dir')
parser.add_argument('--file', default='data/surf_279_2e-1.csv', help='file')


# def plot_points(self, points, key, radius=DEFAULT['point']['radius'], **kwargs):
#     points = np.array([p for p in points if all(0 <= c <= l for l,c in zip(self.bounds, p))])
#     element = pyvista.PolyData(points).glyph(scale=False, geom=pyvista.Sphere(radius=radius))
#     kwargs = {**{'color' : DEFAULT['point']['color']}, **kwargs}
#     return self.add_element(element, key, **kwargs)

if __name__ == '__main__':

    SKIP = 4
    FRAMES = 100
    COEF = 60
    SCALE = None
    WEIGHT = 10

    LENGTH = 30

    for i in range(len(mics)):
        try:
            print(f"{i}: {mics[i].name}")
        except Exception as e:
            print(e)

    kw = {  'in':   {   'samplerate':   148000},
            'out':  {   'samplerate':   148000}}

    plt.ion()
    # plt.scatter(data[:,0]+1, data[:,1]+1, s=1, alpha=0.1)
    # plt.scatter(data[:,2], data[:,3], s=2, alpha=0.1)
    fig, ax = plt.subplots()
    ax.axis('off')

    if SCALE is not None:
        ax.set_xlim(-SCALE,SCALE)
        ax.set_ylim(-SCALE,SCALE)

    with (  default_mic.recorder(**kw['in']) as mic ) : # ,
            # default_speaker.player(**kw['out']) as sp):


        for i in range(LENGTH):
            print("Recording...")
            _data = mic.record(numframes=COEF*FRAMES)

            data = _data[::SKIP]*i/100
            time = np.linspace(0, WEIGHT, len(data))
            ax.plot(data[:,4]*time, data[:,5]*time, alpha=0.25,lw=0.5)
            plt.pause(1.1)


    # fout = 'data/drip2.txt'
    # print("saving %s" % fout)
    # np.savetxt(fout, data)


    # import pyvistaqt as pvqt
    # import pyvista
    # pvqt.BackgroundPlotter()
    # element = pyvista.PolyData(np.vstack([data[:,4:].T,np.array(range(len(data)))]).T).glyph(scale=False, geom=pyvista.Sphere(radius=10))




    # if input('save? ') in {'y','yes','Y'}:
    #     plt.savefig('data/last_frame.png')


    # surf = ScalarFieldData(SURF_PATH, make_grid(RES, SHAPE))
    # sample = SampleData(SAMP_PATH)
    # rips = RipsComplex(sample.points, sample.radius*MULT)
    # for s in rips:
    #     s.data['f'] = sample(s).max()
    #
    # plt.ion()
    # fig, ax = plt.subplots(figsize=(10,8))
    # surf_plt = plot_surface(ax, surf, CUTS, COLORS)
    # rips_plt = plot_rips(ax, rips, zorder=1, color=COLOR['red'], alpha=1/MULT)
    # plt.show()
