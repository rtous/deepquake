#EXPERIMENT experiment1
#2015-02-05-0420-00S train
#2015-02-05-0538-00S train
#2015-02-05-0703-00S train
#2015-01-10-0517-00S test


python step1_preprocess1_funvisis2oklahoma.py \
--config_file_path ./config_experiment2.ini \
--output_dir ./output/inputdata50

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path ./config_experiment2.ini \
--dataset_dir ./output/inputdata50 \
--pattern 2015-02-05-0420-00S*.mseed \
--output_dir ./output/experiment1/tfrecords1 \
--file_name 2015-02-05-0420-00S.tfrecords
python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path ./config_experiment2.ini \
--dataset_dir ./output/inputdata50 \
--pattern 2015-02-05-0420-00S*.mseed \
--output_dir ./output/experiment1/tfrecords1 \
--file_name 2015-02-05-0420-00S.tfrecords

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path ./config_experiment2.ini \
--dataset_dir ./output/inputdata50 \
--pattern 2015-02-05-0538-00S*.mseed \
--output_dir ./output/experiment1/tfrecords1 \
--file_name 2015-02-05-0538-00S.tfrecords
python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path ./config_experiment2.ini \
--dataset_dir ./output/inputdata50 \
--pattern 2015-02-05-0538-00S*.mseed \
--output_dir ./output/experiment1/tfrecords1 \
--file_name 2015-02-05-0538-00S.tfrecords

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path ./config_experiment2.ini \
--dataset_dir ./output/inputdata50 \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/experiment1/tfrecords1 \
--file_name 2015-02-05-0703-00S.tfrecords
python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path ./config_experiment2.ini \
--dataset_dir ./output/inputdata50 \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/experiment1/tfrecords1 \
--file_name 2015-02-05-0703-00S.tfrecords

python step4_train.py \
--config_file_path ./config_experiment2.ini \
--dataset_dir ./output/experiment1/tfrecords1 \
--checkpoint_dir ./output/experiment1/checkpoints1

python step6_predict.py \
--config_file_path ./config_experiment2.ini \
--stream_path ./output/inputdata50/mseed \
--pattern 2015-02-05-0420-00S \
--output_dir ./output/experiment1/predict1 \
--pattern 2015-01-10-0517-00S*.mseed \
--checkpoint_dir ./output/experiment1/checkpoints1

