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
import config as config

def preprocess_stream(stream):
    stream = stream.detrend('constant')
    return stream.normalize()

def main(args):

    stream_files = [file for file in os.listdir(cfg.INPUT_STREAM_DIR) if
                    fnmatch.fnmatch(file, '*.MAN___161')]
    print "List of streams to anlayze", stream_files

    # Create dir to store oklahoma style mseed
    if not os.path.exists(cfg.OUTPUT_MSEED_DIR):
        os.makedirs(cfg.OUTPUT_MSEED_DIR)
    if not os.path.exists(cfg.OUTPUT_PNG_DIR):
        os.makedirs(cfg.OUTPUT_PNG_DIR)
    if not os.path.exists(cfg.OUTPUT_MSEED_EVENT_DIR):
        os.makedirs(cfg.OUTPUT_MSEED_EVENT_DIR)
    if not os.path.exists(cfg.OUTPUT_PNG_EVENT_DIR):
        os.makedirs(cfg.OUTPUT_PNG_EVENT_DIR)
    if not os.path.exists(cfg.OUTPUT_MSEED_NOISE_DIR):
        os.makedirs(cfg.OUTPUT_MSEED_NOISE_DIR)
    if not os.path.exists(cfg.OUTPUT_PNG_NOISE_DIR):
        os.makedirs(cfg.OUTPUT_PNG_NOISE_DIR)

    metadata_files = [file for file in os.listdir(cfg.INPUT_METADATA_DIR) if
                    fnmatch.fnmatch(file, '*')]
    for metadata_file in metadata_files:
        #1. Process metadata
        print("Reading metadata file "+os.path.join(cfg.INPUT_METADATA_DIR, metadata_file))
        obspyCatalogMeta = seisobs.seis2cat(os.path.join(cfg.INPUT_METADATA_DIR, metadata_file)) 
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
        stream_path = os.path.join(cfg.INPUT_STREAM_DIR, stream_file)
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
                substream.plot(outfile=cfg.OUTPUT_PNG_DIR+"/"+stream_file+"_"+station_code+".png")
                print ("Saving file "+cfg.OUTPUT_MSEED_DIR+"/"+stream_file+"_"+station_code+".mseed")
                substream.write(cfg.OUTPUT_MSEED_DIR+"/"+stream_file+"_"+station_code+".mseed", format="MSEED") 

                #Now a 10s window from the P wave
                timeP = pick.time
                print("P time = "+str(timeP))
                win = substream.slice(UTCDateTime(timeP), UTCDateTime(timeP) + cfg.WINDOW_SIZE).copy()
                win.plot(outfile=cfg.OUTPUT_PNG_EVENT_DIR+"/"+stream_file+"_"+station_code+".png")
                print ("Saving file "+cfg.OUTPUT_MSEED_EVENT_DIR+"/"+stream_file+"_"+station_code+".mseed")
                win.write(cfg.OUTPUT_MSEED_EVENT_DIR+"/"+stream_file+"_"+station_code+".mseed", format="MSEED") 

                #Save noise windows (exclude from P wave and 20s later)
                win_gen = substream.slide(window_length=cfg.WINDOW_SIZE,
                           step=cfg.WINDOW_STEP_NEGATIVES,
                           include_partial_windows=False)
                total_time = substream[0].stats.endtime - substream[0].stats.starttime
                max_windows = (total_time - cfg.WINDOW_SIZE) / cfg.WINDOW_STEP_NEGATIVES
                for idx, win in enumerate(win_gen):
                    window_start = win[0].stats.starttime.timestamp
                    window_end = win[-1].stats.endtime.timestamp
                    if ((window_start < timeP and window_end < timeP)
                        or
                        (window_start > timeP+cfg.WINDOW_AVOID_NEGATIVES)
                        ):
                        print("Noise window selected")
                        print ("Saving file "+cfg.OUTPUT_MSEED_NOISE_DIR+"/"+stream_file+"_"+station_code+"_noise"+str(idx)+".mseed")
                        win.write(cfg.OUTPUT_MSEED_NOISE_DIR+"/"+stream_file+"_"+station_code+"_noise"+str(idx)+".mseed", format="MSEED") 
                        win.plot(outfile=cfg.OUTPUT_PNG_NOISE_DIR+"/"+stream_file+"_"+station_code+"_noise"+str(idx)+".png")
                    else:
                        print("Noise window avoided: "+stream_file+"_"+station_code)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir",type=str,default=".",
                        help="path to mseed to analyze")
    args = parser.parse_args()

    cfg = config.Config(args.data_dir)

    main(args)
