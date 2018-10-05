python step4_train.py \
--config_file_path experiments/config_50s_model2b.ini \
--tfrecords_dir output/data_prep_50s/tfrecords \
--checkpoint_dir output/train_50s/checkpoints

python step5_eval_over_tfrecords.py \
--config_file_path experiments/config_50s_model2b.ini \
--checkpoint_dir output/train_50s/checkpoints \
--output_dir output/train_50s/eval \
--tfrecords_dir output/data_prep_50s/tfrecords/test

