python step1_preprocess1_funvisis2oklahoma.py \
--config_file_path experiments/config_experiment1_test.ini \
--pattern 05-0420-00L* \
--station CRUV

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_experiment1_test.ini

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_experiment1_test.ini

python step4_train.py \
--config_file_path experiments/config_experiment1_test.ini

python step5_eval.py \
--config_file_path experiments/config_experiment1_test.ini
