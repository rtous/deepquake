# 1/4
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

# 2/4
python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0420-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords2 \
--file_name 2015-02-05-0420-00S.tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0420-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords2 \
--file_name 2015-02-05-0420-00S.tfrecords

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0538-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords2 \
--file_name 2015-02-05-0538-00S.tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0538-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords2 \
--file_name 2015-02-05-0538-00S.tfrecords

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords2 \
--file_name 2015-01-10-0517-00S.tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords2 \
--file_name 2015-01-10-0517-00S.tfrecords

python step4_train.py \
--config_file_path experiments/config_experiment3_20s.ini \
--dataset_dir ./output/data_prep_experiment3_20s/tfrecords2 \
--checkpoint_dir ./output/data_prep_experiment3_20s/checkpoints2

python step5_eval.py \
--config_file_path experiments/config_experiment3_20s.ini \
--output_dir ./output/data_prep_experiment3_20s/eval2 \
--pattern 2015-02-05-0703-00S*.mseed \
--checkpoint_dir ./output/data_prep_experiment3_20s/checkpoints2

# 3/4
python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0420-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords3 \
--file_name 2015-02-05-0420-00S.tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0420-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords3 \
--file_name 2015-02-05-0420-00S.tfrecords

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords3 \
--file_name 2015-02-05-0703-00S.tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords3 \
--file_name 2015-02-05-0703-00S.tfrecords

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords3 \
--file_name 2015-01-10-0517-00S.tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords3 \
--file_name 2015-01-10-0517-00S.tfrecords

python step4_train.py \
--config_file_path experiments/config_experiment3_20s.ini \
--dataset_dir ./output/data_prep_experiment3_20s/tfrecords3 \
--checkpoint_dir ./output/data_prep_experiment3_20s/checkpoints3

python step5_eval.py \
--config_file_path experiments/config_experiment3_20s.ini \
--output_dir ./output/data_prep_experiment3_20s/eval3 \
--pattern 2015-02-05-0538-00S*.mseed \
--checkpoint_dir ./output/data_prep_experiment3_20s/checkpoints3

# 4/4
python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0538-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords2 \
--file_name 2015-02-05-0538-00S.tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0538-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords2 \
--file_name 2015-02-05-0538-00S.tfrecords

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords4 \
--file_name 2015-02-05-0703-00S.tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords4 \
--file_name 2015-02-05-0703-00S.tfrecords

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords4 \
--file_name 2015-01-10-0517-00S.tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment3_20s.ini \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir ./output/data_prep_experiment3_20s/tfrecords4 \
--file_name 2015-01-10-0517-00S.tfrecords

python step4_train.py \
--config_file_path experiments/config_experiment3_20s.ini \
--dataset_dir ./output/data_prep_experiment3_20s/tfrecords4 \
--checkpoint_dir ./output/data_prep_experiment3_20s/checkpoints4

python step5_eval.py \
--config_file_path experiments/config_experiment3_20s.ini \
--output_dir ./output/data_prep_experiment3_20s/eval4 \
--pattern 2015-02-05-0420-00S*.mseed \
--checkpoint_dir ./output/data_prep_experiment3_20s/checkpoints4