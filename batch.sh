#! /bin/bash

COLOR_REST="$(tput sgr0)"
COLOR_GREEN="$(tput setaf 2)"
STEP=0

RES=32 # 16 # s
NAME='rainier_sub' # 'surf' #
THRESH=2e+03 # 2.5e-01 # 3e-01 #
SUBTHRESH=3.5e+03 # 4e-01 #5.5e-01 #
# THRESH2=2.31e-01
# SUBTHRESH2=3.47e-01

DIR="data/${NAME}"
DATA="${DIR}/${NAME}.asc"
RDATA="${DIR}/${NAME}${RES}.csv"


# (0)
CMD="parse.py $DATA --gauss --downsample $RES --save"
printf '%s%s%s\n' $COLOR_GREEN "($STEP) python $CMD" $COLOR_REST
STEP=$( expr $STEP + 1 )
python $CMD
# python surf.py data/surf/surf16.csv --greedy --thresh 2.5e-1 --show



# SAMPLE_PATH=${DIR}/samples/${NAME}${RES}-sample
#
# SAMPLE=${SAMPLE_PATH}*_${THRESH}.csv
# SUBSAMPLE=${SAMPLE_PATH}*_${SUBTHRESH}.csv

# SAMPLE_PATH=${DIR}/samples/${NAME}${RES}-sample
SAMPLE=${DIR}/samples/${NAME}${RES}-sample*_${THRESH}.csv
SUBSAMPLE=${DIR}/samples/${NAME}${RES}-sample*_${SUBTHRESH}.csv

# SAMPLE2=${SAMPLE_NAME}*_${THRESH2}.csv
# SUBSAMPLE2=${SAMPLE_NAME}*_${SUBTHRESH2}.csv

# rm -r "figures/${NAME}${RES}"

# ()
CMD="surf.py $RDATA --save --contours --barcode"
printf '%s%s%s\n' $COLOR_GREEN "($STEP) python $CMD" $COLOR_REST
STEP=$( expr $STEP + 1 )
python $CMD

# (2)
CMD="surf.py $RDATA --save --sample --thresh $THRESH"
printf '%s%s%s\n' $COLOR_GREEN "($STEP) python $CMD" $COLOR_REST
STEP=$( expr $STEP + 1 )
python $CMD

# (3)
CMD="surf.py $RDATA --save --sample --thresh $SUBTHRESH"
printf '%s%s%s\n' $COLOR_GREEN "($STEP) python $CMD" $COLOR_REST
STEP=$( expr $STEP + 1 )
python $CMD

# cp $SAMPLE $SSAMPLE
# cp $SUBSAMPLE $SSUBSAMPLE
# cp ${SAMPLE_PATH}*_${THRESH}.json ${SAMPLE_PATH}_${THRESH2}.json
# cp ${SAMPLE_PATH}*_${SUBTHRESH}.json ${SAMPLE_PATH}_${SUBTHRESH2}.json


# STEP=4
# (4) - (17)
for SAMPLENAME in $SAMPLE $SUBSAMPLE; do # $SAMPLE2 $SUBSAMPLE2; do
  # (4), (11),
  CMD="rips.py $SAMPLENAME --save --barcode --contours --graph"
  printf '%s%s%s\n' $COLOR_GREEN "($STEP) python $CMD" $COLOR_REST
  STEP=$( expr $STEP + 1 )
  python $CMD
  for COLOR in '' '--color'; do
    for RUN in '--cover' '--union' '--rips'; do
      # (5), (6), (7), (8), (9), (10),
      # (12), (13), (14), (15), (16), (17)
      CMD="rips.py $SAMPLENAME --save --contours $RUN $COLOR"
      printf '%s%s%s\n' $COLOR_GREEN "($STEP) python $CMD" $COLOR_REST
      STEP=$( expr $STEP + 1 )
      python $CMD
    done
  done
done

# DABUG
CMD="rips.py $SAMPLE --sub-file $SUBSAMPLE --save --lips --barcode"
printf '%s%s%s\n' $COLOR_GREEN "($STEP) python $CMD" $COLOR_REST
STEP=$( expr $STEP + 1 )
python $CMD
for FLAG in '' '--nomin' '--nomax'; do
  for COLOR in '' '--color'; do
      CMD="rips.py $SAMPLE --sub-file $SUBSAMPLE --save --contours --rips --lips $FLAG $COLOR"
      printf '%s%s%s\n' $COLOR_GREEN "($STEP) python $CMD" $COLOR_REST
      STEP=$( expr $STEP + 1 )
      python $CMD
    for RUN in '--cover' '--union' '--rips'; do
      CMD="rips.py $SAMPLE --save --contours $RUN --lips $FLAG $COLOR"
      printf '%s%s%s\n' $COLOR_GREEN "($STEP) python $CMD" $COLOR_REST
      STEP=$( expr $STEP + 1 )
      python $CMD
    done
  done
