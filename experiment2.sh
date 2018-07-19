python step1_preprocess1_funvisis2oklahoma.py \
--output_dir ./output/prepdata_1_50s_nonsliding

python step2_preprocess2_create_tfrecords_positives.py \
--dataset_dir ./output/prepdata_1_50s_nonsliding \
--output_dir ./output/prepdata_1_50s_nonsliding/tfrecords
python step3_preprocess3_create_tfrecords_negatives.py \
--dataset_dir ./output/prepdata_1_50s_nonsliding \
--output_dir ./output/prepdata_1_50s_nonsliding/tfrecords

python step4_train.py \
--dataset_dir ./output/prepdata_1_50s_nonsliding/tfrecords \
--checkpoint_dir ./output/experiment1/checkpoints

python step6_predict.py \
--stream_path ./output/prepdata_1_50s_nonsliding/mseed \
--output_dir ./output/experiment1/predict \
--checkpoint_dir ./output/experiment1/checkpoints