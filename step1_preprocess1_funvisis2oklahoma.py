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

def main(input_stream, input_metadata, output_dir, pattern, station, plot_station, plot_positives, plot_negatives):
    createDirectories(output_dir, plot_station, plot_positives, plot_negatives)
    if os.path.isdir(input_stream):
        processDirectory(input_stream, input_metadata, output_dir, pattern, station, plot_station, plot_positives, plot_negatives) 
    else:
        processSingleFile(input_stream, input_metadata, output_dir, station, plot_station, plot_positives, plot_negatives)

def createDirectories(base_dir, plot_station, plot_positives, plot_negatives):
    if not os.path.exists(os.path.join(base_dir, cfg.mseed_dir)):
        os.makedirs(os.path.join(base_dir, cfg.mseed_dir))
    if plot_station:
        if not os.path.exists(os.path.join(base_dir, cfg.png_dir)):
            os.makedirs(os.path.join(base_dir, cfg.png_dir))
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

def processSingleFile(input_stream, input_metadata, output_dir, station, plot_station, plot_positives, plot_negatives):
    #1. Process metadata
    print("[obtain training windows] Reading metadata file "+input_metadata)
    obspyCatalogMeta = seisobs.seis2cat(input_metadata) 
    eventOriginTime = obspyCatalogMeta.events[0].origins[0].time
    processMseed(input_stream, obspyCatalogMeta, output_dir, station, plot_station, plot_positives, plot_negatives)

def processDirectory(input_stream_dir, input_metadata_dir, output_dir, pattern, station, plot_station, plot_positives, plot_negatives): 
    #os.path.join(output_dir, cfg.png_noise_dir)
    #stream_files = [file for file in os.listdir(input_stream_dir) if
    #                fnmatch.fnmatch(file, '*.MAN___161')]
    #print "List of streams to anlayze", stream_files

    metadata_files = [file for file in os.listdir(input_metadata_dir) if
                    fnmatch.fnmatch(file, pattern)]
    print "[obtain training windows] List of metadata files to anlayze: ", metadata_files
    for metadata_file in metadata_files:
        #1. Process metadata
        print("[obtain training windows] Reading metadata file "+os.path.join(input_metadata_dir, metadata_file))
        obspyCatalogMeta = seisobs.seis2cat(os.path.join(input_metadata_dir, metadata_file)) 
        eventOriginTime = obspyCatalogMeta.events[0].origins[0].time
        mseedFileName = metadata_file.split(".")[1][1:5]+"-"+metadata_file.split(".")[1][5:7]+"-"+metadata_file.split(".")[0][:-1]+"S.MAN___161"
        processMseed(os.path.join(input_stream_dir, mseedFileName), obspyCatalogMeta, output_dir, station, plot_station, plot_positives, plot_negatives)

def processMseed(stream_path, obspyCatalogMeta, output_dir, station, plot_station, plot_positives, plot_negatives):
        stream_file = os.path.basename(stream_path)
        #2. Process .mseed
        #print("Processing stream "+stream_file)
        # Load stream
        print "[obtain training windows] Loading Stream {}".format(stream_file)
        stream = read(stream_path)
        print '[obtain training windows] Preprocessing stream'
        stream = preprocess_stream(stream)
        total_time = stream[-1].stats.endtime - stream[0].stats.starttime
        #print "total time {}s".format(total_time)
        #print(stream[-1].stats.starttime)
        #print(stream[0].stats.endtime)


        for pick in obspyCatalogMeta.events[0].picks:
            if pick.phase_hint == 'P':
                timeP = pick.time
                station_code = pick.waveform_id.station_code
                if station is not None and station != station_code: #just for debugging (arg --station)
                    continue
                print ("[obtain training windows] ---------- Station "+station_code+" ---------")
                print ("[obtain training windows] Extracting full stream and saving into "+os.path.join(output_dir, cfg.mseed_dir)+"/"+stream_file+"_"+station_code+".mseed")
                
                #Slice the input stream horizontally, for one station
                substream = stream.select(station=station_code)
                if plot_station:
                    customPlot(substream, timeP, os.path.join(output_dir, cfg.png_dir)+"/"+stream_file+"_"+station_code+".png")
                substream.write(os.path.join(output_dir, cfg.mseed_dir)+"/"+stream_file+"_"+station_code+".mseed", format="MSEED") 

                event_window_start = timeP - cfg.pwave_window/2
                event_window_end = timeP + cfg.pwave_window/2

                # Create catalog name in which the events are stored
                output_catalog = os.path.join(output_dir, cfg.mseed_dir)+"/"+stream_file+"_"+station_code+".csv"
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
                    if utils.check_stream(win, cfg):
                        window_start = win[0].stats.starttime.timestamp
                        window_end = win[-1].stats.endtime.timestamp

                        #Event window: [timeP-cfg.pwave_window..timeP+cfg.pwave_window]
                        #Do not use negatives 
                        if (window_start <= event_window_start) and (window_end >= event_window_end): #positive
                            win.write(os.path.join(output_dir, cfg.mseed_event_dir)+"/"+stream_file+"_"+station_code+"_"+str(idx)+".mseed", format="MSEED") 
                            if plot_positives:
                                win.plot(outfile=os.path.join(output_dir, cfg.png_event_dir)+"/"+stream_file+"_"+station_code+".png")
                            sys.stdout.write("\033[92m.\033[0m")
                            num_positives = num_positives+1
                        elif (window_end < event_window_start-cfg.window_avoid_negatives) or (window_start > event_window_end+cfg.window_avoid_negatives):# negative
                            win.write(os.path.join(output_dir, cfg.mseed_noise_dir)+"/"+stream_file+"_"+station_code+"_noise"+str(idx)+".mseed", format="MSEED") 
                            if plot_negatives:
                                win.plot(outfile=os.path.join(output_dir, cfg.png_noise_dir)+"/"+stream_file+"_"+station_code+"_noise"+str(idx)+".png")
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

if __name__ == "__main__":
    print ("\033[92m******************** STEP 1/5. PREPROCESSING STEP 1/3. OBTAIN TRAINING WINDOWS *******************\033[0m ")
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file_path",type=str,default="config_default.ini",
                        help="path to .ini file with all the parameters")
    parser.add_argument("--raw_data_dir",type=str)
    parser.add_argument("--raw_metadata_dir",type=str)
    parser.add_argument("--prep_data_dir",type=str)
    parser.add_argument("--station",type=str, default=None)
    parser.add_argument("--pattern",type=str, default=None,
                        help="filename pattern for the METADATA files to process.")
    parser.add_argument("--plot_station",type=bool, default=False)
    parser.add_argument("--plot_positives",type=bool, default=False)
    parser.add_argument("--plot_negatives",type=bool, default=False)
    #parser.add_argument("--redirect_stdout_stderr",type=bool, default=False)
    args = parser.parse_args()

    cfg = config.Config(args.config_file_path)

    #If arguments not set, switch to default values in conf
    input_stream = args.raw_data_dir
    input_metadata = args.raw_metadata_dir
    output_dir = args.prep_data_dir
    
    if args.pattern is None:
        pattern = '*'
    else:
        pattern = args.pattern

    main(input_stream, input_metadata, output_dir, pattern, args.station, args.plot_station, args.plot_positives, args.plot_negatives)

    #utils.save_json(
    #    data['people'].append({  
    #        'total_streams': 'Tim',
    #        'total_station_streams': 'apple.com',
    #        'total_positives': 'apple.com',
    #        'total_negatives': 'apple.com',
    #        'total_discarded': 'Alabama'
    #        }),
    #    os.path.join(output_dir, "output_obtain_training_windows.json")
    #)
