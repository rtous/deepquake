#!/usr/bin/env python
# -------------------------------------------------------------------
# File Name : create_dataset_events.py
# Creation Date : 05-12-2016
# Last Modified : Fri Jan  6 15:04:54 2017
# Author: Thibaut Perol <tperol@g.harvard.edu>
# -------------------------------------------------------------------
"""Creates tfrecords dataset of events trace and their cluster_ids.
This is done by loading a dir of .mseed and one catalog with the
time stamps of the events and their cluster_id
e.g.,
./bin/preprocess/create_dataset_events.py \
--stream_dir data/streams \
--catalog data/50_clusters/catalog_with_cluster_ids.csv\
--output_dir data/50_clusters/tfrecords
"""

import os
import numpy as np
from quakenet.data_pipeline import DataWriter
import tensorflow as tf
from obspy.core import read
from quakenet.data_io import load_catalog
from obspy.core.utcdatetime import UTCDateTime
from openquake.hazardlib.geo.geodetic import distance
import fnmatch
import json

INPUT_STREAM_DIR = "funvisis/funvisis2oklahoma/mseed_10s"
OUTPUT_TFRECORDS_DIR = "output_funvisis/positive"
WINDOW_SIZE = 10

def preprocess_stream(stream):
    stream = stream.detrend('constant')
    return stream.normalize()

def main(_):

    stream_files = [file for file in os.listdir(INPUT_STREAM_DIR) if
                    fnmatch.fnmatch(file, '*.mseed')]

    # Create dir to store tfrecords
    if not os.path.exists(OUTPUT_TFRECORDS_DIR):
        os.makedirs(OUTPUT_TFRECORDS_DIR)

    # Write event waveforms and cluster_id in .tfrecords
    output_name = "positives.tfrecords"
    output_path = os.path.join(OUTPUT_TFRECORDS_DIR, output_name)
    writer = DataWriter(output_path)
    for stream_file in stream_files:
        stream_path = os.path.join(INPUT_STREAM_DIR, stream_file)
        print "+ Loading Stream {}".format(stream_file)
        st_event = read(stream_path)
        print '+ Preprocessing stream'
        st_event = preprocess_stream(st_event)   

        #cluster_id = filtered_catalog.cluster_id.values[event_n]
        cluster_id = 0 #We work with only one location for the moment (cluster id = 0)
        n_traces = len(st_event)
        # If there is not trace skip this waveform
        if n_traces == 0:
            continue
        n_samples = len(st_event[0].data)
        n_pts = st_event[0].stats.sampling_rate * WINDOW_SIZE + 1
        if (len(st_event) == 3) and (n_pts == n_samples) and (st_event[0].stats.sampling_rate == 100.0):
            print("Writing sample with dimensions "+str(WINDOW_SIZE)+"x"+str(st_event[0].stats.sampling_rate)+"x"+str(n_traces))
            # Write tfrecords
            writer.write(st_event, cluster_id) 
        else:
            print ("\033[91m WARNING!!\033[0m Missing waveform for event in "+stream_file)

    # Cleanup writer
    print("Number of events written={}".format(writer._written))
    writer.close()
    

if __name__ == "__main__":
    tf.app.run()
