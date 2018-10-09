python step0_preprocess0_metadata.py \
--input_path input/datos1/sfiles_nordicformat \
--output_path output/data_prep_test/catalog.json

python step1_preprocess1_get_windows.py \
--config_file_path experiments/config_test.ini \
--raw_data_dir input/datos1/mseed \
--catalog_path output/data_prep_test/catalog.json \
--prep_data_dir output/data_prep_test \
--pattern 2015-02-05-0420* \
--station CRUV

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_test.ini \
--prep_data_dir output/data_prep_test \
--tfrecords_dir output/data_prep_test/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_test.ini \
--prep_data_dir output/data_prep_test \
--tfrecords_dir output/data_prep_test/tfrecords

python step4_train.py \
--config_file_path experiments/config_test.ini \
--tfrecords_dir output/data_prep_test/tfrecords \
--checkpoint_dir output/train_test/checkpoints

python step5_eval_over_tfrecords.py \
--config_file_path experiments/config_test.ini \
--checkpoint_dir output/train_test/checkpoints \
--output_dir output/train_test/eval \
--tfrecords_dir output/data_prep_test/tfrecords/test
