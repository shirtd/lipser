#! /bin/bash


# TODO surf --color
# image persistence
# subsample with new format
# - subsample rainier


SURF='data/rainier_sub16.csv'
SAMPLE='data/rainier_sub16-sample-2318_7.5e-02.csv'

# SURF='data/surf32.csv'
# SAMPLE='data/surf-sample_1067_1.3e-1.csv'
# SUB='data/surf-sample_329_2e-1.csv'
# PARTIAL='data/surf32-partial-sample-393_1.3e-01.csv'



python surf.py --save --file $SURF --contours

python surf.py --save --file $SURF --sample-file $SAMPLE
python surf.py --save --file $SURF --sample-file $SAMPLE --cover
python surf.py --save --file $SURF --sample-file $SAMPLE --union
python surf.py --save --file $SURF --sample-file $SAMPLE --cover --color
python surf.py --save --file $SURF --sample-file $SAMPLE --union --color
python surf.py --save --file $SURF --sample-file $SAMPLE --cover --nosurf
python surf.py --save --file $SURF --sample-file $SAMPLE --union --nosurf
python surf.py --save --file $SURF --sample-file $SAMPLE --cover --nosurf --color
python surf.py --save --file $SURF --sample-file $SAMPLE --union --nosurf --color

if [ -n "$PARTIAL" ]; then
  python surf.py --save --file $SURF --sample-file $PARTIAL
  python surf.py --save --file $SURF --sample-file $PARTIAL --cover
  python surf.py --save --file $SURF --sample-file $PARTIAL --union
  python surf.py --save --file $SURF --sample-file $PARTIAL --nosurf
  python surf.py --save --file $SURF --sample-file $PARTIAL --cover --nosurf
  python surf.py --save --file $SURF --sample-file $PARTIAL --union --nosurf
  python surf.py --save --file $SURF --sample-file $PARTIAL --color
  python surf.py --save --file $SURF --sample-file $PARTIAL --cover --color
  python surf.py --save --file $SURF --sample-file $PARTIAL --union --color
  python surf.py --save --file $SURF --sample-file $PARTIAL --cover --nosurf --color
  python surf.py --save --file $SURF --sample-file $PARTIAL --union --nosurf --color
fi


python rips.py --save --file $SURF --sample-file $SAMPLE
python rips.py --save --file $SURF --sample-file $SAMPLE --union
python rips.py --save --file $SURF --sample-file $SAMPLE --rips
python rips.py --save --file $SURF --sample-file $SAMPLE --barcode

python rips.py --save --file $SURF --sample-file $SAMPLE --color
python rips.py --save --file $SURF --sample-file $SAMPLE --rips --color
python rips.py --save --file $SURF --sample-file $SAMPLE --union --color

if [ -n "$PARTIAL" ]; then
  python rips.py --save --file $SURF --sample-file $PARTIAL
  python rips.py --save --file $SURF --sample-file $PARTIAL --union
  python rips.py --save --file $SURF --sample-file $PARTIAL --rips
  python rips.py --save --file $SURF --sample-file $PARTIAL --barcode

  python rips.py --save --file $SURF --sample-file $PARTIAL --color
  python rips.py --save --file $SURF --sample-file $PARTIAL --rips --color
  python rips.py --save --file $SURF --sample-file $PARTIAL --union --color
fi


python lips.py --save --file $SURF --sample-file $SAMPLE
python lips.py --save --file $SURF --sample-file $SAMPLE --nomax
python lips.py --save --file $SURF --sample-file $SAMPLE --nomin
python lips.py --save --file $SURF --sample-file $SAMPLE --union
python lips.py --save --file $SURF --sample-file $SAMPLE --nomax --union
python lips.py --save --file $SURF --sample-file $SAMPLE --nomin --union
python lips.py --save --file $SURF --sample-file $SAMPLE --rips
python lips.py --save --file $SURF --sample-file $SAMPLE --nomax --rips
python lips.py --save --file $SURF --sample-file $SAMPLE --nomin --rips

if [ -n "$SUB" ]; then

  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --nomax
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --nomin
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --union
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --nomax --union
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --nomin --union
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --rips
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --nomax --rips
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --nomin --rips

  python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --sub
  python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --sub --nomin
  python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --sub --nomax
  python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --barcode

  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --union
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --color
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --nosub
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --nosub --union
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --nosub --color
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --nosample
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --nosample --union
  # python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --nosample --color

  if [ -n "$PARTIAL" ]; then
    python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover
    python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --union
    python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --color
    python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosub
    python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosub --union
    python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosub --color
    python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosample
    python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosample --union
    python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosample --color
    python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosample --color
  fi
fi


# python circle.py --save
# python circle.py --save --union
# python circle.py --save --rips
# python circle.py --save --graph
