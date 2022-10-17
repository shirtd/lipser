import argparse
import os

parser = argparse.ArgumentParser(prog='contours')

parser.add_argument('--dir', default=os.path.join('figures','lips'), help='dir')
parser.add_argument('--file', default='data/surf_279_2e-1.csv', help='file')
parser.add_argument('--dpi', type=int, default=300, help='dpi')
parser.add_argument('--wait', type=float, default=0.5, help='wait')
parser.add_argument('--save', action='store_true', help='save')
parser.add_argument('--comp', action='store_true', help='min complement')
parser.add_argument('--mult', type=float, default=1., help='thresh mult')
parser.add_argument('--cmult', type=float, default=1., help='c mult')
