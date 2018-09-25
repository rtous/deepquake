#Asume data already preprocessed in data_prep_experiment5_50s_LOCV 

# 1/4
python step4_train.py \
--config_file_path experiments/config_50s_modelv2.ini \
--tfrecords_dir output/data_prep_experiment5_50s_LOCV/tfrecords1 \
--checkpoint_dir output/train_experiment5_50s_LOCV/checkpoints1

python step5_eval.py \
--stream_path output/data_prep_default/mseed \
--config_file_path experiments/config_50s_modelv2.ini \
--checkpoint_dir output/train_experiment5_50s_LOCV/checkpoints1 \
--pattern 2015-01-10-0517-00S*.mseed \
--output_dir output/train_experiment5_50s_LOCV/eval1

# 2/4
python step4_train.py \
--config_file_path experiments/config_50s_modelv2.ini \
--tfrecords_dir output/data_prep_experiment5_50s_LOCV/tfrecords2 \
--checkpoint_dir output/train_experiment5_50s_LOCV/checkpoints2

python step5_eval.py \
--stream_path output/data_prep_default/mseed \
--config_file_path experiments/config_50s_modelv2.ini \
--checkpoint_dir output/train_experiment5_50s_LOCV/checkpoints2 \
--pattern 2015-02-05-0703-00S*.mseed \
--output_dir output/train_experiment5_50s_LOCV/eval2

# 3/4
python step4_train.py \
--config_file_path experiments/config_50s_modelv2.ini \
--tfrecords_dir output/data_prep_experiment5_50s_LOCV/tfrecords3 \
--checkpoint_dir output/train_experiment5_50s_LOCV/checkpoints3

python step5_eval.py \
--stream_path output/data_prep_default/mseed \
--config_file_path experiments/config_50s_modelv2.ini \
--checkpoint_dir output/train_experiment5_50s_LOCV/checkpoints3 \
--pattern 2015-02-05-0538-00S*.mseed \
--output_dir output/train_experiment5_50s_LOCV/eval3

# 4/4
python step4_train.py \
--config_file_path experiments/config_50s_modelv2.ini \
--tfrecords_dir output/data_prep_experiment5_50s_LOCV/tfrecords4 \
--checkpoint_dir output/train_experiment5_50s_LOCV/checkpoints4

python step5_eval.py \
--stream_path output/data_prep_default/mseed \
--config_file_path experiments/config_50s_modelv2.ini \
--checkpoint_dir output/train_experiment5_50s_LOCV/checkpoints4 \
--pattern 2015-02-05-0420-00S*.mseed \
--output_dir output/train_experiment5_50s_LOCV/eval4