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
import seisobs #https://github.com/d-chambers/seisobs

INPUT_STREAM_DIR = "funvisis/mseed"
INPUT_METADATA_DIR = "funvisis/sfiles_nordicformat"
OUTPUT_MSEED_DIR = "funvisis/funvisis2oklahoma/mseed"
OUTPUT_PNG_DIR = "funvisis/funvisis2oklahoma/png"
WINDOW_SIZE = 10

def preprocess_stream(stream):
    stream = stream.detrend('constant')
    return stream.normalize()

def write_json(metadata,output_metadata):
    with open(output_metadata, 'w') as outfile:
        json.dump(metadata, outfile)

def main(args):

    

    stream_files = [file for file in os.listdir(INPUT_STREAM_DIR) if
                    fnmatch.fnmatch(file, '*.MAN___161')]
    print "List of streams to anlayze", stream_files

    # Create dir to store oklahoma style mseed
    if not os.path.exists(OUTPUT_MSEED_DIR):
        os.makedirs(OUTPUT_MSEED_DIR)
    if not os.path.exists(OUTPUT_PNG_DIR):
        os.makedirs(OUTPUT_PNG_DIR)

    metadata_files = [file for file in os.listdir(INPUT_METADATA_DIR) if
                    fnmatch.fnmatch(file, '*')]
    for metadata_file in metadata_files:
        #1. Process metadata
        print("Reading metadata file "+os.path.join(INPUT_METADATA_DIR, metadata_file))
        obspyCatalogMeta = seisobs.seis2cat(os.path.join(INPUT_METADATA_DIR, metadata_file)) 
        eventOriginTime = obspyCatalogMeta.events[0].origins[0].time
        

        #yearStr = "%04d" % eventOriginTime.year
        #monthStr = "%02d" % eventOriginTime.month
        #dayStr = "%02d" % eventOriginTime.day
        #hourStr = "%02d" % eventOriginTime.hour
        #minuteStr = "%02d" % eventOriginTime.minute
        # print(yearStr+"-"+monthStr+"-"+dayStr+
        #    "-"+hourStr+minuteStr+"-00S.MAN___161")
        
        # metadata filename = 10-0517-00L.S201501
        # mseedFileName = 2015-02-14-1027-00S.MAN___161
        mseedFileName = metadata_file.split(".")[1][1:5]+"-"+metadata_file.split(".")[1][5:7]+"-"+metadata_file.split(".")[0][:-1]+"S.MAN___161"

        processMseed(mseedFileName, obspyCatalogMeta)


def processMseed(stream_file, obspyCatalogMeta):
        #2. Process .mseed
        print("Processing stream "+stream_file)
        # Load stream
        stream_path = os.path.join(INPUT_STREAM_DIR, stream_file)
        print "+ Loading Stream {}".format(stream_file)
        stream = read(stream_path)
        print '+ Preprocessing stream'
        stream = preprocess_stream(stream)
        total_time = stream[-1].stats.endtime - stream[0].stats.starttime
        print "total time {}s".format(total_time)
        print(stream[-1].stats.starttime)
        print(stream[0].stats.endtime)

        #debug: plot all
        for pick in obspyCatalogMeta.events[0].picks:
            if pick.phase_hint == 'P':
                station_code = pick.waveform_id.station_code
                print("Processing sample from "+stream_file+" and station"+station_code)
                substream = stream.select(station=station_code)
                substream.plot(outfile=OUTPUT_PNG_DIR+"/"+stream_file+"_"+station_code+".png")
                print ("Saving file "+OUTPUT_MSEED_DIR+"/"+stream_file+"_"+station_code+".mseed")
                substream.write(OUTPUT_MSEED_DIR+"/"+stream_file+"_"+station_code+".mseed", format="MSEED") 

                #Now a 10s window from the P wave
                timeP = pick.time
                print("P time = "+str(timeP))
                win = substream.slice(UTCDateTime(timeP), UTCDateTime(timeP) + WINDOW_SIZE).copy()
                win.plot(outfile=OUTPUT_PNG_DIR+"_10s/"+stream_file+"_"+station_code+".png")
                print ("Saving file "+OUTPUT_MSEED_DIR+"_10s/"+stream_file+"_"+station_code+".mseed")
                win.write(OUTPUT_MSEED_DIR+"_10s/"+stream_file+"_"+station_code+".mseed", format="MSEED") 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    #parser.add_argument("--stream_dir",type=str,default=None,
    #                    help="path to mseed to analyze")
    args = parser.parse_args()
    main(args)
