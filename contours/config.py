import numpy as np

CONFIG = {  'surf32' :    {'res' : 32, 'shape' : (2,1), 'pad' : (1.2, 1.55),
                        'cuts' : [0.05, 0.3, 0.55, 0.8, 1.35],
                        'colors' : ['green', 'blue', 'purple', 'yellow'],
                        'labels' : ['A', 'B', 'C', 'D'],
                        'lips' : 3.1443048369350226, 'lw' : 5,
                        'gauss_args' : [(1,     [-0.2, 0.2],    [0.3, 0.3]),
                                        (0.5,   [-1.3, -0.1],   [0.15, 0.15]),
                                        (0.7,   [-0.8, -0.4],   [0.2, 0.2]),
                                        (0.8,   [-0.8, -0],     [0.4, 0.4]),
                                        (0.4,   [0.6, 0.0],     [0.4, 0.2]),
                                        (0.7,   [1.25, 0.3],    [0.25, 0.25])]},
            'rainier_sub16' : {'res' : 337, 'shape' : (1,1), 'pad' : (1.3, 1.3),
                        'cuts' : [200, 1000, 1400, 1800, 2500, 4500],
                        'colors' : ['blue','green','yellow','salmon','purple'],
                        'labels' : ['A', 'B', 'C', 'D', 'E'],
                        'min' : 265.258441, 'max' : 4379.845434, 'lw' : 1,
                        'lips' : 46519.52591999933},
            'rainier_peak' : {'res' : 230, 'shape' : (1,1), 'pad' : (1.3, 1.3),
                        'cuts' : [1800, 2000, 2300, 2600, 3100, 4500],
                        'colors' : ['blue','green', 'yellow', 'salmon', 'purple'],
                        # 'colors' : ['green', 'yellow','salmon','purple'],
                        'labels' : ['A', 'B', 'C', 'D', 'E'],
                        'min' : 265.258441, 'max' : 4379.845434, 'lw' : 1,
                        'lips' : 31705.27213000035},
                        # 'lips' : 25483.938340730343},
            'circle'  : {'res' : 256, 'weight' : 0.5, 'scale' : 2.8, 'seed' : 0,
                        'cuts' : [0, 0.07, 0.15, 0.2, 0.27, 0.4, 0.6, 0.75, 1.3]}}

CONFIG['surf32_2'] = CONFIG['surf32'].copy()
CONFIG['surf32_2']['cuts'] = [0.05, 0.2, 0.45, 0.875, 1.09, 1.31]
CONFIG['surf32_2']['colors'] = ['blue','green','yellow','salmon','purple']
CONFIG['surf32_2']['labels'] = ['A', 'B', 'C', 'D', 'E']

CONFIG['surf8'] = CONFIG['surf32'].copy()
CONFIG['surf8']['res'] = 8
