python step0_preprocess0_metadata.py \
--input_path input/datos1/sfiles_nordicformat \
--output_path output/data_prep_test/catalog.json

python step1_preprocess1_get_windows.py \
--debug 1 \
--window_size 10 \
--raw_data_dir input/datos1/mseed \
--catalog_path output/data_prep_test/catalog.json \
--prep_data_dir output/data_prep_test/10 \
--station CRUV

./scripts/step2_and_3_preprocess2_and_3_create_tfrecords.sh test 10 2 3

./scripts/step4_and_5_train_and_eval_over_tfrecords.sh test 10 2 3 model1 experiments/config_test_model1.ini
