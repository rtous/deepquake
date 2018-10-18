#!/bin/bash

TRAIN_CONFIG=train_default

###################################
# 1. DATOS 1 
################################### 
INPUT_DATA_DIR=datos1

# 40s
WINDOW_SIZE=40
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE
DATA_TRAIN_DIR=$DATA_PREP_DIR/$TRAIN_CONFIG

python step4_train.py \
--window_size $WINDOW_SIZE \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints

python step5_eval_over_tfrecords.py \
--window_size $WINDOW_SIZE \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
--output_dir output/$DATA_TRAIN_DIR/eval \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test
