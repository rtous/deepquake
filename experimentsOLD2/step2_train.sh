#!/bin/bash

#./experiments/train.sh [preprocessing dir name] [WINDOW SIZE] [CLUSTERS + 1] [COMPONENTS 1 or 3]
#./experiments/train.sh $1 $2 $3 $4 
#./experiments/train.sh datos1 10 2 3
#./experiments/train.sh datos2 10 2 1
#./experiments/train.sh datos1 10 4 3
#./experiments/train.sh datos1_datos2_datos3 10 4 1


TRAIN_CONFIG=train_default

INPUT_DATA_DIR=$1

WINDOW_SIZE=$2
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE/CL$3/CO$4
DATA_TRAIN_DIR=$DATA_PREP_DIR/$TRAIN_CONFIG

if [ "$4" = "3" ]
then
	echo "python step4_train.py \
	--n_clusters 4 \
	--window_size $WINDOW_SIZE \
	--tfrecords_dir output/$DATA_PREP_DIR/tfrecords \
	--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints"

	python step4_train.py \
	--n_clusters 4 \
	--window_size $WINDOW_SIZE \
	--tfrecords_dir output/$DATA_PREP_DIR/tfrecords \
	--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints

	echo "python step5_eval_over_tfrecords.py \
	--n_clusters 4 \
	--window_size $WINDOW_SIZE \
	--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
	--output_dir output/$DATA_TRAIN_DIR/eval \
	--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test"

	python step5_eval_over_tfrecords.py \
	--n_clusters 4 \
	--window_size $WINDOW_SIZE \
	--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
	--output_dir output/$DATA_TRAIN_DIR/eval \
	--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test
else

	echo "python step4_train.py \
	--component_N 0 \
	--component_E 0 \
	--n_clusters 4 \
	--window_size $WINDOW_SIZE \
	--tfrecords_dir output/$DATA_PREP_DIR/tfrecords \
	--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints"

    python step4_train.py \
	--component_N 0 \
	--component_E 0 \
	--n_clusters 4 \
	--window_size $WINDOW_SIZE \
	--tfrecords_dir output/$DATA_PREP_DIR/tfrecords \
	--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints

	echo "python step5_eval_over_tfrecords.py \
	--component_N 0 \
	--component_E 0 \
	--n_clusters 4 \
	--window_size $WINDOW_SIZE \
	--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
	--output_dir output/$DATA_TRAIN_DIR/eval \
	--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test"

	python step5_eval_over_tfrecords.py \
	--component_N 0 \
	--component_E 0 \
	--n_clusters 4 \
	--window_size $WINDOW_SIZE \
	--checkpoint_dir output/$DATA_TRAIN_DIR/checkpoints \
	--output_dir output/$DATA_TRAIN_DIR/eval \
	--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test
fi

