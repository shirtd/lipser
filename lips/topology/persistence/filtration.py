from lips.topology.complex.chains import Chain, CoChain
from lips.util import insert, partition


class Filtration:
    def __init__(self, K, key, reverse=False, filter=None):
        self.sequence = K.get_sequence(key, reverse)
        self.dim, self.key, self.reverse = K.dim, key, reverse
        self.imap = {hash(s) : i for i, s in enumerate(self)}
    def __len__(self):
        return len(self.sequence)
    def __iter__(self):
        yield from self.sequence
    def __getitem__(self, i):
        return self.sequence[i]
    def index(self, s):
        return self.imap[hash(s)]
    def get_range(self, R=set(), coh=False):
        it = reversed(list(enumerate(self))) if coh else enumerate(self)
        f = lambda L,ix: L if ix[0] in R else insert(L, ix[1].dim, ix[0])
        return partition(f, it, self.dim+1)[::(1 if coh else -1)]
    def sort_faces(self, K, i, pivot=None):
        pivot = self if pivot is None else pivot
        return sorted([pivot.index(f) for f in K.faces(self[i])])
    def sort_cofaces(self, K, i, pivot=None):
        pivot = self if pivot is None else pivot
        return sorted([pivot.index(f) for f in K.cofaces(self[i])], reverse=True)
    def as_chain(self, K, i, pivot=None):
        return Chain({i}, self.sort_faces(K, i, pivot))
    def as_cochain(self, K, i, pivot=None):
        return CoChain({i}, self.sort_cofaces(K, i, pivot))
    def get_chains(self, K, rng, pivot=None):
        return {i : self.as_chain(K, i, pivot) for i in rng}
    def get_cochains(self, K, rng, pivot=None):
        return {i : self.as_cochain(K, i, pivot) for i in rng}
    def get_matrix(self, K, rng, coh=False, pivot=None):
        return (self.get_cochains if coh else self.get_chains)(K, rng, pivot)
