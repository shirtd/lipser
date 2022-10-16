import lipser
import numpy as np

from lipser.util import array, iter

print(f"\nutil.array\n\t{array.get_grid(2)}")
print(f"\nutil.iter\n\t{iter.lmap(lambda x: 2*x, 'misisipi')}\n")


from lipser.topology import RipsComplex

P = np.random.rand(10,2)
K = RipsComplex(P, 1)
print(f"\ntopology.RipsComplex\n{K}\n")

from lipser.topology import Filtration, Diagram
F = Filtration(K, 'dist')
H = Diagram(K, F)
B = H.diagram
# from lipser.geometry import util
