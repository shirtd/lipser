#! /bin/bash


NAME=${1:-'surf'}
RES=${2:-16}
THRESH=${3:-200}
SUBTHRESH=${4:-400}

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

# RUN "parse.py $DATA --gauss --downsample $RES --save"
# RUN "parse.py $DATA --downsample $RES --save"

RUN "surf.py $RDATA --save --contours --barcode"

RUN "surf.py $RDATA --save --force --greedy --thresh $THRESH"
RUN "surf.py $RDATA --save --force --greedy --thresh $SUBTHRESH"

SAMPLE=$( echo "${SAMPLE_PATH}"*"-${THRESH}.csv" )
SUBSAMPLE=$( echo "${SAMPLE_PATH}"*"-${SUBTHRESH}.csv" )

RUN "rips.py $SAMPLE --save --barcode --contours --rips --color"
RUN "rips.py $SUBSAMPLE --save --barcode --contours --rips --color"
RUN "rips.py $SAMPLE --sub-file $SUBSAMPLE --save --barcode --contours --lips --rips --color"
for COLOR in '' '--color'; do
  for SUB in '--cover' '--union'; do
    RUN "rips.py $SAMPLE --save --contours $SUB $COLOR"
    RUN "rips.py $SAMPLE --save --contours $SUB --lips $COLOR"
  done
done

RUN "rips.py $SAMPLE --save --graph"
RUN "rips.py $SAMPLE --save --graph --noim --barcode"
RUN "rips.py $SAMPLE --save --lips --noim --barcode"


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
