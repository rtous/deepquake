#!/bin/bash

#set -x #echo on

EXPERIMENT_NAME=data_preprocessing

###################################
# 3. DATOS 1 + DATOS 2 
###################################
INPUT_DATA_DIR=datos1_datos2

# 3.2 20s
WINDOW_SIZE=20
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

mkdir -p output/$DATA_PREP_DIR/mseed_event_windows
mkdir -p output/$DATA_PREP_DIR/mseed_noise
cp -r output/data_prep_datos1/$WINDOW_SIZE/mseed_event_windows output/$DATA_PREP_DIR
cp -r output/data_prep_datos1/$WINDOW_SIZE/mseed_noise output/$DATA_PREP_DIR
cp -r output/data_prep_datos2/$WINDOW_SIZE/mseed_event_windows output/$DATA_PREP_DIR  
cp -r output/data_prep_datos2/$WINDOW_SIZE/mseed_noise output/$DATA_PREP_DIR

python step2_preprocess2_create_tfrecords_positives.py \
--window_size $WINDOW_SIZE \
--component_N 0 \
--component_E 0 \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/Z/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--window_size $WINDOW_SIZE \
--component_N 0 \
--component_E 0 \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/Z/tfrecords

# 3.3 30s
WINDOW_SIZE=30
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

mkdir -p output/$DATA_PREP_DIR/mseed_event_windows
mkdir -p output/$DATA_PREP_DIR/mseed_noise
cp -r output/data_prep_datos1/$WINDOW_SIZE/mseed_event_windows output/$DATA_PREP_DIR
cp -r output/data_prep_datos1/$WINDOW_SIZE/mseed_noise output/$DATA_PREP_DIR
cp -r output/data_prep_datos2/$WINDOW_SIZE/mseed_event_windows output/$DATA_PREP_DIR  
cp -r output/data_prep_datos2/$WINDOW_SIZE/mseed_noise output/$DATA_PREP_DIR

python step2_preprocess2_create_tfrecords_positives.py \
--window_size $WINDOW_SIZE \
--component_N 0 \
--component_E 0 \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/Z/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--window_size $WINDOW_SIZE \
--component_N 0 \
--component_E 0 \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/Z/tfrecords

# 3.4 40s
WINDOW_SIZE=40
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

mkdir -p output/$DATA_PREP_DIR/mseed_event_windows
mkdir -p output/$DATA_PREP_DIR/mseed_noise
cp -r output/data_prep_datos1/$WINDOW_SIZE/mseed_event_windows output/$DATA_PREP_DIR
cp -r output/data_prep_datos1/$WINDOW_SIZE/mseed_noise output/$DATA_PREP_DIR
cp -r output/data_prep_datos2/$WINDOW_SIZE/mseed_event_windows output/$DATA_PREP_DIR  
cp -r output/data_prep_datos2/$WINDOW_SIZE/mseed_noise output/$DATA_PREP_DIR

python step2_preprocess2_create_tfrecords_positives.py \
--window_size $WINDOW_SIZE \
--component_N 0 \
--component_E 0 \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/Z/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--window_size $WINDOW_SIZE \
--component_N 0 \
--component_E 0 \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/Z/tfrecords

# 3.5 50s
WINDOW_SIZE=50
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

mkdir -p output/$DATA_PREP_DIR/mseed_event_windows
mkdir -p output/$DATA_PREP_DIR/mseed_noise
cp -r output/data_prep_datos1/$WINDOW_SIZE/mseed_event_windows output/$DATA_PREP_DIR
cp -r output/data_prep_datos1/$WINDOW_SIZE/mseed_noise output/$DATA_PREP_DIR
cp -r output/data_prep_datos2/$WINDOW_SIZE/mseed_event_windows output/$DATA_PREP_DIR  
cp -r output/data_prep_datos2/$WINDOW_SIZE/mseed_noise output/$DATA_PREP_DIR

python step2_preprocess2_create_tfrecords_positives.py \
--window_size $WINDOW_SIZE \
--component_N 0 \
--component_E 0 \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/Z/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--window_size $WINDOW_SIZE \
--component_N 0 \
--component_E 0 \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/Z/tfrecords

# 3.6 60s
WINDOW_SIZE=60
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

mkdir -p output/$DATA_PREP_DIR/mseed_event_windows
mkdir -p output/$DATA_PREP_DIR/mseed_noise
cp -r output/data_prep_datos1/$WINDOW_SIZE/mseed_event_windows output/$DATA_PREP_DIR
cp -r output/data_prep_datos1/$WINDOW_SIZE/mseed_noise output/$DATA_PREP_DIR
cp -r output/data_prep_datos2/$WINDOW_SIZE/mseed_event_windows output/$DATA_PREP_DIR  
cp -r output/data_prep_datos2/$WINDOW_SIZE/mseed_noise output/$DATA_PREP_DIR

python step2_preprocess2_create_tfrecords_positives.py \
--window_size $WINDOW_SIZE \
--component_N 0 \
--component_E 0 \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/Z/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--window_size $WINDOW_SIZE \
--component_N 0 \
--component_E 0 \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/Z/tfrecords

