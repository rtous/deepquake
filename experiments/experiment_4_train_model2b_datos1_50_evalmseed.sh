#!/bin/bash

TRAIN_CONFIG=train_model2b
CONFIG_FILE=experiments/config_model2b.ini

###################################
# 1. DATOS 1 
################################### 
INPUT_DATA_DIR=datos1

# 50s
WINDOW_SIZE=50
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE
DATA_TRAIN_DIR=$DATA_PREP_DIR/$TRAIN_CONFIG

python step6_eval_over_mseed.py \
--config_file_path $CONFIG_FILE \
--window_size $WINDOW_SIZE \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
--output_dir output/$DATA_TRAIN_DIR/evalmseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--stream_path output/$DATA_PREP_DIR/mseed

