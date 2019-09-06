#!/usr/bin/env python
# -------------------------------------------------------------------
# File Name : predict_from_stream.py
# Creation Date : 03-12-2016
# Last Modified : Sun Jan  8 13:33:08 2017
# Author: Thibaut Perol <tperol@g.harvard.edu>
# -------------------------------------------------------------------
""" Detect event and predict localization on a stream (mseed) of
continuous recording. This is the slow method. For fast detections
run bin/predict_from_tfrecords.py
e.g,
./bin/predict_from_stream.py --stream_path data/streams/GSOK029_12-2016.mseed
--checkpoint_dir model/convnetquake --n_clusters 6 --window_step 10 --output
output/december_detections --max_windows 8640
"""
import os
import setproctitle
import argparse

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
import shutil
import tqdm
import pandas as pd
import time

from obspy.core import read
import quakenet.models as models
from quakenet.data_pipeline import DataPipeline
#import quakenet.config as config
import config
from quakenet.data_io import load_stream
from quakenet.data_io import load_catalog
import sys
import utils
import fnmatch
from obspy.core.utcdatetime import UTCDateTime
import logging
import catalog

evaluation = False
truePositives = 0
falsePositives = 0
trueNegatives = 0
falseNegatives = 0

def customPlot(st, outfile, predictions, windowsMissed, true_positive_dic, false_positive_dic, false_negative_dic, showMissed=False, ):
    fig = plt.figure()

    st = st.select(component="Z")

    st.plot(fig=fig)
    #plt.axvline(x=obspyDateTime2PythonDateTime(timeP), linewidth=2, color='g')
    #plt.axvline(x=obspyDateTime2PythonDateTime(timeP+cfg.window_size), linewidth=2, color='g')
    #plt.axvline(x=obspyDateTime2PythonDateTime(timeP+cfg.WINDOW_AVOID_NEGATIVES), linewidth=2, color='g')

    total_time = st[-1].stats.endtime - st[0].stats.starttime
    max_windows = int((total_time - cfg.window_size) / cfg.window_step_predict)
    #print(max_windows)
    #for i in range(0, max_windows):
    #    plt.axvline(x=utils.obspyDateTime2PythonDateTime(st[0].stats.starttime+i*cfg.window_step_predict), linewidth=1, color='b', linestyle='dashed')



    #for prediction in predictions:
    #    plt.axvline(x=utils.obspyDateTime2PythonDateTime(prediction), linewidth=cfg.window_size, color='r', alpha=0.5)

    for prediction in true_positive_dic:
        plt.axvline(x=utils.obspyDateTime2PythonDateTime(prediction+cfg.window_size/2), linewidth=cfg.window_size, color='g', alpha=0.5)

    for prediction in false_positive_dic:
        plt.axvline(x=utils.obspyDateTime2PythonDateTime(prediction+cfg.window_size/2), linewidth=cfg.window_size, color='r', alpha=0.5)

    for prediction in false_negative_dic:
        plt.axvline(x=utils.obspyDateTime2PythonDateTime(prediction+cfg.window_size/2), linewidth=cfg.window_size, color='c', alpha=0.5)

    if showMissed:
        for windowMissed in windowsMissed:
            plt.axvline(x=utils.obspyDateTime2PythonDateTime(windowMissed+cfg.window_size/2), linewidth=cfg.window_size, color='y', alpha=0.5)

    #plt.show()
    fig.savefig(outfile)   # save the figure to file
    plt.close(fig) 


