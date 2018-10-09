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
import catalog

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
    plt.axvline(x=obspyDateTime2PythonDateTime(timeP), linewidth=2, color='g')
    plt.axvline(x=obspyDateTime2PythonDateTime(timeP+cfg.window_size), linewidth=2, color='g')
    plt.axvline(x=obspyDateTime2PythonDateTime(timeP+cfg.window_avoid_negatives), linewidth=2, color='g')

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

def main(input_stream, input_metadata, output_dir, plot, onlyPattern, onlyStation):
    createDirectories(output_dir, plot)
    if os.path.isdir(input_stream):
        processDirectory(input_stream, input_metadata, output_dir, plot, pattern, onlyStation) 
    else:
        processSingleFile(input_stream, input_metadata, output_dir, plot, onlyStation)

def createDirectories(base_dir, plot):
    if not os.path.exists(os.path.join(base_dir, cfg.mseed_dir)):
        os.makedirs(os.path.join(base_dir, cfg.mseed_dir))
    if not os.path.exists(os.path.join(base_dir, cfg.mseed_event_dir)):
        os.makedirs(os.path.join(base_dir, cfg.mseed_event_dir))
    if not os.path.exists(os.path.join(base_dir, cfg.mseed_noise_dir)):
        os.makedirs(os.path.join(base_dir, cfg.mseed_noise_dir))
    if plot:
        if not os.path.exists(os.path.join(base_dir, cfg.png_dir)):
            os.makedirs(os.path.join(base_dir, cfg.png_dir))
        if not os.path.exists(os.path.join(base_dir, cfg.png_event_dir)):
            os.makedirs(os.path.join(base_dir, cfg.png_event_dir))
        if not os.path.exists(os.path.join(base_dir, cfg.png_noise_dir)):
            os.makedirs(os.path.join(base_dir, cfg.png_noise_dir))

def processSingleFile(input_stream, cat, output_dir, plot, onlyStation):    
    processMseed(input_stream, cat, output_dir, station, plot, onlyStation)

def processDirectory(input_stream_dir, cat, output_dir, plot, onlyPattern, onlyStation):
    stream_files = [file for file in os.listdir(input_stream_dir) if
                   fnmatch.fnmatch(file, onlyPattern)]
    if len(stream_files) == 0:
        print ("[obtain training windows] \033[91m ERROR!!\033[0m No files with .mseed extension with pattern "+onlyPattern+".")
        sys.exit(0)
    for mseedFileName in stream_files:
        processMseed(os.path.join(input_stream_dir, mseedFileName), cat, output_dir, plot, onlyStation)

