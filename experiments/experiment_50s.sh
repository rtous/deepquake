python step0_preprocess0_metadata.py \
--input_path input/datos1/sfiles_nordicformat \
--output_path output/data_prep_50s/catalog.json

python step1_preprocess1_get_windows.py \
--config_file_path experiments/config_50s.ini \
--raw_data_dir input/datos1/mseed \
--catalog_path output/data_prep_50s/catalog.json \
--prep_data_dir output/data_prep_50s

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_50s.ini \
--prep_data_dir output/data_prep_50s \
--tfrecords_dir output/data_prep_50s/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_50s.ini \
--prep_data_dir output/data_prep_50s \
--tfrecords_dir output/data_prep_50s/tfrecords

python step4_train.py \
--config_file_path experiments/config_50s.ini \
--tfrecords_dir output/data_prep_50s/tfrecords \
--checkpoint_dir output/train_50s/checkpoints

python step5_eval_over_tfrecords.py \
--config_file_path experiments/config_50s.ini \
--checkpoint_dir output/train_50s/checkpoints \
--output_dir output/train_50s/eval \
--tfrecords_dir output/data_prep_50s/tfrecords/test

