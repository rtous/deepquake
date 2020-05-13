#!/bin/bash

#./experiments/step0_metadata.sh [preprocessing dir name]

DATA_PREP_MAIN_DIR_NAME=data_prep_$1

echo "python step0_preprocess0_metadata.py \
--input_path input/$DATA_PREP_MAIN_DIR_NAME/sfiles_nordicformat \
--output_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json"

python step0_preprocess0_metadata.py \
--input_path input/$1/sfiles_nordicformat \
--output_path output/$DATA_PREP_MAIN_DIR_NAME/catalog.json

#python step0_preprocess0_metadata.py \
#--input_path input/datos1/sfiles_nordicformat \
#--output_path output/data_prep_datos1/catalog.json

#python step0_preprocess0_metadata.py \
#--input_path input/datos2/sfiles_nordicformat \
#--output_path output/data_prep_datos2/catalog.json

#python step0_preprocess0_metadata.py \
#--input_path input/datos3/sfiles_nordicformat \
#--output_path output/data_prep_datos3/catalog.json

#python step0_preprocess0_metadata.py \
#--input_path input/datos1/sfiles_nordicformat input/datos2/sfiles_nordicformat \
#--output_path output/data_prep_datos1_datos2/catalog.json

#python step0_preprocess0_metadata.py \
#--input_path input/datos1/sfiles_nordicformat input/datos2/sfiles_nordicformat  input/datos3/sfiles_nordicformat \
#--output_path output/data_prep_datos1_datos2_datos3/catalog.json