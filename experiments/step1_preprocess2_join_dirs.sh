#!/bin/bash

#./experiments/step1_preprocess2_join_dirs.sh [preprocessing dir name 1] [preprocessing dir name 2] [WINDOW SIZE]
#./experiments/step1_preprocess2_join_dirs.sh $1 $2
#./experiments/step1_preprocess2_join_dirs.sh datos1 datos2

#set -x #echo on

INPUT_DATA_DIR=$1_$2

DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$3

mkdir -p output/$DATA_PREP_DIR/mseed_event_windows
mkdir -p output/$DATA_PREP_DIR/mseed_noise
cp -r output/data_prep_$1/$3/mseed_event_windows output/$DATA_PREP_DIR
cp -r output/data_prep_$1/$3/mseed_noise output/$DATA_PREP_DIR
cp -r output/data_prep_$2/$3/mseed_event_windows output/$DATA_PREP_DIR  
cp -r output/data_prep_$2/$3/mseed_noise output/$DATA_PREP_DIR

