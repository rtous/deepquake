# DeepQuake

## 1 Setup environment (local machine)

NOTE: I tried the setup both on Mac (El Capitan) and Linux. Each one required its own tricks, which are probably not well documented here, but nothing extraordinary. 

Let's first create and activate a Python's virtualenv (let's assume you save your Python virtualenvs within MY_VIRTUALENVS folder, e.g. $HOME/virtualenvs):
 
	virtualenv MY_VIRTUALENVS/deepquake
	source MY_VIRTUALENVS/deepquake/bin/activate

Now download the repository from GiHub into your home directory or wherever you prefer: 

	cd
	git clone https://github.com/rtous/deepquake.git
	cd deepquake

WARNING: An "ouput" directory will be created after running some of the programs. This directory will not be part of the repository (is listed within .gitignore).

In case you don't have pip installed let's install it:

	curl https://bootstrap.pypa.io/get-pip.py | python

Install all the dependencies listed within requirements.txt:

	pip install -r requirements.txt

NOTE: According to the ConvNetQuake repo they used tensorflow 0.11. I tried with 0.12 and it works. However, this version are very old (currently 1.8) and we should consider updating at some point. 

## 2.1 Prepare the input data (FUNVISIS dataset)

The input data must be located within the input folder (from the root of the repo):

```
input
	|-funvisis
		|-mseed
		|-sfiles_nordicformat
```

Currently the input data is part of the repository for convenience. If these data would become too big we would remove them. 

Currently the data includes:

* Data for 5 events and many stations, +50 (AGIV, AUA1, BAUV, BBGH...).
* Sampled at 100Hz, 3-channels
* Event time windows is higher than 10s:
	*2015-01-10-0517-00S (total time 449.0s)
	*2015-02-05-0420-00S (total time 1199.0s)
	*2015-02-05-0538-00S (total time 1199.0s)
	*2015-02-05-0703-00S (total time 1199.0s)
	*2015-02-14-1027-00S (total time 449.0s)

* Each event has a .mseed for all the stations and a metadata in Nordic Format (easy process if translated to obspy with seisobs) 
* Provides also .mseed splits by station and channel (not using them now).

## 2.2 Utils for inspecting the data

Plotting a complete mseed file (all stations, all channels):

	cd 
	cd deepquake
	export PYTHONPATH=.
	python util_plot_mseed.py --stream_path input/funvisis/mseed/2015-01-10-0517-00S.MAN___161

NOTE: Results within the output directory.

The following utility allows to read the S-File metadata (shows some from the terminal, write them to output/metadata.xml):
	
	python util_read_metadata.py --stream_path input/funvisis/sfiles_nordicformat/05-0420-00L.S201502
	python util_read_metadata.py --stream_path input/funvisis/sfiles_nordicformat/05-0538-00L.S201502
	python util_read_metadata.py --stream_path input/funvisis/sfiles_nordicformat/05-0703-00L.S201502
	python util_read_metadata.py --stream_path input/funvisis/sfiles_nordicformat/10-0517-00L.S201501 

The following utility allows to join .mseed files containing the different components:

python util_join_components.py \
--streamHHN_path input/funvisis/other/CAPV/CAPV.VE..HHN.2017.323 \
--streamHHE_path input/funvisis/other/CAPV/CAPV.VE..HHE.2017.323 \
--streamHHZ_path input/funvisis/other/CAPV/CAPV.VE..HHZ.2017.323 \
--output_stream_path input/funvisis/other/CAPV.VE.2017.323

## 2.3 Step 1. Preprocessing 1. Converting FUNVISIS to ConvNetQuake format

The following utility will:

1. split the data of all the events into station-level mseed
2. Extract windows noise from all the events
3. Save .png for everything

	python step1_preprocess1_funvisis2oklahoma.py

NOTE: By default it processes all the files in input directory.
NOTE: By default results within output/data_prep_default.

In order to use the utility over specific files, you may do:

	python step1_preprocess1_funvisis2oklahoma.py \
	--input_stream ./input/data_raw_default/mseed/2015-01-10-0517-00S.MAN___161 \
	--input_metadata ./input/data_raw_default/sfiles_nordicformat/10-0517-00L.S201501 \
	--output_dir ./output/data_prep_sometest

Or you may prefer to use specific config file for the experiment:

	python step1_preprocess1_funvisis2oklahoma.py \
	--config_file_path config_test.ini

To save plots use:

	--plot_station True
	--plot_positives True
	--plot_negatives True

## 2.4 Step 2. Preprocessing 2. Generating tfrecords for positives

	python step2_preprocess2_create_tfrecords_positives.py

In order to use the utility over specific files, you may do:

	python step2_preprocess2_create_tfrecords_positives.py \
	--pattern 2015-02-05-0420-00S*.mseed \
	--output_dir ./output/data_prep_sometest/tfrecords1 \
	--file_name 2015-02-05-0420-00S.tfrecords

Or you may prefer to use specific config file for the experiment:

	python step2_preprocess2_create_tfrecords_positives.py \
	--config_file_path config_test.ini

## 2.5 Step 3. Preprocessing 3. Generating tfrecords for negatives

	python step3_preprocess3_create_tfrecords_negatives.py

In order to use the utility over specific files, you may do:

	python step3_preprocess3_create_tfrecords_negatives.py \
	--pattern 2015-02-05-0420-00S-00S*.mseed \
	--output_dir ./output/data_prep_sometest/tfrecords1 \
	--file_name 2015-02-05-0420-00S.tfrecords

Or you may prefer to use specific config file for the experiment:

	python step3_preprocess3_create_tfrecords_negatives.py \
	--config_file_path config_test.ini

## 2.6 Step 4. Train

	python step4_train.py

In order to change the paths you may do:

	python step4_train.py \
	--dataset_dir ./output/data_prep_sometest/tfrecords \
	--checkpoint_dir ./output/train_sometest/checkpoints

Or you may prefer to use specific config file for the experiment:

	python step4_train.py \
	--config_file_path config_test.ini

## 2.7 Step 5. Eval

	python step5_eval.py

In order to change the paths you may do:

	python step5_eval.py \
	--stream_path ./output/test/mseed

In order to change the defaults you may do:

	python step5_eval.py \
	--config_file_path config_test.ini \
	--stream_path ./output/data_prep_sometest/mseed \
	--pattern 2015-02-05-0420-00S \
	--output_dir ./output/train_sometest/predict \
	--checkpoint_dir ./output/train_sometest/checkpoints

Or you may prefer to use specific config file for the experiment:

	python step5_eval.py \
	--config_file_path config_test.ini

## 2.8 Preliminary conclusions

* 500s windows from funvisis >>> 10s windows from ConvNetQuake
* Predicting with ConvNetQuake model over funvisis finds too much events
* Using 50s windows worked better than 10s. Other values to be tested

## 2.9 Troubleshooting

	"tensorflow.python.framework.errors_impl.InternalError: Unable to get element from the feed as bytes." -> cannot find the checkpoint file

	"ValueError: string_input_producer requires a non-null input tensor" -> the training directoris should be "positive" and "negative" without "s" at the end.

	"InvalidArgumentError (see above for traceback): Name: <unknown>, Feature: end_time is required but could not be found." -> Using old positives/negatives (downloaded), generate new ones

	"_tkinter.TclError: no display name and no $DISPLAY environment variable" -> Add this code to the start of your script (before importing pyplot) and try again:
			import matplotlib
			matplotlib.use('Agg')

	"tf.errors.OutOfRangeError" -> a parameter from config .ini is not being passed correctly. Harcode it in config.py instead.

## 2.10 TODO

* making plotting optional
* use local scratch in arvei instead of nas
* Change step1_preprocess1_funvisis2oklahoma.py to generate training samples trough a pure sliding window
* Intensive testing of different parameters
* Overlapping detections fussion 
* Arvei:
	- Intermediate results should go to local scratch.
	- stdout should be saved outside the execution node. 
* keep tensorflow 0.12.0 wheel somewhere (pip install tensorflow==0.12.0 stop working)
* keep openquake.hazardlib==0.22.0 from https://github.com/gem/oq-hazardlib/releases

DONE:

* Extract Funvisis data for ALL stations
* Prepare my own noise and see how it looks like
* (ignored) metadata 5/2 21:50 does not have stream. Stream 14/02 does not have metadata
* (ignored) data from stations HEL and URI is flat. Some signals from other stations are not complete

## 2.11 Lessons learned

* Ar

/* ——————————————————————————————————- */
/* ——————————————————————————————————- */
/* ——————————————————————————————————- */

## ANNEX 1. Running tperol/ConvNetQuake

Input:

* Input 1: 47 1-month 3-channel 100Hz .mseed files (2 stations, 13 GSOK027, 34 GSOK029).
* Continous records (not divided by events) for years 2014, 2015, 2016.
* Input 2: A .csv catalog of around 3K events for these years

Workflow:
 
1. Cluster locations in the catalog into 6 regions (kmeans, Voronoi map)
2. Use the catalog info to extract the waveforms for the 3K events from the 47 input streams. Pick only 10 second per event. (the positives)
3. (optional) augment these data (x2)
4. Generate +700K synthetic noise windows (the negatives)
5. Get 90% for training, 10% for test. 
6. Train with a CNN with a 10x100x3 input and 7 outputs (6 locations, 1 no event).

Results:

* Acceptable (but low) location accuracy (around 76%)
* 100% recall
* 93% precission

Open issues

* Why 10 seconds?
* It's ok treating data from both stations the same way?

Get the repo:

	git clone https://github.com/tperol/ConvNetQuake.git
	cd /vol/ConvNetQuake

### A1.1 Predict

	mkdir -p data/streams
	#DOWNLOAD data/streams/GS0K029_5-2015.mseed into data/streams
	export PYTHONPATH=.
	mkdir -p models/convnetquake
	#DOWNLOAD models/convnetquake/model-32000 into folder models/convnetquake
	#DOWNLOAD models/convnetquake/checkpoint into folder models/convnetquake
	./bin/predict_from_stream.py --stream_path data/streams/GSOK027_8-2014.mseed \
	--checkpoint_dir models/convnetquake --n_clusters 6 \
	--window_step 11 --output output/july_detections/from_stream \
	--max_windows 8640

	(takes about 3-5 minutes, results within the output dir)

### A1.2 Train with already preprocessed data 
	
	mkdir -p data/6_clusters
	#DOWNLOAD data/6_clusters/detection/train into data/6_clusters (Note: +4GB!!)
	./bin/train --dataset data/6_clusters/train --checkpoint_dir output/convnetquake --n_clusters 6

	(takes few hours but with less than 5 minuts you can see that it works)

### A1.3 Preprocess the data your own

Cluster events (generate region centroids):

	mkdir data/catalogs
	#DOWNLOAD data/catalogs/OK_2014-2015-2016.csv into data/catalogs
	./bin/preprocess/cluster_events --src data/catalogs/OK_2014-2015-2016.csv --dst data/6_clusters --n_components 6 --model KMeans
	#This outputs in data/6_clusters: catalog_with_cluster_ids.csv: catalog of labeled events + clusters_metadata.json: number of events per clusters.

Match training data to clusters (regions):

	./bin/preprocess/create_dataset_events.py --stream_dir data/streams --catalog data/6_clusters/catalog_with_cluster_ids.csv --output_dir data/6_clusters/events --save_mseed True --plot False
	#A data/6_clusters/events deixa les dades per a l'entrenament

Data augmentation:

	./bin/preprocess/data_augmentation.py --tfrecords data/6_clusters/events --output data/6_clusters/augmented_data/augmented_stetch_std1-2.tfrecords --std_factor 1.2

Noise windows:

	#DOWNLOAD data/catalogs/OK_2014-Benz_catalog-2016.csv into data/catalogs
	./bin/preprocess/create_dataset_noise.py --stream_path data/streams/GSOK027_8-2014.mseed --catalog data/catalogs/Benz_catalog.csv --output_dir data/noise_OK029/noise_august --plot

The training data should be within a directory with this structure:
	
	train
		|- positive 
		|- negative

Now you can run step 2.2 again to train with your own data.

## ANNEX 2. Using a Docker container 

	(I'm not actually using this because of memory constraints)

	docker build -t deepquake:latest -f Dockerfile .
	docker run -it --name deepquake -v //Users/rtous/DockerVolume:/vol -d -p 8080:8080 deepquake:latest
	docker exec -it deepquake bash
	cd vol

	(Note: basic tests require about 8GB of memory so using Docker may not be a good idea depending on your hardware. Be sure to change the memory limit on Docker preferences.)

