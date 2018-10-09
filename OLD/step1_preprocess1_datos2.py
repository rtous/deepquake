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
import sys
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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import obspy
import datetime as dt
import utils

#total_streams = 0
#total_station_streams = 0
#total_negatives = 0
#total_positives = 0
#total_discarded = 0
#total_time = 0

def preprocess_stream(stream):
    stream = stream.detrend('constant')
    return stream.normalize()

def obspyDateTime2PythonDateTime(odt):
    return dt.datetime(odt.year, odt.month, odt.day, odt.hour, odt.minute, odt.second)

def customPlot(st, timeP, outfile):
    fig = plt.figure()
    st.plot(fig=fig)
    plt.axvline(x=obspyDateTime2PythonDateTime(timeP), linewidth=2, color='r')
    #plt.axvline(x=obspyDateTime2PythonDateTime(timeP+cfg.window_avoid_negatives), linewidth=2, color='g')

    total_time = st[-1].stats.endtime - st[0].stats.starttime
    max_windows = int((total_time - cfg.window_size) / cfg.window_step_negatives)
    #print(max_windows)
    for i in range(0, max_windows):
        plt.axvline(x=obspyDateTime2PythonDateTime(st[0].stats.starttime+i*cfg.window_step_negatives), linewidth=1, color='r', linestyle='dashed')
    #plt.show()
    fig.savefig(outfile)   # save the figure to file
    plt.close(fig) 

def customPlotPureMatplotlib(st, timeP):
    tr = st[0]
    data = tr.data
    npts = tr.stats.npts
    samprate = tr.stats.sampling_rate
    times = [(tr.stats.starttime + t).datetime for t in tr.times()]
    plt.plot(times, tr.data)
    #xpoints = np.arange(0, npts / samprate, 1 / samprate)
    #plt.plot(xpoints, tr.data, 'k')
    
    #plt.plot(t, data_envelope, 'k:')
    plt.title(tr.stats.starttime)
    plt.ylabel('Filtered Data w/ Envelope')
    plt.xlabel('Time [s]')
    #plt.xlim(0, 2000)
    #plt.xlim(80, 90)
    #plt.axvline(x=0.22058956)
    #plt.axvline(x=0, linewidth=1, color='r', linestyle='dashed')
    #plt.axvline(x=0.1, linewidth=1, color='r', linestyle='dashed')
    for i in range(10):
        plt.axvline(x=i*50, linewidth=1, color='r', linestyle='dashed')
    plt.grid()
    plt.legend()
    plt.show()

def main(input_stream, input_metadata_dir, output_dir, pattern, plot_positives, plot_negatives, catalog_path, stations_path):
    #cat = pd.read_csv(catalog_path)
    #stations = pd.read_csv(stations_path)
    createDirectories(output_dir, plot_positives, plot_negatives)
    processDirectory(input_stream, input_metadata_dir, output_dir, pattern, plot_positives, plot_negatives) 
    

def createDirectories(base_dir, plot_positives, plot_negatives):
    if not os.path.exists(os.path.join(base_dir, cfg.mseed_dir)):
        os.makedirs(os.path.join(base_dir, cfg.mseed_dir))
    if not os.path.exists(os.path.join(base_dir, cfg.mseed_event_dir)):
        os.makedirs(os.path.join(base_dir, cfg.mseed_event_dir))
    if plot_positives:
        if not os.path.exists(os.path.join(base_dir, cfg.png_event_dir)):
            os.makedirs(os.path.join(base_dir, cfg.png_event_dir))
    if not os.path.exists(os.path.join(base_dir, cfg.mseed_noise_dir)):
        os.makedirs(os.path.join(base_dir, cfg.mseed_noise_dir))
    if plot_negatives:
        if not os.path.exists(os.path.join(base_dir, cfg.png_noise_dir)):
            os.makedirs(os.path.join(base_dir, cfg.png_noise_dir))
    if not os.path.exists(os.path.join(base_dir, cfg.png_dir)):
            os.makedirs(os.path.join(base_dir, cfg.png_dir))

