python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0420-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords1 \
--file_name 2015-02-05-0420-00S.tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0420-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords1 \
--file_name 2015-02-05-0420-00S.tfrecords

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0538-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords1 \
--file_name 2015-02-05-0538-00S.tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0538-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords1 \
--file_name 2015-02-05-0538-00S.tfrecords

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords1 \
--file_name 2015-02-05-0703-00S.tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords1 \
--file_name 2015-02-05-0703-00S.tfrecords

python step4_train.py \
--config_file_path experiments/config_experiment3_20s.ini \
--dataset_dir ./output/data_prep_experiment3_20s/tfrecords1 \
--checkpoint_dir ./output/data_prep_experiment3_20s/checkpoints1

python step5_eval.py \
--config_file_path experiments/config_experiment3_20s.ini \
--output_dir ./output/data_prep_experiment3_20s/eval1 \
--pattern 2015-01-10-0517-00S*.mseed \
--checkpoint_dir ./output/data_prep_experiment3_20s/checkpoints1