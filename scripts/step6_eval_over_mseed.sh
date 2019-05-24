#!/bin/bash

#./experiments/train.sh [preprocessing dir name] [WINDOW SIZE] [CLUSTERS + 1] [COMPONENTS 1 or 3] [train label] [config_file] [stream_path] [catalog_path]
#./experiments/train.sh $1 $2 $3 $4 $5 $6 $7 $8
#./experiments/step6_eval_over_mseed.sh test1 50 2 1 model2 experiments/config_model2.ini output/data_prep_test1/50/mseed output/data_prep_test1/catalog.json

TRAIN_CONFIG=$5
CONFIG_FILE=$6
INPUT_DATA_DIR=$1
WINDOW_SIZE=$2
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE/CL$3/CO$4
DATA_TRAIN_DIR=$DATA_PREP_DIR/$TRAIN_CONFIG

if [ "$4" = "3" ]; then
	echo "python step6_eval_over_mseed.py \
	--config_file_path $CONFIG_FILE \
	--n_clusters $3 \
	--window_size $WINDOW_SIZE \
	--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
	--output_dir output/$DATA_TRAIN_DIR/eval \
	--catalog_path $8 \
	--stream_path $7"

	python step6_eval_over_mseed.py \
	--config_file_path $CONFIG_FILE \
	--n_clusters $3 \
	--window_size $WINDOW_SIZE \
	--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
	--output_dir output/$DATA_TRAIN_DIR/eval \
	--catalog_path $8 \
	--stream_path $7
else
	echo "python step6_eval_over_mseed.py \
	--config_file_path $CONFIG_FILE \
	--component_N 0 \
	--component_E 0 \
	--n_clusters $3 \
	--window_size $WINDOW_SIZE \
	--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
	--output_dir output/$DATA_TRAIN_DIR/eval \
	--catalog_path $8 \
	--stream_path $7"

	python step6_eval_over_mseed.py \
	--config_file_path $CONFIG_FILE \
	--component_N 0 \
	--component_E 0 \
	--n_clusters $3 \
	--window_size $WINDOW_SIZE \
	--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
	--output_dir output/$DATA_TRAIN_DIR/eval \
	--catalog_path $8 \
	--stream_path $7
fi

