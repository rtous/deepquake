!/bin/bash

### Ejecutar
CURRENT_ENVIRONMENT=`ls -d /scratch/nas/4/rtous`/convnetquake
source $CURRENT_ENVIRONMENT/bin/activate
cd /scratch/nas/4/rtous/deepquake/
#export PYTHONPATH=.
#./util_read_metadata.py --stream_path input/funvisis/sfiles_nordicformat/05-0420-00L.S201502

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





