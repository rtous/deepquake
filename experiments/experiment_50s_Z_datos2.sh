python util_datos2_metadata2csv.py \
--input_metadata_file input/datos2/Eventos.txt \
--output_csv_metadata_file output/data_prep_datos2/catalog.csv

python step1_preprocess1_datos2.py \
--config_file_path experiments/config_50s_Z.ini \
--raw_data_dir input/datos2 \
--prep_data_dir output/data_prep_datos2 \
--catalog_path output/data_prep_datos2/catalog.csv \
--stations_path input/stations.csv

python step2_preprocess2_create_tfrecords_positives.py \
--config_file_path experiments/config_50s_Z.ini \
--prep_data_dir output/data_prep_datos2 \
--tfrecords_dir output/data_prep_datos2/tfrecords

python step3_preprocess3_create_tfrecords_negatives.py \
--config_file_path experiments/config_50s_Z.ini \
--prep_data_dir output/data_prep_datos2 \
--tfrecords_dir output/data_prep_datos2/tfrecords

python step4_train.py \
--config_file_path experiments/config_50s_Z.ini \
--tfrecords_dir output/data_prep_datos2/tfrecords \
--checkpoint_dir output/train_datos2/checkpoints

python step5_eval_over_tfrecords.py \
--config_file_path experiments/config_50s_Z.ini \
--checkpoint_dir output/train_datos2/checkpoints \
--output_dir output/train_datos2/eval \
--tfrecords_dir output/data_prep_datos2/tfrecords/test

