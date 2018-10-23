#!/bin/bash

TRAIN_CONFIG=train_model2a
CONFIG_FILE=experiments/config_model2a.ini

###################################
# 1. DATOS 1 
################################### 
INPUT_DATA_DIR=datos1

# 50s
WINDOW_SIZE=50
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE/Z
DATA_TRAIN_DIR=$DATA_PREP_DIR/$TRAIN_CONFIG

python step4_train.py \
--config_file_path $CONFIG_FILE \
--window_size $WINDOW_SIZE \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints

python step5_eval_over_tfrecords.py \
--config_file_path $CONFIG_FILE \
--window_size $WINDOW_SIZE \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
--output_dir output/$DATA_TRAIN_DIR/eval \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test

