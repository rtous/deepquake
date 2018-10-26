#!/bin/bash

EXPERIMENT_NAME=test
INPUT_DATA_DIR=datos1

#CONFIG_FILE=experiments/config_$EXPERIMENT_NAME.ini
CONFIG_FILE=experiments/config_model2b.ini
DATA_PREP_DIR=data_prep_$EXPERIMENT_NAME
DATA_TRAIN_DIR=train_$EXPERIMENT_NAME
WINDOW_SIZE=50

python step4_train.py \
--window_size $WINDOW_SIZE \
--debug 1 \
--config_file_path $CONFIG_FILE \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints

python step5_eval_over_tfrecords.py \
--window_size $WINDOW_SIZE \
--debug 1 \
--config_file_path $CONFIG_FILE \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
--output_dir output/$DATA_TRAIN_DIR/eval \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test
