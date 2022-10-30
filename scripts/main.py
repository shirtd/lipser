import numpy as np
import lips


from lips.util import array, iter

print(f"\nutil.array\n\t{array.get_grid(2)}")
print(f"\nutil.iter\n\t{iter.lmap(lambda x: 2*x, 'misisipi')}\n")

from lips.topology import RipsComplex

P = np.random.rand(10,2)
K = RipsComplex(P, 1)
print(f"\ntopology.RipsComplex\n{K}\n")

from lips.topology import Filtration, Diagram

F = Filtration(K, 'dist')
print(f"topology.Filtration\n{F}\n")

from lips.topology import Diagram

H = Diagram(K, F)
print(f"topology.Filtration\n{H.diagram}\n")
