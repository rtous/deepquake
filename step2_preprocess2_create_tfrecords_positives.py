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
import random


def preprocess_stream(stream):
    stream = stream.detrend('constant')
    return stream.normalize()


def main(_):
    print("[tfrecords positives] Converting .mseed files into tfrecords...")
    print("[tfrecords positives] Input directory: "+os.path.join(dataset_dir, cfg.mseed_event_dir))
    print("[tfrecords positives] Output directory: "+os.path.join(output_dir, cfg.output_tfrecords_dir_positives))
    print("[tfrecords positives] File pattern: "+args.pattern)

    stream_files = [file for file in os.listdir(os.path.join(dataset_dir, cfg.mseed_event_dir)) if
                    fnmatch.fnmatch(file, args.pattern)]
    total_positives = len(stream_files)
    print("[tfrecords positives] Matching files: "+str(len(stream_files)))
    
    
    # Divide training and validation datasets
    random.shuffle(stream_files)
    stream_files_train = stream_files[:int(0.8*total_positives)-1]
    print("[tfrecords positives] Number of windows for train: "+str(len(stream_files_train)))
    stream_files_validation = stream_files[int(0.8*total_positives):]
    print("[tfrecords positives] Number of windows for test: "+str(len(stream_files_validation)))

    # Create dir to store tfrecords
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    write(stream_files_train, "train")
    write(stream_files_validation, "test")

def write(stream_files, subfolder):

    if not os.path.exists(os.path.join(output_dir, subfolder)):
        os.makedirs(os.path.join(output_dir, subfolder))

    if not os.path.exists(os.path.join(os.path.join(output_dir, subfolder), cfg.output_tfrecords_dir_positives)):
        os.makedirs(os.path.join(os.path.join(output_dir, subfolder), cfg.output_tfrecords_dir_positives))

    # Write event waveforms and cluster_id in .tfrecords
    #output_name = "positives.tfrecords"  
    output_name = args.file_name
    output_path = os.path.join(os.path.join(os.path.join(output_dir, subfolder), cfg.output_tfrecords_dir_positives), output_name)
    writer = DataWriter(output_path)
    for stream_file in stream_files:

        stream_path = os.path.join(os.path.join(dataset_dir, cfg.mseed_event_dir), stream_file)
        #print "[tfrecords positives] Loading Stream {}".format(stream_file)
        st_event = read(stream_path)
        #print '[tfrecords positives] Preprocessing stream'
        st_event = preprocess_stream(st_event)  

        #Select only the specified channels
        st_event_select = utils.select_components(st_event, cfg) 

        #cluster_id = filtered_catalog.cluster_id.values[event_n]
        cluster_id = 0 #We work with only one location for the moment (cluster id = 0)

        n_traces = len(st_event_select)
        if utils.check_stream(st_event_select, cfg):
            #print("[tfrecords positives] Writing sample with dimensions "+str(cfg.WINDOW_SIZE)+"x"+str(st_event[0].stats.sampling_rate)+"x"+str(n_traces))
            # Write tfrecords
            writer.write(st_event_select, cluster_id) 

    # Cleanup writer
    print("[tfrecords positives] Number of windows written={}".format(writer._written))
    writer.close()

if __name__ == "__main__":
    print ("\033[92m******************** STEP 2/5. PREPROCESSING STEP 2/3. POSITIVE TRAINING WINDOWS -> TFRECORDS *******************\033[0m ")
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file_path",type=str,default=None,
                        help="path to .ini file with all the parameters")
    parser.add_argument("--prep_data_dir",type=str, required=True)
    parser.add_argument("--pattern",type=str, default="*.mseed")
    parser.add_argument("--tfrecords_dir",type=str, required=True)
    parser.add_argument("--component_N",type=int, default=argparse.SUPPRESS) #Optional, we will use the value from the config file
    parser.add_argument("--component_E",type=int, default=argparse.SUPPRESS) #Optional, we will use the value from the config file
    parser.add_argument("--file_name",type=str, default="positives.tfrecords")
    parser.add_argument("--window_size", type=int, required=True)
    parser.add_argument("--debug",type=int, default=argparse.SUPPRESS) #Optional, we will use the value from the config file
    #parser.add_argument("--redirect_stdout_stderr",type=bool, default=False)

    args = parser.parse_args()

    cfg = config.Config(args)
    
    dataset_dir = args.prep_data_dir
    output_dir = args.tfrecords_dir

    #if args.redirect_stdout_stderr:
    #    stdout_stderr_file = open(os.path.join(checkpoint_dir, 'stdout_stderr_file.txt'), 'w')
    #    sys.stdout = stderr = stdout_stderr_file

    tf.app.run()

    #if args.redirect_stdout_stderr:  
    #    stdout_stderr_file.close()   
