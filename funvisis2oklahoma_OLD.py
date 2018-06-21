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

def preprocess_stream(stream):
    stream = stream.detrend('constant')
    return stream.normalize()

def write_json(metadata,output_metadata):
    with open(output_metadata, 'w') as outfile:
        json.dump(metadata, outfile)

def main(args):

    stream_dir = "funvisis/mseed"
    output_mseed_dir = "funvisis/funvisis2oklahoma/mseed"
    output_png_dir = "funvisis/funvisis2oklahoma/png"

    stream_files = [file for file in os.listdir(stream_dir) if
                    fnmatch.fnmatch(file, '*.MAN___161')]
    print "List of streams to anlayze", stream_files

    # Create dir to store oklahoma style mseed
    if not os.path.exists(output_mseed_dir):
        os.makedirs(output_mseed_dir)
    if not os.path.exists(output_png_dir):
        os.makedirs(output_png_dir)

    for stream_file in stream_files:
        print("Processing stream "+stream_file)
        # Load stream
        stream_path = os.path.join(stream_dir, stream_file)
        print "+ Loading Stream {}".format(stream_file)
        stream = read(stream_path)
        print '+ Preprocessing stream'
        stream = preprocess_stream(stream)
        total_time = stream[-1].stats.endtime - stream[0].stats.starttime
        print "total time {}s".format(total_time)
        print(stream[-1].stats.starttime)
        print(stream[0].stats.endtime)


        #debug: plot all
        substream = stream.select(station="CUM*")
        substream.plot(outfile=output_png_dir+"/"+stream_file+".png")

        print ("Saving file "+output_mseed_dir+"/"+stream_file+".mseed")
        substream.write(output_mseed_dir+"/"+stream_file+".mseed", format="MSEED") 


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("--stream_dir",type=str,default=None,
    #                    help="path to mseed to analyze")
    args = parser.parse_args()
    main(args)
