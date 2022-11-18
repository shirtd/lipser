#! /bin/bash
# # color lips max but not min (min is red: dead)
# # python parse.py data/rainier_small/rainier_small.asc --downsample 8 --save
# ./batch.sh rainier_small 8 1000 2500
#
# # python parse.py data/rainier_sub/rainier_sub.asc --cuts 200 1000 1400 1800 2500 4500 --downsample 32 --save
# ./batch.sh rainier_sub 32 2000 3500

# python parse.py data/olympics/olympics.asc  --cuts 700 1000 1400 1650 2000 2500 --downsample 32 --save
./batch.sh olympics 32 3000 5000

# python parse.py data/cascades/cascades.asc --show --cuts 1 100 700 1400 2100 4500 --save --downsample 64
./batch.sh cascades 64 10000 15000

# python parse.py data/northwest/northwest.asc --cuts 1 100 700 1400 2100 4500 --downsample 128 --save
./batch.sh northwest 128 17000 25000
