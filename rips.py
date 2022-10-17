from contours.data import make_grid, ScalarFieldFile

RES = 32
SHAPE = (2,1)
PATH = 'data/surf32.csv'

if __name__ == '__main__':
    surf = ScalarFieldFile(PATH, make_grid(RES, SHAPE))