def main(args):    
    global evaluation

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(checkpoint_dir):
        print ("[classify] \033[91m ERROR!!\033[0m Missing directory "+checkpoint_dir+". Run step 4 first.")
        sys.exit(0)
    ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
    
    #Load model just once
    samples = {
            'data': tf.placeholder(tf.float32,
                                   shape=(1, cfg.win_size, cfg.n_traces),
                                   name='input_data'),
            'cluster_id': tf.placeholder(tf.int64,
                                         shape=(1,),
                                         name='input_label')
        }
    model = models.get(cfg.model, samples, cfg,
                       checkpoint_dir,
                       is_training=False)
    sess = tf.Session() 
    model.load(sess)
    print '[classify] Evaluating using model at step {}'.format(
            sess.run(model.global_step))

    stream_files = [file for file in os.listdir(stream_path) if
                    fnmatch.fnmatch(file, args.pattern)]

    if len(stream_files)==0:
        print ("[classify] \033[91m ERROR!!\033[0m No files match the file pattern "+args.pattern+".")
        sys.exit(0)

    for stream_file in stream_files:
    	stream_file_without_extension = os.path.split(stream_file)[-1].split(".mseed")[0]
        if args.catalog_path is None:
            metadata_path = os.path.join(stream_path, stream_file_without_extension+".csv")
            if os.path.isfile(metadata_path):
                print("[classify] Found groundtruth metadata in "+metadata_path+".")  
                cat = pd.read_csv(metadata_path)
                evaluation = True
            else:
                print("[classify] Not found groundtruth metadata in "+metadata_path+".")
                cat = None
        else:
            #cat = pd.read_csv(args.catalog_path)
            #stations = pd.read_csv(args.stations_path)
            #Load metadata
            cat = catalog.Catalog()
            cat.import_json(args.catalog_path)
            evaluation = True
        predictions = predict(stream_path, stream_file, sess, model, samples, cat)
        #stream_file_without_extension = os.path.split(stream_file)[-1].split(".mseed")[0]
        #metadata_path = os.path.join(args.stream_path, stream_file_without_extension+".csv")
        #if os.path.isfile(metadata_path):
            #print("Found groundtruth metadata in "+metadata_path+".")  
            #cat = pd.read_csv(metadata_path)
            #for idx, start_time in enumerate(predictions["start_time"]):
            #    filtered_catalog = cat[
            #        ((cat.start_time >= predictions["start_time"][idx])
            #        & (cat.end_time <= predictions["end_time"][idx]))]
            #    print(str(len(filtered_catalog["start_time"])))   
        #else:
        #    print("Not found groundtruth metadata in "+metadata_path+".")     
        #cat = load_catalog(metadata_path)
        #cat = filter_catalog(cat)
    sess.close()

    if evaluation:
        print("[classify] true positives = "+str(truePositives))
        print("[classify] false positives = "+str(falsePositives))
        print("[classify] true negatives = "+str(trueNegatives))
        print("[classify] false negatives = "+str(falseNegatives))

        if truePositives+falsePositives>0:
            print("[classify] precission = "+str(100*float(truePositives)/(truePositives+falsePositives))+"%")
        else:
            print("[classify] cannot compute precission as truePositives+falsePositives == 0")

        if truePositives+falseNegatives>0:
            print("[classify] recall = "+str(100*float(truePositives)/(truePositives+falseNegatives))+"%")
        else:
            print("[classify] cannot compute recall as truePositives+falseNegatives == 0")

        if truePositives+falsePositives+trueNegatives+falseNegatives>0:
            print("[classify] accuracy = "+str(100*float(truePositives+trueNegatives)/(truePositives+falsePositives+trueNegatives+falseNegatives))+"%")
        else:
            print("[classify] cannot compute accuracy as truePositives+falsePositives+trueNegatives+falseNegatives == 0")


    