def processMseed(stream_path, cat, output_dir, plot, onlyStation):
        stream_file = os.path.basename(stream_path)
        #2. Process .mseed
        #print("Processing stream "+stream_file)
        # Load stream
        print "[obtain training windows] Loading Stream {}".format(stream_file)
        stream = read(stream_path)
        print '[obtain training windows] Preprocessing stream'
        stream = preprocess_stream(stream)
        stream_start_time = stream[0].stats.starttime
        stream_end_time = stream[-1].stats.endtime
        total_time = stream_start_time - stream_end_time 

        z_streams = stream.select(component="Z")
        #if len(z_streams) > 1: #multiple stations, need to cut
        for z_stream in z_streams:
            #Slice the input stream horizontally, for one station
            station = z_stream.stats.station

            if onlyStation is not None and onlyStation != station: 
                    continue

            print ("[obtain training windows] ---------- Station "+station+" ---------")

            substream = stream.select(station=station)

            ptime = cat.getPtime(stream_start_time, stream_end_time, station)

            if ptime is not None:
                print ("[obtain training windows] Found event in the catalog: "+str(ptime))
        
                event_window_start = ptime - cfg.pwave_window/2
                event_window_end = ptime + cfg.pwave_window/2

                print ("[obtain training windows] Extracting full stream and saving into "+os.path.join(output_dir, cfg.mseed_dir)+"/"+stream_file+"_"+station+".mseed")

                if plot:
                    customPlot(substream, ptime, os.path.join(output_dir, cfg.png_dir)+"/"+utils.fileNameWithoutExtension(stream_file)+"_"+station+".png")
                substream.write(os.path.join(output_dir, cfg.mseed_dir)+"/"+utils.fileNameWithoutExtension(stream_file)+"_"+station+".mseed", format="MSEED") 

                #Slice the input stream vertically, by time
                sys.stdout.write("[obtain training windows] Extracting positive and negative windows and saving into "+output_dir+":\n")
                win_gen = substream.slide(window_length=cfg.window_size,
                           step=cfg.window_step_negatives,
                           include_partial_windows=False)
                total_time = substream[0].stats.endtime - substream[0].stats.starttime
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

                        #window_ptime = cat.getPtime(window_start, window_end, station)

                        if (window_start <= event_window_start) and (window_end >= event_window_end): #positive: #positive
                            win.write(os.path.join(output_dir, cfg.mseed_event_dir)+"/"+utils.fileNameWithoutExtension(stream_file)+"_"+station+"_"+str(idx)+".mseed", format="MSEED") 
                            if plot:
                                win.plot(outfile=os.path.join(output_dir, cfg.png_event_dir)+"/"+utils.fileNameWithoutExtension(stream_file)+"_"+station+"_"+str(idx)+".png")
                            sys.stdout.write("\033[92m.\033[0m")
                            num_positives = num_positives+1
                        elif (window_end < event_window_start-cfg.window_avoid_negatives) or (window_start > event_window_end+cfg.window_avoid_negatives):# negative
                            win.write(os.path.join(output_dir, cfg.mseed_noise_dir)+"/"+utils.fileNameWithoutExtension(stream_file)+"_"+station+"_noise"+str(idx)+".mseed", format="MSEED") 
                            if plot:
                                win.plot(outfile=os.path.join(output_dir, cfg.png_noise_dir)+"/"+utils.fileNameWithoutExtension(stream_file)+"_"+station+"_noise"+str(idx)+".png")
                            sys.stdout.write("\033[91m.\033[0m")
                            sys.stdout.flush()
                            num_negatives = num_negatives+1
                        else: # skipped
                            sys.stdout.write(".")
                            num_skipped = num_skipped+1
                    else:
                        sys.stdout.write("\033[93m.\033[0m")
                        sys.stdout.flush()
                        num_errors = num_errors+1
                print("\n[obtain training windows] "+str(num_positives)+" positive windows obtained.")
                print("[obtain training windows] "+str(num_negatives)+" negative windows obtained.")
                print("[obtain training windows] "+str(num_skipped)+" windows skipped (neither clear positive nor negative).")
                print("[obtain training windows] "+str(num_errors)+" windows discarded because of errors (config debug=True for details).")

            else:
                print ("[obtain training windows] \033[93m WARNING\033[0m No event detected at station "+station+" from "+stream_path+".")

            
if __name__ == "__main__":
    print ("\033[92m******************** STEP 1/5. PREPROCESSING STEP 1/3. OBTAIN TRAINING WINDOWS *******************\033[0m ")
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file_path",type=str,default="config_default.ini",
                        help="path to .ini file with all the parameters")
    parser.add_argument("--raw_data_dir",type=str)
    parser.add_argument("--catalog_path",type=str)
    parser.add_argument("--prep_data_dir",type=str)
    parser.add_argument("--plot",type=bool, default=False)
    parser.add_argument("--station",type=str, default=None)
    parser.add_argument("--pattern",type=str, default=None)
    args = parser.parse_args()

    cfg = config.Config(args.config_file_path)

    #Load metadata
    cat = catalog.Catalog()
    cat.import_json(args.catalog_path)

    if args.pattern is None:
        pattern = '*.mseed'
    else:
        pattern = args.pattern

    main(args.raw_data_dir, cat, args.prep_data_dir, args.plot, args.pattern, args.station)


   