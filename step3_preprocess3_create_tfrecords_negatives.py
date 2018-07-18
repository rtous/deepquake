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
import argparse
import config as config
import utils

def preprocess_stream(stream):
    stream = stream.detrend('constant')
    return stream.normalize()

def main(_):
    print("[tfrecords negatives] Converting .mseed files into tfrecords...")
    print("[tfrecords negatives] Input directory: "+os.path.join(dataset_dir, cfg.MSEED_NOISE_DIR))
    print("[tfrecords negatives] Output directory: "+os.path.join(output_dir, cfg.OUTPUT_TFRECORDS_DIR_NEGATIVES))
    print("[tfrecords negatives] File pattern: "+args.pattern)

    stream_files = [file for file in os.listdir(os.path.join(dataset_dir, cfg.MSEED_NOISE_DIR)) if
                    fnmatch.fnmatch(file, args.pattern)]
    print("[tfrecords negatives] Matching files: "+str(len(stream_files)))

    # Create dir to store tfrecords
    if not os.path.exists(os.path.join(output_dir, cfg.OUTPUT_TFRECORDS_DIR_NEGATIVES)):
        os.makedirs(os.path.join(output_dir, cfg.OUTPUT_TFRECORDS_DIR_NEGATIVES))

    # Write event waveforms and cluster_id in .tfrecords
    output_name = output_name = args.file_name
    output_path = os.path.join(os.path.join(output_dir, cfg.OUTPUT_TFRECORDS_DIR_NEGATIVES), output_name)
    writer = DataWriter(output_path)
    for stream_file in stream_files:
        stream_path = os.path.join(os.path.join(dataset_dir, cfg.MSEED_NOISE_DIR), stream_file)
        #print "[tfrecords negatives] Loading Stream {}".format(stream_file)
        st_event = read(stream_path)
        #print '[tfrecords negatives] Preprocessing stream'
        st_event = preprocess_stream(st_event)

        #cluster_id = filtered_catalog.cluster_id.values[event_n]
        cluster_id = -1 #We work with only one location for the moment (cluster id = 0)
        n_traces = len(st_event)
        if utils.check_stream(st_event, cfg):
            #print("[tfrecords negatives] Writing sample with dimensions "+str(cfg.WINDOW_SIZE)+"x"+str(st_event[0].stats.sampling_rate)+"x"+str(n_traces))
            # Write tfrecords
            writer.write(st_event, cluster_id) 
            
    # Cleanup writer
    print("[tfrecords negatives] Number of events written={}".format(writer._written))
    writer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file_path",type=str,default="config_default.ini",
                        help="path to .ini file with all the parameters")
    parser.add_argument("--dataset_dir",type=str, default=None)
    parser.add_argument("--pattern",type=str, default="*.mseed")
    parser.add_argument("--output_dir",type=str, default=None)
    parser.add_argument("--file_name",type=str, default="negatives.tfrecords")

    args = parser.parse_args()
    cfg = config.Config(args.config_file_path)
    #If arguments not set, switch to default values in conf
    if args.dataset_dir is None:
        dataset_dir = cfg.DATASET_BASE_DIR
    else:
        dataset_dir = args.dataset_dir
    if args.output_dir is None:
        output_dir = dataset_dir
    else:
        output_dir = args.output_dir
    tf.app.run()