def predict(path, stream_file, sess, model, samples, cat):
    global truePositives
    global falsePositives
    global trueNegatives
    global falseNegatives

    # Load stream
    stream_path = path+"/"+stream_file #TODO join
    stream_file = os.path.split(stream_path)[-1]
    stream_file_without_extension = os.path.split(stream_file)[-1].split(".mseed")[0]
    print "[classify] Loading Stream {}".format(stream_file)
    stream = read(stream_path)
    print '[classify] Preprocessing stream'
    stream = utils.preprocess_stream(stream)


    #Select only the specified channels
    stream_select = utils.select_components(stream, cfg) 

    outputSubdir = os.path.join(output_dir, stream_file_without_extension)
    if os.path.exists(outputSubdir):
        shutil.rmtree(outputSubdir)
    os.makedirs(outputSubdir)
    outputSubdirSubplots = os.path.join(outputSubdir, "subPlots")    
    os.makedirs(outputSubdirSubplots) 
    os.makedirs(os.path.join(output_dir+"/"+stream_file_without_extension,"viz"))
    if cfg.save_sac:
        os.makedirs(os.path.join(output_dir+"/"+stream_file_without_extension,"sac"))

    #if args.metadata_path is not None: #This is groundtruth data
    #    print("Reading metadata file "+args.metadata_path)
    #    obspyCatalogMeta = seisobs.seis2cat(args.metadata_path) 

    # # TODO: change and look at all streams
    # stream_path = args.stream_path
    # stream_file = os.path.split(stream_path)[-1]
    # print " + Loading stream {}".format(stream_file)
    # stream = load_stream(stream_path)
    # print " + Preprocess stream"
    # stream = preprocess_stream(stream)
    # print " -- Stream is ready, starting detection"

    # Create catalog name in which the events are stored
    catalog_name = os.path.split(stream_file)[-1].split(".mseed")[0] + ".csv"
    output_catalog = os.path.join(output_dir, catalog_name)
    print '[classify] Catalog created to store events', output_catalog

    # Dictonary to store info on detected events
    events_dic ={"start_time": [],
                 "end_time": [],
                 "cluster_id": [],
                 "clusters_prob": []}

    true_positive_dic ={"start_time": [],
                 "end_time": [],
                 "cluster_id": [],
                 "clusters_prob": []}

    false_positive_dic ={"start_time": [],
                 "end_time": [],
                 "cluster_id": [],
                 "clusters_prob": []}
    false_negative_dic ={"start_time": [],
                 "end_time": [],
                 "cluster_id": [],
                 "clusters_prob": []}

    missed_dic ={"start_time": [],
                 "end_time": [],
                 "cluster_id": [],
                 "clusters_prob": []}

    # Windows generator
    win_gen = stream_select.slide(window_length=cfg.window_size,
                           step=cfg.window_step_predict,
                           include_partial_windows=False)

    total_time_in_sec = stream_select[0].stats.endtime - stream_select[0].stats.starttime
    max_windows = (total_time_in_sec - cfg.window_size) / cfg.window_step_predict

    

    step = tf.train.global_step(sess, model.global_step)


    n_events = 0
    time_start = time.time()

    #if stations is not None:
    #    station = stream_select[-1].stats.station
    #    stationLAT, stationLONG, stationDEPTH = utils.station_coordinates(station, stations)

    station = stream[0].stats.station
    stream_start_time = stream[0].stats.starttime
    stream_end_time = stream[-1].stats.endtime
    ptime = cat.getPtime(stream_start_time, stream_end_time, station)
    event_window_start = ptime - cfg.pwave_window/2
    event_window_end = ptime + cfg.pwave_window/2

    print("ptime="+str(ptime))
    print("event_window_start="+str(event_window_start)+"<->event_window_end="+str(event_window_end))

    try:
        for idx, win in enumerate(win_gen):
            #Check the groundtruth
            isPositive = False
            if cat is not None:
            	#print("win[0].stats.starttime ="+str(win[0].stats.starttime))
            	#print("win[0].stats.endtime ="+str(win[0].stats.endtime))
            	#print("cat.start_time[0] ="+str(cat.start_time[0]))
            	#print("cat.end_time[0] ="+str(cat.end_time[0]))

                window_start = win[0].stats.starttime
                window_end = win[-1].stats.endtime

                print("window: "+str(window_start)+"-"+str(window_end))

                if (window_start <= event_window_start) and (window_end >= event_window_end): #positive
                    isPositive = True
                    print("REAL POSITIVE")
                else:# negative
                    isPositive = False    
                    print("REAL NEGATIVE")  

                #if stations is not None:
                #    isPositive = utils.isPositive(window_start, window_end, cat, stationLAT, stationLONG, stationDEPTH, cfg.mean_velocity)
                #else:
                #    isPositive = utils.isPositive(window_start, window_end, cat)

                #Event window: [timeP-cfg.pwave_window..timeP+cfg.pwave_window]
                #Do not use negatives 

            	#for i in range(0, len(cat.start_time)):
	            #	if (UTCDateTime(cat.start_time[i]) >= UTCDateTime(win[0].stats.starttime)) and (UTCDateTime(cat.end_time[i]) <= UTCDateTime(win[0].stats.endtime)):# and (cat.end_time[0] <= win[0].stats.endtime):
		        #    	isPositive = True
		        #        #print("\033[92m isPositive = True\033[0m")
	            #    else:
	            #        isPositive = False
                         
            # Fetch class_proba and label
            to_fetch = [samples['data'], model.layers['class_prob'], model.layers['class_prediction']]
            # Feed window and fake cluster_id (needed by the net) but
            # will be predicted
            if utils.check_stream(win, cfg):
                feed_dict = {samples['data']: utils.fetch_window_data(win, cfg),
                            samples['cluster_id']: np.array([0])}
                sample, class_prob_, cluster_id = sess.run(to_fetch,
                                                        feed_dict)
            else:
                missed_dic["start_time"].append(win[0].stats.starttime)
                continue

            # # Keep only clusters proba, remove noise proba
            clusters_prob = class_prob_[0,1::]
            cluster_id -= 1

            # label for noise = -1, label for cluster \in {0:n_clusters}

            is_event = cluster_id[0] > -1

            if is_event:
                print("PREDICTED POSITIVE")
                n_events += 1
            else:
                print("PREDICTED NEGATIVE")

            # print "event {} ,cluster id {}".format(is_event,class_prob_)
            if is_event:
                events_dic["start_time"].append(win[0].stats.starttime)
                events_dic["end_time"].append(win[0].stats.endtime)
                events_dic["cluster_id"].append(cluster_id[0])
                events_dic["clusters_prob"].append(list(clusters_prob))
                if evaluation and isPositive:
	                #sys.stdout.write("\033[92m HIT\033[0m (positive)\n")
                    sys.stdout.write("\033[92mP\033[0m")
                    sys.stdout.flush()
                    truePositives = truePositives+1
                    true_positive_dic["start_time"].append(win[0].stats.starttime)
                    true_positive_dic["end_time"].append(win[0].stats.endtime)
                    true_positive_dic["cluster_id"].append(cluster_id[0])
                    true_positive_dic["clusters_prob"].append(list(clusters_prob))
                    #break
                elif evaluation:
	                #sys.stdout.write("\033[91m MISS\033[0m (false positive)\n")
                    sys.stdout.write("\033[91mP\033[0m")
                    sys.stdout.flush()
                    falsePositives = falsePositives+1
                    false_positive_dic["start_time"].append(win[0].stats.starttime)
                    false_positive_dic["end_time"].append(win[0].stats.endtime)
                    false_positive_dic["cluster_id"].append(cluster_id[0])
                    false_positive_dic["clusters_prob"].append(list(clusters_prob))
            else:
                if evaluation and isPositive:
                    #sys.stdout.write("\033[91m MISS\033[0m (false negative)\n")
                    sys.stdout.write("\033[91mN\033[0m")
                    sys.stdout.flush()
                    falseNegatives = falseNegatives+1
                    false_negative_dic["start_time"].append(win[0].stats.starttime)
                    false_negative_dic["end_time"].append(win[0].stats.endtime)
                    false_negative_dic["cluster_id"].append(cluster_id[0])
                    false_negative_dic["clusters_prob"].append(list(clusters_prob))
                elif evaluation:
	                #sys.stdout.write("\033[92m HIT\033[0m (negative)\n")
                    sys.stdout.write("\033[92mN\033[0m")
                    sys.stdout.flush()
                    trueNegatives = trueNegatives+1

            #if idx % 1000 ==0:
            #    print "\n[classify] Analyzing {} records".format(win[0].stats.starttime)

            if is_event:
                win_filtered = win.copy()
                #win_filtered.plot(outfile=os.path.join(output_dir+"/"+stream_file_without_extension,"viz",
                #                "event_{}_cluster_{}.png".format(idx,cluster_id)))

            if cfg.save_sac and is_event:
                win_filtered = win.copy()
                win_filtered.write(os.path.join(output_dir,"sac",
                        "event_{}_cluster_{}.sac".format(idx,cluster_id)),
                        format="SAC")

            if idx >= max_windows:
                print "[classify] stopped after {} windows".format(max_windows)
                print "[classify] found {} events".format(n_events)
                break

    except KeyboardInterrupt:
        print '[classify] Interrupted at time {}.'.format(win[0].stats.starttime)
        print "[classify] processed {} windows, found {} events".format(idx+1,n_events)
        print "[classify] Run time: ", time.time() - time_start

    df = pd.DataFrame.from_dict(events_dic)
    df.to_csv(output_catalog)

    #Plot everything
    customPlot(stream, output_dir+"/"+stream_file+"_"+str(idx)+".png", events_dic["start_time"], missed_dic["start_time"], true_positive_dic["start_time"], false_positive_dic["start_time"], false_negative_dic["start_time"])
    
    #Plot only 10min sections with events
    #max_secs_to_show = 600
    #win_gen = stream_select.slide(window_length=max_secs_to_show,
    #                      step=max_secs_to_show,
    #                       include_partial_windows=False)
    #for idx, win in enumerate(win_gen):
    #    customPlot(win, outputSubdirSubplots+"/win_"+str(idx)+".png", events_dic["start_time"], missed_dic["start_time"])
    #win = substream.slice(UTCDateTime(timeP), UTCDateTime(timeP) + cfg.window_size).copy()    
    print "\n[classify] Run time: ", time.time() - time_start

    return events_dic

