python step1_preprocess1_funvisis2oklahoma.py \
--raw_data_dir input/data_raw_default/mseed \
--raw_metadata_dir input/data_raw_default/sfiles_nordicformat \
--prep_data_dir output/data_prep_default

python step2_preprocess2_create_tfrecords_positives.py \
--prep_data_dir output/data_prep_default \
--tfrecords_dir output/data_prep_default/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--prep_data_dir output/data_prep_default \
--tfrecords_dir output/data_prep_default/tfrecords

python step4_train.py \
--tfrecords_dir output/data_prep_default/tfrecords \
--checkpoint_dir output/train_default/checkpoints

python step5_eval.py \
--stream_path output/data_prep_default/mseed \
--checkpoint_dir output/train_default/checkpoints \
--output_dir output/train_default/eval