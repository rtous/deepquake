#!/usr/bin/env python
# -------------------------------------------------------------------
# File Name : funvisis2oklahoma.py
# Creation Date : 09-06-2018
# Last Modified : Mon Jan  9 13:21:32 2018
# Author: Ruben Tous <rtous@ac.upc.edu>
# -------------------------------------------------------------------
""""
1. splits the data of all the events into station-level mseed
2. Extracts windows noise from all the events
3. Saves .png for everything
e.g.,
funvisis2oklahoma.py \
--input_dir input \
--output_dir  output \
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
OUTPUT_MSEED_DIR = "funvisis2oklahoma/mseed"
OUTPUT_MSEED_EVENT_DIR = "funvisis2oklahoma/mseed_10s"
OUTPUT_MSEED_NOISE_DIR = "funvisis2oklahoma/mseed_noise"
OUTPUT_PNG_DIR = "funvisis2oklahoma/png"
OUTPUT_PNG_EVENT_DIR = "funvisis2oklahoma/png_10s"
OUTPUT_PNG_NOISE_DIR = "funvisis2oklahoma/png_noise"
WINDOW_SIZE = 10
WINDOW_STEP_NEGATIVES = 10
WINDOW_AVOID_NEGATIVES = 20

def preprocess_stream(stream):
    stream = stream.detrend('constant')
    return stream.normalize()

def write_json(metadata,output_metadata):
    with open(output_metadata, 'w') as outfile:
        json.dump(metadata, outfile)

def main(args):

    global INPUT_STREAM_DIR
    global INPUT_METADATA_DIR
    global OUTPUT_MSEED_DIR
    global OUTPUT_MSEED_EVENT_DIR
    global OUTPUT_MSEED_NOISE_DIR
    global OUTPUT_PNG_DIR
    global OUTPUT_PNG_EVENT_DIR
    global OUTPUT_PNG_NOISE_DIR

    INPUT_STREAM_DIR = args.input_dir+"/"+INPUT_STREAM_DIR
    INPUT_METADATA_DIR = args.input_dir+"/"+INPUT_METADATA_DIR
    OUTPUT_MSEED_DIR = args.output_dir+"/"+OUTPUT_MSEED_DIR
    OUTPUT_MSEED_EVENT_DIR = args.output_dir+"/"+OUTPUT_MSEED_EVENT_DIR
    OUTPUT_MSEED_NOISE_DIR = args.output_dir+"/"+OUTPUT_MSEED_NOISE_DIR
    OUTPUT_PNG_DIR = args.output_dir+"/"+OUTPUT_PNG_DIR
    OUTPUT_PNG_EVENT_DIR = args.output_dir+"/"+OUTPUT_PNG_EVENT_DIR
    OUTPUT_PNG_NOISE_DIR = args.output_dir+"/"+OUTPUT_PNG_NOISE_DIR

    stream_files = [file for file in os.listdir(INPUT_STREAM_DIR) if
                    fnmatch.fnmatch(file, '*.MAN___161')]
    print "List of streams to anlayze", stream_files

    # Create dir to store oklahoma style mseed
    if not os.path.exists(OUTPUT_MSEED_DIR):
        os.makedirs(OUTPUT_MSEED_DIR)
    if not os.path.exists(OUTPUT_PNG_DIR):
        os.makedirs(OUTPUT_PNG_DIR)
    if not os.path.exists(OUTPUT_MSEED_EVENT_DIR):
        os.makedirs(OUTPUT_MSEED_EVENT_DIR)
    if not os.path.exists(OUTPUT_PNG_EVENT_DIR):
        os.makedirs(OUTPUT_PNG_EVENT_DIR)
    if not os.path.exists(OUTPUT_MSEED_NOISE_DIR):
        os.makedirs(OUTPUT_MSEED_NOISE_DIR)
    if not os.path.exists(OUTPUT_PNG_NOISE_DIR):
        os.makedirs(OUTPUT_PNG_NOISE_DIR)

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
                win.plot(outfile=OUTPUT_PNG_EVENT_DIR+"/"+stream_file+"_"+station_code+".png")
                print ("Saving file "+OUTPUT_MSEED_EVENT_DIR+"/"+stream_file+"_"+station_code+".mseed")
                win.write(OUTPUT_MSEED_EVENT_DIR+"/"+stream_file+"_"+station_code+".mseed", format="MSEED") 

                #Save noise windows (exclude from P wave and 20s later)
                win_gen = substream.slide(window_length=WINDOW_SIZE,
                           step=WINDOW_STEP_NEGATIVES,
                           include_partial_windows=False)
                total_time = substream[0].stats.endtime - substream[0].stats.starttime
                max_windows = (total_time - WINDOW_SIZE) / WINDOW_STEP_NEGATIVES
                for idx, win in enumerate(win_gen):
                    window_start = win[0].stats.starttime.timestamp
                    window_end = win[-1].stats.endtime.timestamp
                    if ((window_start < timeP and window_end < timeP)
                        or
                        (window_start > timeP+WINDOW_AVOID_NEGATIVES)
                        ):
                        print("Noise window selected")
                        print ("Saving file "+OUTPUT_MSEED_NOISE_DIR+"/"+stream_file+"_"+station_code+"_noise"+str(idx)+".mseed")
                        win.write(OUTPUT_MSEED_NOISE_DIR+"/"+stream_file+"_"+station_code+"_noise"+str(idx)+".mseed", format="MSEED") 
                        win.plot(outfile=OUTPUT_PNG_NOISE_DIR+"/"+stream_file+"_"+station_code+"_noise"+str(idx)+".png")
                    else:
                        print("Noise window avoided: "+stream_file+"_"+station_code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir",type=str,default="input",
                        help="path to mseed to analyze")
    parser.add_argument("--output_dir",type=str,default="output",
                        help="path to mseed to analyze")
    args = parser.parse_args()
    main(args)
