#!/bin/bash

#./experiments/step1_preprocess1_get_windows.sh [preprocessing dir name] [WINDOW SIZE] [WINDOW STRIDE]
#./experiments/step1_preprocess1_get_windows.sh datos1 $1 $2
#./experiments/step1_preprocess1_get_windows.sh datos1 10

#set -x #echo on

DATA_PREP_MAIN_DIR_NAME=data_prep_$1
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$2

# EXTRACT WINDOWS

echo "python step1_preprocess1_get_windows.py \
--window_size $2 \
--raw_data_dir input/$1/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR"

python step1_preprocess1_get_windows.py \
--window_size $2 \
--window_stride $3 \
--raw_data_dir input/$1/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

