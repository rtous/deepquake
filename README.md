# DeepQuake

## 1 Setup environment (local machine)

According to the ConvNetQuake repo they used tensorflow 0.11. I tried with 0.12 and it works. However, this version are very old (currently 1.8) and we should consider updating at some point. I tried the setup both on Mac and Linux. Each one required its own tricks, which are probably not well documented here, but nothing extraordinary. 

Let's first create a Python's virtualenv:

	cd 
	virtualenv Virtualenvs/deepquake
	source Virtualenvs/deepquake/bin/activate
	cd DockerVolume/deepquake
	curl https://bootstrap.pypa.io/get-pip.py | python
	pip install -r requirements.txt

## 2. Running tperol/ConvNetQuake

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

### 2.1 Predict

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

### 2.2 Train with already preprocessed data 
	
	mkdir -p data/6_clusters
	#DOWNLOAD data/6_clusters/detection/train into data/6_clusters (Note: +4GB!!)
	./bin/train --dataset data/6_clusters/train --checkpoint_dir output/convnetquake --n_clusters 6

	(takes few hours but with less than 5 minuts you can see that it works)

### 2.3 Preprocess the data your own

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


## 3. Deepquake (Funvisis dataset)

### 3.1 Deepquake (Funvisis dataset)

* Only data for the events 
* Also sampled at 100Hz, also 3-channels
* Data for 5 events but for many stations, +50 (AGIV, AUA1, BAUV, BBGH...).
* Event time windows is higher than 10s:
	*2015-01-10-0517-00S (total time 449.0s)
	*2015-02-05-0420-00S (total time 1199.0s)
	*2015-02-05-0538-00S (total time 1199.0s)
	*2015-02-05-0703-00S (total time 1199.0s)
	*2015-02-14-1027-00S (total time 449.0s)

* Each event has a .mseed for all the stations and a metadata in Nordic Format (easy process if translated to obspy with seisobs) 
* Provides also .mseed splits by station and channel (useless).

### 3.2 Inspecting the data

Plotting the 3 channels of one station (harcoded):

	cd 
	cd deepquake
	export PYTHONPATH=.
	python plot_mseed.py --stream_path /Users/rtous/DockerVolume/deepquake_data/sfiles/2015-01-10-0517-00S.MAN___161

The following utility allows to read the S-File metadata:

	python read_metadata.py --stream_path funvisis/sfiles_nordicformat/10-0517-00L.S201501 

This is a tuned version of the ConvNetQuake (works over ConvNetQuake data) that allows to plot the samples that ConvNetQuake selects for training:

	python create_dataset_events_OLD.py --stream_dir data/streams --catalog data/6_clusters/catalog_with_cluster_ids.csv --output_dir data/6_clusters/events --save_mseed False --plot True

This is a tuned version of the same ConvNetQuake .py (works over ConvNetQuake data) that allows to plot the 10s windows that ConvNetQuake used during PREDICTION:

	python read_mseed.py --stream_path data/streams/GSOK027_3-2015.mseed \
	--output_dir data/tfrecord \
	--window_size 10 --window_step 11 \
	--max_windows 5000 \
	--plot True

### 3.3 Converting FUNVISIS to ConvNetQuake

This utility splits the data of all the events for one station (harcoded).

	python funvisis2oklahoma.py

### 3.4 Predicting with ConvNetQuake over transformed FUNVISIS mseed

	(from the ConvNetQuake repo)

	cd ..
	cd ConvNetQuake 
	./bin/predict_from_stream.py --stream_path ../deepquake/funvisis/funvisis2oklahoma/mseed/2015-01-10-0517-00S.MAN___161.mseed \
	--checkpoint_dir models/convnetquake --n_clusters 6 \
	--window_step 11 --output output/funvisis \
	--max_windows 8640 --plot

### 3.5 Training with FUNVISIS data

(back to the deepquake repo)

We convert the 10s streams to tfrecords this way:

	python create_dataset_events.py

We copy some noise windows to the negative folder and then: (TODO: generate our own noise)

	python train.py

	create_dataset_noise.py --stream_path data/streams/GSOK027_8-2014.mseed --catalog data/catalogs/Benz_catalog.csv --output_dir data/noise_OK029/noise_august --plot


### 3.6 Predicting with FUNVISIS model and FUNVISIS mseed

	(from the ConvNetQuake repo)

	python predict_from_stream.py --stream_path funvisis/funvisis2oklahoma/mseed/2015-01-10-0517-00S.MAN___161_CRUV.mseed \
	--checkpoint_dir output_funvisis/checkpoints/ConvNetQuake --n_clusters 1 \
	--window_step 11 --output output_funvisis/prediction \
	--max_windows 8640 --plot

### 3.? Preliminary conclusions

* 500s windows from funvisis >>> 10s windows from ConvNetQuake
* Predicting with ConvNetQuake model over funvisis finds too much events

## ANNEX 1. Using a Docker container 

	(I'm not actually using this because of memory constraints)

	docker build -t deepquake:latest -f Dockerfile .
	docker run -it --name deepquake -v //Users/rtous/DockerVolume:/vol -d -p 8080:8080 deepquake:latest
	docker exec -it deepquake bash
	cd vol

	(Note: basic tests require about 8GB of memory so using Docker may not be a good idea depending on your hardware. Be sure to change the memory limit on Docker preferences.)

## Troubleshooting

	"tensorflow.python.framework.errors_impl.InternalError: Unable to get element from the feed as bytes." -> cannot find the checkpoint file

	"ValueError: string_input_producer requires a non-null input tensor" -> the training directoris should be "positive" and "negative" without "s" at the end.

	"InvalidArgumentError (see above for traceback): Name: <unknown>, Feature: end_time is required but could not be found." -> Using old positives/negatives (downloaded), generate new ones

## TODO

* Prepare my own noise and see how it looks like
* metadata 5/2 21:50 does not have stream. Stream 14/02 does not have metadata
* data from stations HEL and URI is flat. Some signals from other stations are not complete
* Check the real duration of funvisis events
* DUBTE: Coincideix el temps d'inici de l'event amb l'inici de l'stream? Diria que no, però com s'estableix??

DONE

* Extract Funvisis data for ALL stations
