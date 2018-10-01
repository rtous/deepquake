python step1_preprocess1_funvisis2oklahoma.py \
--config_file_path experiments/config_30s.ini \
--raw_data_dir input/data_raw_default/mseed \
--raw_metadata_dir input/data_raw_default/sfiles_nordicformat \
--prep_data_dir output/data_prep_30s \

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_30s.ini \
--prep_data_dir output/data_prep_30s \
--tfrecords_dir output/data_prep_30s/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_30s.ini \
--prep_data_dir output/data_prep_30s \
--tfrecords_dir output/data_prep_30s/tfrecords

python step4_train.py \
--config_file_path experiments/config_30s.ini \
--tfrecords_dir output/data_prep_30s/tfrecords \
--checkpoint_dir output/train_30s/checkpoints

python step5_eval.py \
--stream_path output/data_prep_experiment3_30s/mseed \
--config_file_path experiments/config_30s.ini \
--checkpoint_dir output/train_30s/checkpoints \
--output_dir output/train_30s/eval

