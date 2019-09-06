#!/bin/bash

# AQUEST SCRIPT NOMÉS L'HE FET PER PODER USAR UN MODEL JA ENTRENAT SOBRE UN ALTRE DATASET
# PER AIXO AFEGEIXO EL DARRER PARAMETRE QUE ES UNA RUTA COMPLERTA

#./experiments/train.sh [preprocessing dir name] [WINDOW SIZE] [CLUSTERS + 1] [COMPONENTS 1 or 3] [train label] [config_file] [checkpoint_dir]
#./experiments/train.sh $1 $2 $3 $4 $5 $6 
#./experiments/train.sh datos1 10 2 3 model1 config_default.ini
#./experiments/train.sh datos1 10 2 3 model2 experiments/config_model2b.ini
#./experiments/train.sh datos2 10 2 1 model1 config_default.ini
#./experiments/train.sh datos1 10 4 3 model1 config_default.ini
#./experiments/train.sh datos1_datos2_datos3 10 4 1 model1 config_default.ini

TRAIN_CONFIG=$5
CONFIG_FILE=$6
INPUT_DATA_DIR=$1
WINDOW_SIZE=$2
DATA_PREP_MAIN_DIR_NAME=data_prep_$INPUT_DATA_DIR
DATA_PREP_DIR=$DATA_PREP_MAIN_DIR_NAME/$WINDOW_SIZE/CL$3/CO$4
DATA_TRAIN_DIR=$DATA_PREP_DIR/$TRAIN_CONFIG
CHECKPOINT_DIR=$7

if [ "$4" = "3" ]; then

	echo "python step5_eval_over_tfrecords.py \
	--config_file_path $CONFIG_FILE \
	--n_clusters $3 \
	--window_size $WINDOW_SIZE \
	--checkpoint_dir $CHECKPOINT_DIR \
	--output_dir output/$DATA_TRAIN_DIR/eval \
	--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test"

	python step5_eval_over_tfrecords.py \
	--config_file_path $CONFIG_FILE \
	--n_clusters $3 \
	--window_size $WINDOW_SIZE \
	--checkpoint_dir $CHECKPOINT_DIR \
	--output_dir output/$DATA_TRAIN_DIR/eval \
	--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test
else

	echo "python step5_eval_over_tfrecords.py \
	--config_file_path $CONFIG_FILE \
	--component_N 0 \
	--component_E 0 \
	--n_clusters $3 \
	--window_size $WINDOW_SIZE \
	--checkpoint_dir $CHECKPOINT_DIR \
	--output_dir output/$DATA_TRAIN_DIR/eval \
	--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test"

	python step5_eval_over_tfrecords.py \
	--config_file_path $CONFIG_FILE \
	--component_N 0 \
	--component_E 0 \
	--n_clusters $3 \
	--window_size $WINDOW_SIZE \
	--checkpoint_dir $CHECKPOINT_DIR \
	--output_dir output/$DATA_TRAIN_DIR/eval \
	--tfrecords_dir output/$DATA_PREP_DIR/tfrecords/test
fi

