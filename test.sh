#! /bin/bash


python sfa.py --save
python sfa.py --save --union
python sfa.py --save --rips
python sfa.py --save --barcode

python sfa.py --save --color
python sfa.py --save --rips --color
python sfa.py --save --union --color


python lips.py --save
python lips.py --save --nomax
python lips.py --save --nomin
python lips.py --save --union
python lips.py --save --nomax --union
python lips.py --save --nomin --union
python lips.py --save --rips
python lips.py --save --nomax --rips
python lips.py --save --nomin --rips
python lips.py --save --sub
python lips.py --save --nomin --sub
python lips.py --save --nomax --sub
python lips.py --save --barcode


python circle.py --save
python circle.py --save --union
python circle.py --save --rips
python circle.py --save --graph
