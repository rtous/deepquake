python step0_preprocess0_metadata.py \
--input_path input/datos1/sfiles_nordicformat \
--output_path output/data_prep_datos1/catalog.json

python step0_preprocess0_metadata.py \
--input_path input/datos2/sfiles_nordicformat \
--output_path output/data_prep_datos2/catalog.json

python step1_preprocess1_get_windows.py \
--debug 1 \
--window_size 10 \
--raw_data_dir input/datos1/mseed \
--catalog_path output/data_prep_datos1/catalog.json \
--prep_data_dir output/data_prep_test1/10 \
--station CRUV

python step1_preprocess1_get_windows.py \
--debug 1 \
--window_size 50 \
--raw_data_dir input/datos1/mseed \
--catalog_path output/data_prep_datos1/catalog.json \
--prep_data_dir output/data_prep_test1/50 \
--station CRUV

python step1_preprocess1_get_windows.py \
--debug 1 \
--window_size 10 \
--raw_data_dir input/datos2/mseed \
--catalog_path output/data_prep_datos2/catalog.json \
--prep_data_dir output/data_prep_test2/10 \
--station BAUV

python step1_preprocess1_get_windows.py \
--debug 1 \
--window_size 50 \
--raw_data_dir input/datos2/mseed \
--catalog_path output/data_prep_datos2/catalog.json \
--prep_data_dir output/data_prep_test2/50 \
--station BAUV

./experiments/step1_preprocess2_join_dirs.sh test1 test2 10
./experiments/step1_preprocess2_join_dirs.sh test1 test2 50

#DATOS 1

./experiments/step1_preprocess3_tfrecords.sh test1 10 2 3
./experiments/step1_preprocess3_tfrecords.sh test1 50 2 3 

./experiments/step1_preprocess3_tfrecords.sh test1 10 2 1
./experiments/step1_preprocess3_tfrecords.sh test1 50 2 1 

./experiments/step2_train.sh test1 10 2 3 model1 experiments/config_test.ini
./experiments/step2_train.sh test1 50 2 3 model1 experiments/config_test.ini

./experiments/step2_train.sh test1 10 2 1 model1 experiments/config_test.ini
./experiments/step2_train.sh test1 50 2 1 model1 experiments/config_test.ini

#DATOS 2

./experiments/step1_preprocess3_tfrecords.sh test2 10 2 1
./experiments/step1_preprocess3_tfrecords.sh test2 50 2 1 

./experiments/step2_train.sh test2 10 2 1 model1 experiments/config_test.ini
./experiments/step2_train.sh test2 50 2 1 model1 experiments/config_test.ini

#DATOS 1 + DATOS 2

./experiments/step1_preprocess3_tfrecords.sh test1_test2 10 2 1
./experiments/step1_preprocess3_tfrecords.sh test1_test2 50 2 1 

./experiments/step2_train.sh test1_test2 10 2 1 model1 experiments/config_test.ini
./experiments/step2_train.sh test1_test2 50 2 1 model1 experiments/config_test.ini
