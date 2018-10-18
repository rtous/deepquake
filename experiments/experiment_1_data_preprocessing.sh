#!/bin/bash

#set -x #echo on

EXPERIMENT_NAME=data_preprocessing

# 0. METADATA
python step0_preprocess0_metadata.py \
--input_path input/datos1/sfiles_nordicformat \
--output_path output/data_prep_datos1/catalog.json

python step0_preprocess0_metadata.py \
--input_path input/datos2/sfiles_nordicformat \
--output_path output/data_prep_datos2/catalog.json

###################################
# 1. DATOS 1 
################################### 
INPUT_DATA_DIR=datos1

# 1.1 10s
WINDOW_SIZE=10
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step1_preprocess1_get_windows.py \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

python step2_preprocess2_create_tfrecords_positives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

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

# 1.2 20s
WINDOW_SIZE=20
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step1_preprocess1_get_windows.py \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

python step2_preprocess2_create_tfrecords_positives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

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

# 1.3 30s
WINDOW_SIZE=30
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step1_preprocess1_get_windows.py \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

python step2_preprocess2_create_tfrecords_positives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

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

# 1.4 40s
WINDOW_SIZE=40
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step1_preprocess1_get_windows.py \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

python step2_preprocess2_create_tfrecords_positives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

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

# 1.5 50s
WINDOW_SIZE=50
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step1_preprocess1_get_windows.py \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

python step2_preprocess2_create_tfrecords_positives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

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

# 1.6 60s
WINDOW_SIZE=60
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step1_preprocess1_get_windows.py \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

python step2_preprocess2_create_tfrecords_positives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--window_size $WINDOW_SIZE \
--prep_data_dir output/$DATA_PREP_DIR \
--tfrecords_dir output/$DATA_PREP_DIR/tfrecords

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


###################################
# 2. DATOS 2 
###################################
INPUT_DATA_DIR=datos2

# 2.1 10s
WINDOW_SIZE=10
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step1_preprocess1_get_windows.py \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

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

# 2.2 20s
WINDOW_SIZE=20
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step1_preprocess1_get_windows.py \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

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

# 2.3 30s
WINDOW_SIZE=30
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step1_preprocess1_get_windows.py \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

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

# 2.4 40s
WINDOW_SIZE=40
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step1_preprocess1_get_windows.py \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

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

# 2.5 50s
WINDOW_SIZE=50
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step1_preprocess1_get_windows.py \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

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

# 2.6 60s
WINDOW_SIZE=60
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE

python step1_preprocess1_get_windows.py \
--window_size $WINDOW_SIZE \
--raw_data_dir input/$INPUT_DATA_DIR/mseed \
--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
--prep_data_dir output/$DATA_PREP_DIR

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

###################################
# 3. DATOS 1 + DATOS 2 
###################################
INPUT_DATA_DIR=datos1_datos2

# 3.1 10s
WINDOW_SIZE=10
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

