# gan

## Dev env setup

	docker build -t deepquake:latest -f Dockerfile .
	docker run -it --name deepquake -v //Users/rtous/DockerVolume:/vol -d -p 8080:8080 deepquake:latest
	docker exec -it deepquake bash

cd /vol/ConvNetQuake
mkdir data
mkdir streams
#copy GSOK029_8-2014.mseed there
export PYTHONPATH=.
sudo apt-get install ttf-bitstream-vera

./bin/predict_from_stream.py --stream_path data/streams/GSOK027_8-2014.mseed \
--checkpoint_dir models/convnetquake --n_clusters 6 \
--window_step 11 --output output/july_detections/from_stream \
--max_windows 8640