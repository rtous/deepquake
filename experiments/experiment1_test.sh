python step1_preprocess1_funvisis2oklahoma.py \
--config_file_path experiments/config_test.ini \
--raw_data_dir input/data_raw_default/mseed \
--raw_metadata_dir input/data_raw_default/sfiles_nordicformat \
--prep_data_dir output/data_prep_test \
--pattern 05-0420-00L* \
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

python step5_eval.py \
--stream_path output/data_prep_test/mseed \
--config_file_path experiments/config_test.ini \
--checkpoint_dir output/train_test/checkpoints \
--output_dir output/train_test/eval
