import numpy as np

CONFIG = {  'surf' :    {'res' : 32, 'shape' : (2,1),
                        'cuts' : [0.05, 0.2, 0.45, 0.875, 1.09, 1.31],
                        'colors' : ['blue','green','yellow','salmon','purple'],
                        'labels' : ['A', 'B', 'C', 'D', 'E'],
                        'lips' : 3.1443048369350226},
            'rainier' : {'res' : 337, 'shape' : (1,1),
                        'cuts' : [200, 1000, 1400, 1800, 2200, 4500],
                        'colors' : ['blue','green','yellow','salmon','purple'],
                        'labels' : ['A', 'B', 'C', 'D', 'E'],
                        'min' : 265.258441, 'max' : 4379.845434,
                        'lips' : 25483.938340730343}}



# LABELS = ['A', 'B', 'C', 'D']
# CUTS = [0.05, 0.3, 0.55, 0.8, 1.3]
# COLOR_ORDER = ['green', 'blue', 'purple', 'yellow']
