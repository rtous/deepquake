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

OUTPUT_DIR = "output"

def preprocess_stream(stream):
    stream = stream.detrend('constant')
    return stream.normalize()

def main(args):
    # Create dir to store the plot
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    # Load stream
    stream_path = args.stream_path
    stream_file = os.path.split(stream_path)[-1]
    print "+ Loading Stream {}".format(stream_file)
    stream = read(stream_path)
    print '+ Preprocessing stream'
    stream = preprocess_stream(stream)

    total_time = stream[-1].stats.endtime - stream[0].stats.starttime
    print "total time {}s".format(total_time)

    #debug: plot all
    stream.plot(outfile=OUTPUT_DIR+"/stream.png")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream_path",type=str,default=None,
                        help="path to mseed to analyze")
    args = parser.parse_args()
    main(args)
