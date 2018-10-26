#!/bin/bash

EXPERIMENT_NAME=test
INPUT_DATA_DIR=datos1


CONFIG_FILE=experiments/config_$EXPERIMENT_NAME.ini
#CONFIG_FILE=experiments/config_model2b.ini
DATA_PREP_DIR=data_prep_$EXPERIMENT_NAME
DATA_TRAIN_DIR=train_$EXPERIMENT_NAME
WINDOW_SIZE=50

python step0_preprocess0_metadata.py \
--input_path input/$INPUT_DATA_DIR/sfiles_nordicformat \
--output_path output/$DATA_PREP_DIR/catalog.json

python step1_preprocess1_get_windows.py \
--debug 1 \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_DIR/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR \
--station CRUV

python step2_preprocess2_create_tfrecords_positives.py \
--debug 1 \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--debug 1 \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

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
