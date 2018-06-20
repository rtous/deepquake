# DeepQuake

## 1 Setup environment (local machine)

Let's first create a Python's virtualenv:

	cd 
	virtualenv Virtualenvs/deepquake
	source Virtualenvs/deepquake/bin/activate
	cd DockerVolume/deepquake
	curl https://bootstrap.pypa.io/get-pip.py | python
	pip install -r requirements.txt

## 2. Running tperol/ConvNetQuake

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
	./bin/preprocess/create_dataset_noise.py --stream_path data/streams/GSOK027_8-2014.mseed --catalog data/catalogs/Benz_catalog.csv --output_dir data/noise_OK029/noise_august

The training data should be within a directory with this structure:
	
	train
		|- positive 
		|- negative

Now you can run step 2.2 again to train with your own data.

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