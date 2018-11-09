#!/bin/bash

TRAIN_CONFIG=train_default

###################################
# 1. DATOS 3 
################################### 
INPUT_DATA_DIR=datos3

# 40s
WINDOW_SIZE=40
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE
DATA_TRAIN_DIR=$DATA_PREP_DIR/$TRAIN_CONFIG

python step4_train.py \
--component_N 0 \
--component_E 0 \
--window_size $WINDOW_SIZE \
--tfrecords_dir output/$DATA_PREP_DIR/Z/tfrecords \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints

python step5_eval_over_tfrecords.py \
--component_N 0 \
--component_E 0 \
--window_size $WINDOW_SIZE \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
--output_dir output/$DATA_TRAIN_DIR/eval \
--tfrecords_dir output/$DATA_PREP_DIR/Z/tfrecords/test

