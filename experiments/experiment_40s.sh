python step1_preprocess1_funvisis2oklahoma.py \
--config_file_path experiments/config_40s.ini \
--raw_data_dir input/data_raw_default/mseed \
--raw_metadata_dir input/data_raw_default/sfiles_nordicformat \
--prep_data_dir output/data_prep_40s \

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_40s.ini \
--prep_data_dir output/data_prep_40s \
--tfrecords_dir output/data_prep_40s/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_40s.ini \
--prep_data_dir output/data_prep_40s \
--tfrecords_dir output/data_prep_40s/tfrecords

python step4_train.py \
--config_file_path experiments/config_40s.ini \
--tfrecords_dir output/data_prep_40s/tfrecords \
--checkpoint_dir output/train_40s/checkpoints

python step5_eval_over_tfrecords.py \
--stream_path output/data_prep_40s/mseed \
--config_file_path experiments/config_40s.ini \
--checkpoint_dir output/train_40s/checkpoints \
--output_dir output/train_40s/eval \
--tfrecords_dir output/data_prep_40s/tfrecords/test