done


# python rips.py $SAMPLENAME --save --contours --cover
# python rips.py $SAMPLENAME --save --contours --cover --color
#
# python rips.py $SAMPLENAME --save --contours --union
# python rips.py $SAMPLENAME --save --contours --union --color
#
# python rips.py $SAMPLENAME --save --contours --rips
# python rips.py $SAMPLENAME --save --contours --rips --color

# python rips.py $SAMPLE --save --contours --cover --lips --nomin
# python rips.py $SAMPLE --save --contours --cover --lips --nomax
# python rips.py $SAMPLE --save --contours --cover --lips --color
# python rips.py $SAMPLE --save --contours --cover --lips --nomin --color
# python rips.py $SAMPLE --save --contours --cover --lips --nomax --color
#
# python rips.py $SAMPLE --save --contours --union --lips
# python rips.py $SAMPLE --save --contours --union --lips --nomin
# python rips.py $SAMPLE --save --contours --union --lips --nomax
# python rips.py $SAMPLE --save --contours --union --lips --color
# python rips.py $SAMPLE --save --contours --union --lips --nomin --color
# python rips.py $SAMPLE --save --contours --union --lips --nomax --color
#
# python rips.py $SAMPLE --save --contours --rips --lips
# python rips.py $SAMPLE --save --contours --rips --lips --nomin
# python rips.py $SAMPLE --save --contours --rips --lips --nomax
# python rips.py $SAMPLE --save --contours --rips --lips --color
# python rips.py $SAMPLE --save --contours --rips --lips --nomin --color
# python rips.py $SAMPLE --save --contours --rips --lips --nomax --color
#
# python rips.py $SAMPLE --sub-file $SUBSAMPLE --save --lips --barcode
# python rips.py $SAMPLE --sub-file $SUBSAMPLE --save --lips --rips --contours
# python rips.py $SAMPLE --sub-file $SUBSAMPLE --save --lips --rips --contours --nomin
# python rips.py $SAMPLE --sub-file $SUBSAMPLE --save --lips --rips --contours --nomax
# python rips.py $SAMPLE --sub-file $SUBSAMPLE --save --lips --rips --contours --color
# python rips.py $SAMPLE --sub-file $SUBSAMPLE --save --lips --rips --contours --nomin --color
# python rips.py $SAMPLE --sub-file $SUBSAMPLE --save --lips --rips --contours --nomax --color



# python parse.py data/test/test.asc # --show # --save
# python parse.py data/test/test.asc --downsample 32 # --show # --save
#
# python parse.py data/test/test.asc --downsample 32 --save
#
# python surf.py data/test/test32.csv # --show # --save
# python surf.py data/test/test32.csv --contours # --show # --save
#
#
# python surf.py data/test/test32.csv --sample
# python surf.py data/test/test32.csv --sample --greedy --thresh 1000



