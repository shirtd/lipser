#! /bin/bash

python surf.py --save --contours

python surf.py --save --sample-file 'data/surf-sample_1067_1.3e-1.csv'
python surf.py --save --sample-file 'data/surf-sample_1067_1.3e-1.csv' --cover
python surf.py --save --sample-file 'data/surf-sample_1067_1.3e-1.csv' --union
python surf.py --save --sample-file 'data/surf-sample_1067_1.3e-1.csv' --cover --color
python surf.py --save --sample-file 'data/surf-sample_1067_1.3e-1.csv' --union --color
python surf.py --save --sample-file 'data/surf-sample_1067_1.3e-1.csv' --cover --nosurf
python surf.py --save --sample-file 'data/surf-sample_1067_1.3e-1.csv' --union --nosurf
python surf.py --save --sample-file 'data/surf-sample_1067_1.3e-1.csv' --cover --nosurf --color
python surf.py --save --sample-file 'data/surf-sample_1067_1.3e-1.csv' --union --nosurf --color

# python surf.py --save --sample-file 'data/surf32-partial-sample-393_1.3e-01.csv'
# python surf.py --save --sample-file 'data/surf32-partial-sample-393_1.3e-01.csv' --cover
# python surf.py --save --sample-file 'data/surf32-partial-sample-393_1.3e-01.csv' --union
# python surf.py --save --sample-file 'data/surf32-partial-sample-393_1.3e-01.csv' --nosurf
# python surf.py --save --sample-file 'data/surf32-partial-sample-393_1.3e-01.csv' --cover --nosurf
# python surf.py --save --sample-file 'data/surf32-partial-sample-393_1.3e-01.csv' --union --nosurf
# python surf.py --save --sample-file 'data/surf32-partial-sample-393_1.3e-01.csv' --color
# python surf.py --save --sample-file 'data/surf32-partial-sample-393_1.3e-01.csv' --cover --color
# python surf.py --save --sample-file 'data/surf32-partial-sample-393_1.3e-01.csv' --union --color
# python surf.py --save --sample-file 'data/surf32-partial-sample-393_1.3e-01.csv' --cover --nosurf --color
# python surf.py --save --sample-file 'data/surf32-partial-sample-393_1.3e-01.csv' --union --nosurf --color
#
#
# python rips.py --save
# python rips.py --save --union
# python rips.py --save --rips
# python rips.py --save --barcode
#
# python rips.py --save --color
# python rips.py --save --rips --color
# python rips.py --save --union --color
#
# python rips.py --file 'data/surf32-partial-sample-393_1.3e-01.csv' --save
# python rips.py --file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --union
# python rips.py --file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --rips
# python rips.py --file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --barcode
#
# python rips.py --file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --color
# python rips.py --file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --rips --color
# python rips.py --file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --union --color
#
#
# python lips.py --save
# python lips.py --save --nomax
# python lips.py --save --nomin
# python lips.py --save --union
# python lips.py --save --nomax --union
# python lips.py --save --nomin --union
# python lips.py --save --rips
# python lips.py --save --nomax --rips
# python lips.py --save --nomin --rips
# python lips.py --save --sub
# python lips.py --save --nomin --sub
# python lips.py --save --nomax --sub
# python lips.py --save --barcode
#
# python lips.py --save --cover
# python lips.py --save --cover --union
# python lips.py --save --cover --color
# python lips.py --save --cover --nosub
# python lips.py --save --cover --nosub --union
# python lips.py --save --cover --nosub --color
# python lips.py --save --cover --nosample
# python lips.py --save --cover --nosample --union
# python lips.py --save --cover --nosample --color
#
# python lips.py --sub-file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --cover
# python lips.py --sub-file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --cover --union
# python lips.py --sub-file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --cover --color
# python lips.py --sub-file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --cover --nosub
# python lips.py --sub-file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --cover --nosub --union
# python lips.py --sub-file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --cover --nosub --color
# python lips.py --sub-file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --cover --nosample
# python lips.py --sub-file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --cover --nosample --union
# python lips.py --sub-file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --cover --nosample --color
# python lips.py --sub-file 'data/surf32-partial-sample-393_1.3e-01.csv' --save --cover --nosample --color
#
#
# python circle.py --save
# python circle.py --save --union
# python circle.py --save --rips
# python circle.py --save --graph
