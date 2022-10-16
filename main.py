
import lipser
# from lipser.util import math
from lipser.util import array
from lipser.util import iter
from lipser.topology import complex
# from lipser import data
# from lipser import geometry
# from lipser import graph
# from lipser import plot
# from lipser import topology
# import lipser.util.array as array

import numpy as np

G = np.eye(4)
for t in array.get_grid(4):
    print(t)

print(iter.lmap(lambda x: 2*x, 'misisipi'))
