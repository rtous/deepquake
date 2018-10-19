#!/bin/bash

EXPERIMENT_NAME=50s_Z_datos2_model2d
INPUT_DATA_DIR=datos2

CONFIG_FILE=experiments/config_$EXPERIMENT_NAME.ini
DATA_PREP_DIR=data_prep_50s_Z_datos2
DATA_TRAIN_DIR=train_$EXPERIMENT_NAME

python step4_train.py \
--config_file_path $CONFIG_FILE \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints

python step5_eval_over_tfrecords.py \
--config_file_path $CONFIG_FILE \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
--output_dir output/$DATA_TRAIN_DIR/eval \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test