# # TODO surf --color
# # image persistence
# # subsample with new format
# # - subsample rainier
#
# SURF='data/rainier_peak.csv'
# SAMPLE='data/rainier_peak-sample-683_7e-02.csv'
#
# # SURF='data/rainier_sub16.csv'
# # SAMPLE='data/rainier_sub16-sample-2466_7.5e-02.csv'
# # SUB='data/rainier_sub16-sample-2466_7.5e-02-subsample_488.csv'
# # PARTIAL='data/rainier_sub16-sample-514_7.5e-02.csv'
#
# # SURF='data/surf32.csv'
# # SAMPLE='data/surf32-sample-1233_1.25e-01.csv'
# # SUB='data/surf32-sample-1233_1.25e-01-subsample_401.csv'
# # PARTIAL='data/surf32-partial-sample-393_1.3e-01.csv'
#
# python surf.py --file 'data/rainier/small/test.csv' --show
#
# python surf.py --save --file $SURF --contours
#
# python surf.py --save --file $SURF --sample-file $SAMPLE
# python surf.py --save --file $SURF --sample-file $SAMPLE --cover
# python surf.py --save --file $SURF --sample-file $SAMPLE --union
# python surf.py --save --file $SURF --sample-file $SAMPLE --cover --color
# python surf.py --save --file $SURF --sample-file $SAMPLE --union --color
# python surf.py --save --file $SURF --sample-file $SAMPLE --cover --nosurf
# python surf.py --save --file $SURF --sample-file $SAMPLE --union --nosurf
# python surf.py --save --file $SURF --sample-file $SAMPLE --cover --nosurf --color
# python surf.py --save --file $SURF --sample-file $SAMPLE --union --nosurf --color
#
# if [ -n "$PARTIAL" ]; then
#   python surf.py --save --file $SURF --sample-file $PARTIAL
#   python surf.py --save --file $SURF --sample-file $PARTIAL --cover
#   python surf.py --save --file $SURF --sample-file $PARTIAL --union
#   python surf.py --save --file $SURF --sample-file $PARTIAL --nosurf
#   python surf.py --save --file $SURF --sample-file $PARTIAL --cover --nosurf
#   python surf.py --save --file $SURF --sample-file $PARTIAL --union --nosurf
#   python surf.py --save --file $SURF --sample-file $PARTIAL --color
#   python surf.py --save --file $SURF --sample-file $PARTIAL --cover --color
#   python surf.py --save --file $SURF --sample-file $PARTIAL --union --color
#   python surf.py --save --file $SURF --sample-file $PARTIAL --cover --nosurf --color
#   python surf.py --save --file $SURF --sample-file $PARTIAL --union --nosurf --color
# fi
#
#
# python rips.py --save --file $SURF --sample-file $SAMPLE
# python rips.py --save --file $SURF --sample-file $SAMPLE --union
# python rips.py --save --file $SURF --sample-file $SAMPLE --rips
# python rips.py --save --file $SURF --sample-file $SAMPLE --graph
# python rips.py --save --file $SURF --sample-file $SAMPLE --barcode
#
# python rips.py --save --file $SURF --sample-file $SAMPLE --color
# python rips.py --save --file $SURF --sample-file $SAMPLE --rips --color
# python rips.py --save --file $SURF --sample-file $SAMPLE --union --color
#
# if [ -n "$PARTIAL" ]; then
#   python rips.py --save --file $SURF --sample-file $PARTIAL
#   python rips.py --save --file $SURF --sample-file $PARTIAL --union
#   python rips.py --save --file $SURF --sample-file $PARTIAL --rips
#   python rips.py --save --file $SURF --sample-file $PARTIAL --barcode
#
#   python rips.py --save --file $SURF --sample-file $PARTIAL --color
#   python rips.py --save --file $SURF --sample-file $PARTIAL --rips --color
#   python rips.py --save --file $SURF --sample-file $PARTIAL --union --color
# fi
#
#
# python lips.py --save --file $SURF --sample-file $SAMPLE
# python lips.py --save --file $SURF --sample-file $SAMPLE --nomax
# python lips.py --save --file $SURF --sample-file $SAMPLE --nomin
# python lips.py --save --file $SURF --sample-file $SAMPLE --union
# python lips.py --save --file $SURF --sample-file $SAMPLE --nomax --union
# python lips.py --save --file $SURF --sample-file $SAMPLE --nomin --union
# python lips.py --save --file $SURF --sample-file $SAMPLE --rips
# python lips.py --save --file $SURF --sample-file $SAMPLE --nomax --rips
# python lips.py --save --file $SURF --sample-file $SAMPLE --nomin --rips
#
# if [ -n "$SUB" ]; then
#
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --nomax
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --nomin
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --union
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --nomax --union
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --nomin --union
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --rips
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --nomax --rips
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --nomin --rips
#
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --rips --sub
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --rips --sub --nomin
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --rips --sub --nomax
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --barcode
#
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --union
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --color
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --nosub
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --nosub --union
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --nosub --color
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --nosample
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --nosample --union
#   python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $SUB --cover --nosample --color
#
#   if [ -n "$PARTIAL" ]; then
#     python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover
#     python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --union
#     python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --color
#     python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosub
#     python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosub --union
#     python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosub --color
#     python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosample
#     python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosample --union
#     python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosample --color
#     python lips.py --save --file $SURF --sample-file $SAMPLE --sub-file $PARTIAL --cover --nosample --color
#   fi
# fi
#
#
# # python circle.py --save
# # python circle.py --save --union
# # python circle.py --save --rips
# # python circle.py --save --graph
