python step1_preprocess1_funvisis2oklahoma.py \
--config_file_path experiments/config_experiment3_20s.ini

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment3_20s.ini

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment3_20s.ini

python step4_train.py \
--config_file_path experiments/config_experiment3_20s.ini

python step5_eval.py \
--config_file_path experiments/config_experiment3_20s.ini