#def processSingleFile(input_stream, output_dir, plot_positives, plot_negatives, cat, stations):
#    processMseed(input_stream, output_dir, plot_positives, plot_negatives, cat, stations)

def processDirectory(input_stream_dir, input_metadata_dir, output_dir, pattern, plot_positives, plot_negatives): 
    #input_stream_files = [file for file in os.listdir(input_stream_dir) if
    #                fnmatch.fnmatch(file, pattern)]
    
    metadata_files = [file for file in os.listdir(input_metadata_dir) if
                    fnmatch.fnmatch(file, "*")]
    print "[obtain training windows] List of metadata files to anlayze: ", metadata_files
    for metadata_file in metadata_files:
        #1. Process metadata
        print("[obtain training windows] Reading metadata file "+os.path.join(input_metadata_dir, metadata_file))
        obspyCatalogMeta = seisobs.seis2cat(os.path.join(input_metadata_dir, metadata_file)) 
        #eventOriginTime = obspyCatalogMeta.events[0].origins[0].time
        
        mseedFileNamePattern = metadata_file.split(".")[1][1:5]+"-"+metadata_file.split(".")[1][5:7]+"-"+metadata_file.split(".")[0][0:2]+"-"+metadata_file.split(".")[0][3:7]+"*"
        print("mseedFileNamePattern="+mseedFileNamePattern)

        #mseedFileNamePattern = metadata_file.split(".")[0]+"*.mseed"
        
        input_stream_files = [file for file in os.listdir(input_stream_dir) if 
            fnmatch.fnmatch(file, mseedFileNamePattern)]

        for mseedFileName in input_stream_files:
            processMseed(os.path.join(input_stream_dir, mseedFileName), obspyCatalogMeta, output_dir, True, plot_positives, plot_negatives)

