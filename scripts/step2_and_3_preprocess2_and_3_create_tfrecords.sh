#!/bin/bash

#./experiments/train.sh [preprocessing dir name] [WINDOW SIZE] [CLUSTERS + 1] [COMPONENTS 1 or 3] [clusters_file_path]
#./experiments/train.sh $1 $2 $3 $4 $5
#./experiments/train.sh datos1 10 2 3
#./experiments/train.sh datos2 10 2 1
#./experiments/train.sh datos1 10 4 3 experiments/clusters_all_k3.json
#./experiments/train.sh datos1_datos2_datos3 10 4 1 experiments/clusters_all_k3.json

#set -x #echo on

INPUT_DATA_DIR=$1

WINDOW_SIZE=$2
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE
TFRECORDS_DIR=$DATA_PREP_DIR/CL$3/CO$4/tfrecords
if [ $# -eq 4 ]; then
	if [ "$4" = "1" ]; then
		python step2_preprocess2_create_tfrecords_positives.py \
		--window_size $WINDOW_SIZE \
		--component_N 0 \
		--component_E 0 \
		--prep_data_dir output/$DATA_PREP_DIR \
		--tfrecords_dir output/$TFRECORDS_DIR

		python step3_preprocess3_create_tfrecords_negatives.py \
		--window_size $WINDOW_SIZE \
		--component_N 0 \
		--component_E 0 \
		--prep_data_dir output/$DATA_PREP_DIR \
		--tfrecords_dir output/$TFRECORDS_DIR
	elif [ "$4" = "3" ]; then
		python step2_preprocess2_create_tfrecords_positives.py \
		--window_size $WINDOW_SIZE \
		--prep_data_dir output/$DATA_PREP_DIR \
		--tfrecords_dir output/$TFRECORDS_DIR

		python step3_preprocess3_create_tfrecords_negatives.py \
		--window_size $WINDOW_SIZE \
		--prep_data_dir output/$DATA_PREP_DIR \
		--tfrecords_dir output/$TFRECORDS_DIR		
	else
		echo 'Wrong number of components'
	    exit 1
	fi
elif [ $# -eq 5 ]; then
	if [ "$4" = "1" ]; then
		python step2_preprocess2_create_tfrecords_positives.py \
		--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
		--clusters_file_path $5 \
		--window_size $WINDOW_SIZE \
		--component_N 0 \
		--component_E 0 \
		--prep_data_dir output/$DATA_PREP_DIR \
		--tfrecords_dir output/$TFRECORDS_DIR

		python step3_preprocess3_create_tfrecords_negatives.py \
		--window_size $WINDOW_SIZE \
		--component_N 0 \
		--component_E 0 \
		--prep_data_dir output/$DATA_PREP_DIR \
		--tfrecords_dir output/$TFRECORDS_DIR
	elif [ "$4" = "3" ]; then
		python step2_preprocess2_create_tfrecords_positives.py \
		--catalog_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json \
		--clusters_file_path $5 \
		--window_size $WINDOW_SIZE \
		--prep_data_dir output/$DATA_PREP_DIR \
		--tfrecords_dir output/$TFRECORDS_DIR

		python step3_preprocess3_create_tfrecords_negatives.py \
		--window_size $WINDOW_SIZE \
		--prep_data_dir output/$DATA_PREP_DIR \
		--tfrecords_dir output/$TFRECORDS_DIR	
	else
		echo 'Wrong number of components'	
		exit 1
	fi
else
	echo 'Wrong number of input params'
    exit 1
fi

