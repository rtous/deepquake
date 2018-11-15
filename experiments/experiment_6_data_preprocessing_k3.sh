#!/bin/bash

#set -x #echo on

EXPERIMENT_NAME=data_preprocessing_clusters

###################################
# 1. DATOS 1 
################################### 
INPUT_DATA_DIR=datos1

# 1.1 10s
WINDOW_SIZE=10
DATA_PREP_MAIN_DIR_NAME=data_prep_k3_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step1_preprocess1_get_windows.py \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

python step2_preprocess2_create_tfrecords_positives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

