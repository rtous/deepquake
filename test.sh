python step1_preprocess1_funvisis2oklahoma.py \
--pattern 05-0420-00L* \
--output_dir ./output/test

python step2_preprocess2_create_tfrecords_positives.py \
--dataset_dir ./output/test \
--output_dir ./output/test/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--dataset_dir ./output/test \
--output_dir ./output/test/tfrecords

python step4_train.py \
--dataset_dir ./output/test/tfrecords \
--checkpoint_dir ./output/test/checkpoints

python step6_predict.py \
--stream_path ./output/test/mseed \
--output_dir ./output/test/predict \
--checkpoint_dir ./output/test/checkpoints

