python catalog.py \
--input_path input/data_raw_default/sfiles_nordicformat \
--output_path output/data_prova/catalog.json

python step1_preprocess1_funvisis2oklahoma_v2.py \
--config_file_path experiments/config_10s_Z.ini \
--raw_data_dir input/data_raw_default/mseed \
--catalog_path output/data_prova/catalog.json \
--prep_data_dir output/data_prova


python catalog.py \
--input_path input/datos2/sfiles_nordicformat \
--output_path output/data_prova2/catalog.json

python step1_preprocess1_funvisis2oklahoma_v2.py \
--config_file_path experiments/config_10s_Z.ini \
--raw_data_dir input/datos2/mseed \
--catalog_path output/data_prova2/catalog.json \
--prep_data_dir output/data_prova2

