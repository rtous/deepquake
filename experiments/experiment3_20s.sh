python step1_preprocess1_funvisis2oklahoma.py \
--config_file_path experiments/config_20s.ini \
--raw_data_dir input/data_raw_default/mseed \
--raw_metadata_dir input/data_raw_default/sfiles_nordicformat \
--prep_data_dir output/data_prep_experiment3_20s \

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_20s.ini \
--prep_data_dir output/data_prep_experiment3_20s \
--tfrecords_dir output/data_prep_experiment3_20s/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_20s.ini \
--prep_data_dir output/data_prep_experiment3_20s \
--tfrecords_dir output/data_prep_experiment3_20s/tfrecords

python step4_train.py \
--config_file_path experiments/config_20s.ini \
--tfrecords_dir output/data_prep_experiment3_20s/tfrecords \
--checkpoint_dir output/train_experiment3_20s/checkpoints

python step5_eval.py \
--stream_path output/data_prep_experiment3_20s/mseed \
--config_file_path experiments/config_20s.ini \
--checkpoint_dir output/train_experiment3_20s/checkpoints \
--output_dir output/train_experiment3_20s/eval