def processMseed(stream_path, obspyCatalogMeta, output_dir, plot_station, plot_positives, plot_negatives):
        stream_file = os.path.basename(stream_path)
        #2. Process .mseed
        print("Processing stream "+stream_file)
        # Load stream
        print "[obtain training windows] Loading Stream {}".format(stream_file)
        stream = read(stream_path)
        print '[obtain training windows] Preprocessing stream'
        stream = preprocess_stream(stream)
        total_time = stream[-1].stats.endtime - stream[0].stats.starttime

        station = stream[-1].stats.station

        print("Processing station "+station)

        #stationLAT, stationLONG, stationDEPTH = utils.station_coordinates(station, stations)
        

        #timeP, eventTime = utils.getPtime(stream[0].stats.starttime, stream[-1].stats.endtime, cat, stationLAT, stationLONG, stationDEPTH, cfg.mean_velocity)
        #if timeP != None:
        timeP = utils.getPtimeFromObsPyCat(obspyCatalogMeta, station)
        
        print("Trying to plot "+stream_file+" with timeP = "+str(timeP))
        customPlot(stream, timeP, os.path.join(output_dir, cfg.png_dir)+"/"+stream_file+".png") 

        #print "total time {}s".format(total_time)
        #print(stream[-1].stats.starttime)
        #print(stream[0].stats.endtime)


        event_window_start = timeP - cfg.pwave_window/2
        event_window_end = timeP + cfg.pwave_window/2

        # Create catalog name in which the events are stored
        output_catalog = os.path.join(output_dir, cfg.mseed_dir)+"/"+stream_file+".csv"
        events_dic ={"start_time": [],
         "end_time": [],
         "cluster_id": [],
         "clusters_prob": []}
        events_dic["start_time"].append(UTCDateTime(timeP) - cfg.pwave_window/2)
        events_dic["end_time"].append(UTCDateTime(timeP) + cfg.pwave_window/2)
        events_dic["cluster_id"].append(0) #TODO
        events_dic["clusters_prob"].append(1) #manually annotated event
        df = pd.DataFrame.from_dict(events_dic)
        df.to_csv(output_catalog)
        cat = pd.read_csv(output_catalog)


        #Slice the input stream horizontally, by time
        sys.stdout.write("[obtain training windows] Extracting positive and negative windows and saving into "+output_dir+":\n")
        win_gen = stream.slide(window_length=cfg.window_size,
                   step=cfg.window_step_negatives,
                   include_partial_windows=False)
        total_time = stream[0].stats.endtime - stream[0].stats.starttime
        max_windows = (total_time - cfg.window_size) / cfg.window_step_negatives
        num_negatives = 0
        num_positives = 0
        num_errors = 0
        num_skipped = 0
        for idx, win in enumerate(win_gen):
            if utils.check_stream(win, cfg, False):
                window_start = win[0].stats.starttime.timestamp
                window_end = win[-1].stats.endtime.timestamp

                #Event window: [timeP-cfg.pwave_window..timeP+cfg.pwave_window]
                #Do not use negatives 

                if (utils.isPositiveKnownP(window_start, window_end, cat)): #positive
                    win.write(os.path.join(output_dir, cfg.mseed_event_dir)+"/"+stream_file+"_"+str(idx)+".mseed", format="MSEED") 
                    if plot_positives:
                        win.plot(outfile=os.path.join(output_dir, cfg.png_event_dir)+"/"+stream_file+"_"+str(idx)+".png")
                    sys.stdout.write("\033[92m.\033[0m")
                    num_positives = num_positives+1
                else:# negative
                    win.write(os.path.join(output_dir, cfg.mseed_noise_dir)+"/"+stream_file+"_noise"+str(idx)+".mseed", format="MSEED") 
                    if plot_negatives:
                        win.plot(outfile=os.path.join(output_dir, cfg.png_noise_dir)+"/"+stream_file+"_noise"+str(idx)+".png")
                    sys.stdout.write("\033[91m.\033[0m")
                    sys.stdout.flush()
                    num_negatives = num_negatives+1
                #else: # skipped
                #    sys.stdout.write(".")
                #    num_skipped = num_skipped+1
                #TODO: We are not considering a window skipping gap
            else:
                sys.stdout.write("\033[93m.\033[0m")
                sys.stdout.flush()
                num_errors = num_errors+1

        print("\n[obtain training windows] "+str(num_positives)+" positive windows obtained.")
        print("[obtain training windows] "+str(num_negatives)+" negative windows obtained.")
        print("[obtain training windows] "+str(num_skipped)+" windows skipped (neither clear positive nor negative).")
        print("[obtain training windows] "+str(num_errors)+" windows discarded because of errors (config debug=True for details).")

if __name__ == "__main__":
    print ("\033[92m******************** STEP 1/5. PREPROCESSING STEP 1/3. OBTAIN TRAINING WINDOWS *******************\033[0m ")
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file_path",type=str,default="config_default.ini",
                        help="path to .ini file with all the parameters")
    parser.add_argument("--raw_data_dir",type=str)
    parser.add_argument("--raw_metadata_dir",type=str)
    parser.add_argument("--prep_data_dir",type=str)
    parser.add_argument("--pattern",type=str, default="*.mseed",
                        help="filename pattern for the METADATA files to process.")
    parser.add_argument("--plot_positives",type=bool, default=False)
    parser.add_argument("--plot_negatives",type=bool, default=False)
    parser.add_argument("--catalog_path",type=str) #For datos2, which have just one global catalog
    parser.add_argument("--stations_path",type=str)
    #parser.add_argument("--redirect_stdout_stderr",type=bool, default=False)
    args = parser.parse_args()

    cfg = config.Config(args.config_file_path)

    #If arguments not set, switch to default values in conf
    input_stream = args.raw_data_dir
    output_dir = args.prep_data_dir
    
    if args.pattern is None:
        pattern = '*'
    else:
        pattern = args.pattern

    main(input_stream, args.raw_metadata_dir, output_dir, pattern, args.plot_positives, args.plot_negatives, args.catalog_path, args.stations_path)

