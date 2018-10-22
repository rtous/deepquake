#!/bin/bash

TRAIN_CONFIG=train_default
CONFIG_FILE=experiments/config_model2a.ini

###################################
# 1. DATOS 2 
################################### 
INPUT_DATA_DIR=datos1_datos2

# 50s
WINDOW_SIZE=50
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE
DATA_TRAIN_DIR=$DATA_PREP_DIR/$TRAIN_CONFIG

python step5_eval_over_tfrecords.py \
--config_file_path $CONFIG_FILE \
--component_N 0 \
--component_E 0 \
--window_size $WINDOW_SIZE \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
--output_dir output/$DATA_TRAIN_DIR/eval_overdatos2 \
--tfrecords_dir output/$data_prep_datos2/Z/tfrecords/test

