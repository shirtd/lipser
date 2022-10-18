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

if __name__ == '__main__':

    SKIP = 4
    FRAMES = 50
    COEF = 60
    SCALE = None

    for i in range(len(mics)):
        try:
            print(f"{i}: {mics[i].name}")
        except Exception as e:
            print(e)

    kw = {  'in':   {   'samplerate':   148000},
            'out':  {   'samplerate':   148000}}

    with (  default_mic.recorder(**kw['in']) as mic ) : # ,
            # default_speaker.player(**kw['out']) as sp):
        print("Recording...")
        _data = mic.record(numframes=COEF*FRAMES)
        data = _data[::SKIP]

    # fout = 'data/drip2.txt'
    # print("saving %s" % fout)
    # np.savetxt(fout, data)

    plt.ion()
    # plt.scatter(data[:,0]+1, data[:,1]+1, s=1, alpha=0.1)
    # plt.scatter(data[:,2], data[:,3], s=2, alpha=0.1)
    fig, ax = plt.subplots()
    ax.plot(data[:,4], data[:,5], alpha=0.15)
    ax.axis('off')
    if SCALE is not None:
        ax.set_xlim(-SCALE,SCALE)
        ax.set_ylim(-SCALE,SCALE)
    # plt.show()

    if input('save? ') in {'y','yes','Y'}:
        plt.savefig('data/last_frame.png')

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
