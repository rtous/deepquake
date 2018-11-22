python step0_preprocess0_metadata.py \
--input_path input/datos1/sfiles_nordicformat \
--output_path output/data_prep_test1/catalog.json

python step0_preprocess0_metadata.py \
--input_path input/datos2/sfiles_nordicformat \
--output_path output/data_prep_test2/catalog.json

python step1_preprocess1_get_windows.py \
--debug 1 \
--window_size 10 \
--raw_data_dir input/datos1/mseed \
--catalog_path output/data_prep_test1/catalog.json \
--prep_data_dir output/data_prep_test1/10 \
--station CRUV

python step1_preprocess1_get_windows.py \
--debug 1 \
--window_size 50 \
--raw_data_dir input/datos1/mseed \
--catalog_path output/data_prep_test1/catalog.json \
--prep_data_dir output/data_prep_test1/50 \
--station CRUV

python step1_preprocess1_get_windows.py \
--debug 1 \
--window_size 10 \
--raw_data_dir input/datos2/mseed \
--catalog_path output/data_prep_test2/catalog.json \
--prep_data_dir output/data_prep_test2/10 \
--station BAUV

python step1_preprocess1_get_windows.py \
--debug 1 \
--window_size 50 \
--raw_data_dir input/datos2/mseed \
--catalog_path output/data_prep_test2/catalog.json \
--prep_data_dir output/data_prep_test2/50 \
--station BAUV

./scripts/step1_preprocess1bis_join_dirs.sh test1 test2 10
./scripts/step1_preprocess1bis_join_dirs.sh test1 test2 50

#DATOS 1

./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test1 10 2 3
./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test1 10 4 3 experiments/clusters_all_k3.json
./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test1 50 2 3 
./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test1 50 4 3 experiments/clusters_all_k3.json

./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test1 10 2 1
./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test1 10 4 1 experiments/clusters_all_k3.json
./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test1 50 2 1 
./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test1 50 4 1 experiments/clusters_all_k3.json

./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 10 2 3 model1 experiments/config_test_model1.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 10 4 3 model1 experiments/config_test_model1.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 50 2 3 model1 experiments/config_test_model1.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 50 4 3 model1 experiments/config_test_model1.ini

./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 10 2 1 model1 experiments/config_test_model1.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 10 4 1 model1 experiments/config_test_model1.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 50 2 1 model1 experiments/config_test_model1.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1 50 4 1 model1 experiments/config_test_model1.ini

#DATOS 2

./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test2 10 2 1
./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test2 10 4 1 experiments/clusters_all_k3.json
./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test2 50 2 1 
./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test2 50 4 1 experiments/clusters_all_k3.json

./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test2 10 2 1 model1 experiments/config_test_model1.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test2 10 4 1 model1 experiments/config_test_model1.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test2 50 2 1 model1 experiments/config_test_model1.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test2 50 4 1 model1 experiments/config_test_model1.ini

#DATOS 1 + DATOS 2

./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test1_test2 10 2 1
./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test1_test2 10 4 1
./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test1_test2 50 2 1 
./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test1_test2 50 4 1 

./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1_test2 10 2 1 model1 experiments/config_test_model1.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1_test2 10 4 1 model1 experiments/config_test_model1.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1_test2 50 2 1 model1 experiments/config_test_model1.ini
./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test1_test2 50 4 1 model1 experiments/config_test_model1.ini