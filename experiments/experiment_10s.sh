python step1_preprocess1_funvisis2oklahoma.py \
--config_file_path experiments/config_10s.ini \
--raw_data_dir input/data_raw_default/mseed \
--raw_metadata_dir input/data_raw_default/sfiles_nordicformat \
--prep_data_dir output/data_prep_10s \

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_10s.ini \
--prep_data_dir output/data_prep_10s \
--tfrecords_dir output/data_prep_10s/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_10s.ini \
--prep_data_dir output/data_prep_10s \
--tfrecords_dir output/data_prep_10s/tfrecords

python step4_train.py \
--config_file_path experiments/config_10s.ini \
--tfrecords_dir output/data_prep_10s/tfrecords \
--checkpoint_dir output/train_10s/checkpoints

python step5_eval_over_tfrecords.py \
--config_file_path experiments/config_10s.ini \
--checkpoint_dir output/train_10s/checkpoints \
--output_dir output/train_10s/eval \
--tfrecords_dir output/data_prep_10s/tfrecords/test

