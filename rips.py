import matplotlib.pyplot as plt
import numpy as np
import argparse
import os, sys

from contours.args import parser
# from contours.surface import ScalarFieldFile
from contours.sample import MetricSampleFile
from contours.config import COLOR, KWARGS
from lips.topology import RipsComplex


if __name__ == '__main__':
    args = parser.parse_args()

    color_str = '-color' if args.color else ''

    # surf = ScalarFieldData(args.file, args.json)
    sample = MetricSampleFile(args.file)
    args.folder = os.path.join(args.folder, sample.parent, sample.name)
    if args.lips:
        args.folder = os.path.join(args.folder, 'lips')
    elif args.rips or args.graph:
        args.folder = os.path.join(args.folder, 'rips')
    elif args.cover or args.union:
        args.folder = os.path.join(args.folder, 'cover')
    if args.sub_file is not None:
        subsample = MetricSampleFile(args.sub_file)

    if args.cover or args.union:
        key = 'cover' if args.cover else 'union'
    elif args.rips or args.graph:
        key = 'rips' if args.rips else 'graph'
        rips = RipsComplex(sample.points, sample.radius, verbose=True)

    if args.contours:
        tag = f'{key}{color_str}'
        if args.lips:
            tag = f"lips-{tag}{'-max' if args.nomin else '-min' if args.nomax else ''}"
        plot_args = [args.show, args.save, args.folder, args.color, args.dpi]
        if args.cover or args.union:
            if args.lips:
                config = {'min' : {**{'visible' : not args.nomin}, **KWARGS['min'][key]},
                            'max' : {**{'visible' : not args.nomax}, **KWARGS['max'][key]}}
                sample.plot_lips_filtration(config, tag, *plot_args)
            else:
                sample.plot_cover_filtration(tag, *plot_args, **KWARGS[key])
        elif args.rips or args.graph:
            if args.lips:
                if args.sub_file is not None:
                    tag += f'-subsample{len(subsample)}_'
                    rips.lips_sub(subsample, sample.config['lips'])
                    config = {'min' : {**{'visible' : False}, **KWARGS['min'][key]},
                                'max' : {**{'visible' : False}, **KWARGS['max'][key]}}
                    sample.plot_rips_filtration(rips, config, tag, *plot_args, subsample=subsample)
                else:
                    rips.lips(sample, sample.config['lips'])
                    config = {'min' : {**{'visible' : True}, **KWARGS['min'][key]},
                                'max' : {**{'visible' : False}, **KWARGS['max'][key]}}
                    sample.plot_rips_filtration(rips, config, tag, *plot_args)
            else:
                rips.sublevels(sample)
                config = {'f' : {**{'visible' : False}, **KWARGS[key]}}
                sample.plot_rips_filtration(rips, config, tag, *plot_args)

    if args.barcode:
        if args.lips:
            sample_dgms = sample.plot_lips_barcode(subsample, args.folder, args.save, args.show, args.dpi, **KWARGS['barcode'])
        else:
            sample_dgms = sample.plot_barcode(args.folder, args.save, args.show, args.dpi, **KWARGS['barcode'])

    fig, ax = sample.init_plot()
    if args.sub_file is not None:
        sample.plot(ax, **KWARGS['supsample'])
        subsample.plot(ax, plot_color=args.color, **KWARGS['subsample'])
    else:
        sample.plot(ax, **KWARGS['sample'])

    tag = f"{key}{color_str}" if args.cover or args.union or args.rips or args.graph else None
    if args.cover or args.union:
        cover_plt = sample.plot_cover(ax, args.color, **KWARGS[key])
    elif args.rips or args.graph:
        rips_plt = sample.plot_rips(ax, rips, args.color, **KWARGS[key])

    if args.save:
        sample.save_plot(args.folder, args.dpi, tag, '-')

    if args.show:
        print('close plot to exit')
        plt.show()
