#!/bin/bash

#set -x #echo on

EXPERIMENT_NAME=data_preprocessing_k3

###################################
# 1. DATOS 1 
################################### 
INPUT_DATA_DIR=datos1

# 50s
WINDOW_SIZE=50
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step2_preprocess2_create_tfrecords_positives.py \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--clusters_file_path experiments/clusters_all_k3.json \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/K3/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/K3/tfrecords

python step2_preprocess2_create_tfrecords_positives.py \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--clusters_file_path experiments/clusters_all_k3.json \
--window_size $WINDOW_SIZE \
--component_N 0 \
--component_E 0 \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/K3/Z/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--window_size $WINDOW_SIZE \
--component_N 0 \
--component_E 0 \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/K3/Z/tfrecords

