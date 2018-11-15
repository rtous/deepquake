#!/bin/bash

#set -x #echo on

EXPERIMENT_NAME=data_preprocessing_k3

# 0. METADATA
python step0_preprocess0_metadata.py \
--input_path input/datos1/sfiles_nordicformat \
--output_path output/data_prep_k3_datos1/catalog.json

python step0_preprocess0_metadata.py \
--input_path input/datos2/sfiles_nordicformat \
--output_path output/data_prep_k3_datos2/catalog.json

python step0_preprocess0_metadata.py \
--input_path input/datos3/sfiles_nordicformat \
--output_path output/data_prep_k3_datos3/catalog.json

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

