#!/bin/bash

EXPERIMENT_NAME=50s_olddata_oldmodel_eval_newdata
INPUT_DATA_DIR=datos1

CONFIG_FILE=experiments/config_50s.ini
DATA_PREP_DIR=data_prep_50s
DATA_TRAIN_DIR=train_50s_olddata_oldmodel

python step5_eval_over_tfrecords.py \
--config_file_path $CONFIG_FILE \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
--output_dir output/$DATA_TRAIN_DIR/eval \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test