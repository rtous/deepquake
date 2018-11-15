#!/bin/bash

#set -x #echo on

EXPERIMENT_NAME=data_preprocessing

python step0_preprocess0_metadata.py \
--input_path input/datos1/sfiles_nordicformat \
--output_path output/data_prep_datos1/catalog.json

python step0_preprocess0_metadata.py \
--input_path input/datos2/sfiles_nordicformat \
--output_path output/data_prep_datos2/catalog.json

python step0_preprocess0_metadata.py \
--input_path input/datos3/sfiles_nordicformat \
--output_path output/data_prep_datos3/catalog.json

