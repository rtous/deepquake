#!/usr/bin/env python
# -------------------------------------------------------------------
# File Name : convert_stream_to_tfrecords.py
# Creation Date : 09-12-2016
# Last Modified : Mon Jan  9 13:21:32 2017
# Author: Thibaut Perol <tperol@g.harvard.edu>
# -------------------------------------------------------------------
#TODO: Generating windows is embarassingly parallel. This can be speed up
""""
Load a stream, preprocess it, and create windows in tfrecords to be
fed to ConvNetQuake for prediction
NB: Use max_windows to create tfrecords of 1 week or 1 month
NB2: This convert a stream into ONE tfrecords, this is different
from create_dataset_events and create_dataset_noise that output
multiple tfrecords of equal size used for training.
e.g.,
./bin/preprocess/convert_stream_to_tfrecords.py \
--stream_path data/streams/GSOK029_7-2014.mseed \
--output_dir  data/tfrecord \
--window_size 10 --window_step 11 \
--max_windows 5000
"""
import os
import setproctitle
import numpy as np
from quakenet.data_pipeline import DataWriter
import tensorflow as tf
from obspy.core import read
from quakenet.data_io import load_catalog
from obspy.core.utcdatetime import UTCDateTime
import fnmatch
import json
import argparse
from tqdm import tqdm
import time
import pandas as pd
import utils

        
def read_stream(stream_path):
    print "+ Loading Stream {}".format(stream_path)
    stream = utils.read(stream_path)
    #print '+ Preprocessing stream'
    #stream = utils.preprocess_stream(stream)
    return stream

def main(args):
    stream_files = [file for file in os.listdir(args.input_dir_path) if
                    fnmatch.fnmatch(file, "*1Z")]

    for stream_file in stream_files:
        stream_file_without_component_code = stream_file[0:-2]
        try:
	        streamHHN = read_stream(args.input_dir_path+"/"+stream_file_without_component_code+"2N")
	        streamHHE = read_stream(args.input_dir_path+"/"+stream_file_without_component_code+"3E")
	        streamHHZ = read_stream(args.input_dir_path+"/"+stream_file_without_component_code+"1Z")
	        resultStream = streamHHN
	        resultStream += streamHHE
	        resultStream += streamHHZ
	        target_path =args.output_dir_path+"/"+stream_file[0:-3]+".mseed"
	        print("writing to "+target_path)
	        resultStream.write(target_path, format="MSEED") 
        except Exception, err:
	        print Exception, err
	        print("\033[91m ERROR:\033[0m Failed to join components")

if __name__ == "__main__":
	#python util_join_components_many.py --input_dir_path=/Users/rtous/Downloads/DeteccionSismos/Datos_full/datos_carabobo --output_dir_path=/Users/rtous/DockerVolume/data/deepquake/datos5/mseed
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir_path",type=str, default=None,
                        help="path to directory with separate files for each component")
    parser.add_argument("--output_dir_path",type=str, default=None,
                        help="path to output mseed")
    args = parser.parse_args()
    main(args)