if __name__ == "__main__":
    logging.getLogger("tensorflow").setLevel(logging.ERROR)

    print ("\033[92m******************** STEP 5/5. EVALUATION *******************\033[0m ")

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file_path",type=str, default=None,
                        help="path to .ini file with all the parameters")
    parser.add_argument("--stream_path",type=str, required=True)
    parser.add_argument("--pattern",type=str, default="*.mseed")
    parser.add_argument("--output_dir",type=str, required=True)
    parser.add_argument("--checkpoint_dir",type=str, required=True)
    parser.add_argument("--catalog_path",type=str, default=None) #For datos2, which have just one global catalog
    parser.add_argument("--stations_path",type=str, default=None) #For datos2, which have just one global catalog
    parser.add_argument("--debug",type=int, default=argparse.SUPPRESS) #Optional, we will use the value from the config file
    parser.add_argument("--window_size", type=int, required=True) #Optional, we will use the value from the config file
    parser.add_argument("--component_N",type=int, default=argparse.SUPPRESS) #Optional, we will use the value from the config file
    parser.add_argument("--component_E",type=int, default=argparse.SUPPRESS) #Optional, we will use the value from the config file    
    parser.add_argument("--n_clusters",type=int, default=argparse.SUPPRESS) #Optional, we will use the value from the config file 
    #parser.add_argument("--redirect_stdout_stderr",type=bool, default=False)

    args = parser.parse_args()

    cfg = config.Config(args)


    checkpoint_dir = args.checkpoint_dir
    output_dir = args.output_dir
    stream_path = args.stream_path

    #if args.redirect_stdout_stderr:
    #    stdout_stderr_file = open(os.path.join(output_dir, 'stdout_stderr_file.txt'), 'w')
    #    sys.stdout = stderr = stdout_stderr_file
    
    main(args)

    #if args.redirect_stdout_stderr:  
    #    stdout_stderr_file.close()

