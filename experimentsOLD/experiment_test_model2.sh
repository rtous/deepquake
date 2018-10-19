#!/bin/bash

EXPERIMENT_NAME=test_model2
INPUT_DATA_DIR=datos1

CONFIG_FILE=experiments/config_$EXPERIMENT_NAME.ini
DATA_PREP_DIR=data_prep_$EXPERIMENT_NAME
DATA_TRAIN_DIR=train_$EXPERIMENT_NAME

python step0_preprocess0_metadata.py \
--input_path input/$INPUT_DATA_DIR/sfiles_nordicformat \
--output_path output/$DATA_PREP_DIR/catalog.json

python step1_preprocess1_get_windows.py \
--config_file_path $CONFIG_FILE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_DIR/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR \
--pattern 2015-02-05-0420* \
--station CRUV

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path $CONFIG_FILE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path $CONFIG_FILE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

python step4_train.py \
--config_file_path $CONFIG_FILE \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints

python step5_eval_over_tfrecords.py \
--config_file_path $CONFIG_FILE \
--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
--output_dir output/$DATA_TRAIN_DIR/eval \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test
