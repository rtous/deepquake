python step1_preprocess1_funvisis2oklahoma.py \
--config_file_path experiments/config_50s_Z.ini \
--raw_data_dir input/data_raw_default/mseed \
--raw_metadata_dir input/data_raw_default/sfiles_nordicformat \
--prep_data_dir output/data_prep_50s_Z \

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_50s_Z.ini \
--prep_data_dir output/data_prep_50s_Z \
--tfrecords_dir output/data_prep_50s_Z/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_50s_Z.ini \
--prep_data_dir output/data_prep_50s_Z \
--tfrecords_dir output/data_prep_50s_Z/tfrecords

python step4_train.py \
--config_file_path experiments/config_50s_Z.ini \
--tfrecords_dir output/data_prep_50s_Z/tfrecords \
--checkpoint_dir output/train_50s_Z/checkpoints

python step5_eval_over_tfrecords.py \
--config_file_path experiments/config_50s_Z.ini \
--checkpoint_dir output/train_50s_Z/checkpoints \
--output_dir output/train_50s_Z/eval \
--tfrecords_dir output/data_prep_50s_Z/tfrecords/test

