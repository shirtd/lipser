#! /bin/bash


NAME=${1:-'surf'}
RES=${2:-8}
THRESH=${3:-100}
SUBTHRESH=${4:-300}

STEP=0
DIR="data/${NAME}"
DATA="${DIR}/${NAME}.asc"
RDATA="${DIR}/${NAME}${RES}.csv"
SAMPLE_PATH=${DIR}/samples/${NAME}${RES}-sample

RUN () {
  printf '%s%s%s\n' "$(tput setaf 2)" "($STEP) python $1" "$(tput sgr0)"
  STEP=$( expr $STEP + 1 )
  python $1
}

RUN "parse.py $DATA --gauss --downsample $RES --save"
RUN "surf.py $RDATA --save --contours --barcode"
RUN "surf.py $RDATA --save --force --greedy --thresh $THRESH"
RUN "surf.py $RDATA --save --force --greedy --thresh $SUBTHRESH"

SAMPLE=$( echo "${SAMPLE_PATH}"*"_${THRESH}.csv" )
SUBSAMPLE=$( echo "${SAMPLE_PATH}"*"_${SUBTHRESH}.csv" )

RUN "rips.py $SAMPLE --save --barcode"
for COLOR in '' '--color'; do
  for SUB in '--cover' '--union'; do
    RUN "rips.py $SAMPLE --save --contours $SUB $COLOR"
  done
done

# RUN "rips.py $SAMPLE --save --contours --rips --color"

RUN "rips.py $SAMPLE --sub-file $SUBSAMPLE --save --contours --lips --barcode --rips --color"

for COLOR in '' '--color'; do
  for SUB in '--cover' '--union'; do
    RUN "rips.py $SAMPLE --save --contours $SUB --lips $COLOR"
  done
done

# for SAMPLENAME in $SAMPLE $SUBSAMPLE; do
#   RUN "rips.py $SAMPLENAME --save --barcode --contours --graph"
#   for COLOR in '' '--color'; do
#     for SUB in '--cover' '--union'; do
#       RUN "rips.py $SAMPLENAME --save --contours $SUB $COLOR"
#     done
#   done
#   RUN "rips.py $SAMPLENAME --save --contours --rips --color"
# done
#
# RUN "rips.py $SAMPLE --sub-file $SUBSAMPLE --save --lips --barcode"
# RUN "rips.py $SAMPLE --sub-file $SUBSAMPLE --save --contours --rips --lips --color"
# for SUB in '--cover' '--union' '--rips'; do
#   RUN "rips.py $SAMPLE --save --contours $SUB --lips $FLAG $COLOR"
# done
#
# # RUN "rips.py $SAMPLE --sub-file $SUBSAMPLE --save --lips --barcode"
# # for FLAG in '' '--nomin' '--nomax'; do
# #   for COLOR in '' '--color'; do
# #     RUN "rips.py $SAMPLE --sub-file $SUBSAMPLE --save --contours --rips --lips $FLAG $COLOR"
# #     for SUB in '--cover' '--union' '--rips'; do
# #       RUN "rips.py $SAMPLE --save --contours $SUB --lips $FLAG $COLOR"
# #     done
# #   done
# # done
