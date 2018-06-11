# DeepQuake

## Running tperol/ConvNetQuake

### Using a Docker container

	docker build -t deepquake:latest -f Dockerfile .
	docker run -it --name deepquake -v //Users/rtous/DockerVolume:/vol -d -p 8080:8080 deepquake:latest
	docker exec -it deepquake bash
	cd vol

	(Note: basic tests require about 8GB of memory so using Docker may not be a good idea depending on your hardware. Be sure to change the memory limit on Docker preferences.)

### Running it

(Note: Dropbox data at https://www.dropbox.com/sh/3p9rmi1bcpvnk5k/AAAV8n9VG_e0QXOpoofsSH0Ma?dl=0)

(Note: Dropbox models at https://www.dropbox.com/sh/t9dj8mmfx1fmxfa/AABSJQke8Ao6wfRnKMvQXipta?dl=0)

### Using virtualenv

cd 
virtualenv Virtualenvs/deepquake
source Virtualenvs/deepquake/bin/activate
cd DockerVolume/deepquake
curl https://bootstrap.pypa.io/get-pip.py | python
pip install -r requirements.txt


#### Test 1: Predict

	git clone https://github.com/tperol/ConvNetQuake.git
	cd /vol/ConvNetQuake
	mkdir -p data/streams
	#DOWNLOAD data/streams/GS0K029_5-2015.mseed into data/streams
	wget -P data/streams https://www.dropbox.com/sh/3p9rmi1bcpvnk5k/AAA0mMlJvhGF2neoN1mKhXQOa/streams/GS0K029_5-2015.mseed
	export PYTHONPATH=.
	mkdir -p models/convnetquake
	#DOWNLOAD models/convnetquake/model-32000 into folder models/convnetquake
	#DOWNLOAD models/convnetquake/checkpoint into folder models/convnetquake
	./bin/predict_from_stream.py --stream_path data/streams/GSOK027_8-2014.mseed \
--checkpoint_dir models/convnetquake --n_clusters 6 \
--window_step 11 --output output/july_detections/from_stream \
--max_windows 8640

	(takes about 3-5 minutes, results within the output dir)

#### Test 2: Train
	
	mkdir -p data/6_clusters
	#DOWNLOAD data/6_clusters/detection/train into data/6_clusters (Note: +4GB!!)
	./bin/train --dataset data/6_clusters/train --checkpoint_dir output/convnetquake --n_clusters 6


#### Test 3: Prepare your own training data

	a) Cluster events (generate region centroids)
	mkdir data/catalogs
	#DOWNLOAD data/catalogs/OK_2014-2015-2016.csv into data/catalogs
	./bin/preprocess/cluster_events --src data/catalogs/OK_2014-2015-2016.csv --dst data/6_clusters --n_components 6 --model KMeans
	#This outputs in data/6_clusters: catalog_with_cluster_ids.csv: catalog of labeled events + clusters_metadata.json: number of events per clusters.

	b) Match training data to clusters (regions)
	./bin/preprocess/create_dataset_events.py --stream_dir data/streams --catalog data/6_clusters/catalog_with_cluster_ids.csv --output_dir data/6_clusters/events --save_mseed True --plot True
	#A data/6_clusters/events deixa les dades per a l'entrenament

	c) Data augmentation
	./bin/preprocess/data_augmentation.py --tfrecords data/6_clusters/events --output data/6_clusters/augmented_data/augmented_stetch_std1-2.tfrecords --std_factor 1.2

	d) Noise windows
	#DOWNLOAD data/catalogs/OK_2014-Benz_catalog-2016.csv into data/catalogs
	./bin/preprocess/create_dataset_noise.py --stream_path data/streams/GSOK027_8-2014.mseed --catalog data/catalogs/Benz_catalog.csv --output_dir data/noise_OK029/noise_august

TROUBLESHOOTING:
- "tensorflow.python.framework.errors_impl.InternalError: Unable to get element from the feed as bytes." -> cannot find the checkpoint file