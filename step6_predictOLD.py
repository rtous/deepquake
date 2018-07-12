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
import sys
import utils


def customPlot(st, outfile, predictions):
    fig = plt.figure()
    st.plot(fig=fig)
    #plt.axvline(x=obspyDateTime2PythonDateTime(timeP), linewidth=2, color='g')
    #plt.axvline(x=obspyDateTime2PythonDateTime(timeP+cfg.WINDOW_SIZE), linewidth=2, color='g')
    #plt.axvline(x=obspyDateTime2PythonDateTime(timeP+cfg.WINDOW_AVOID_NEGATIVES), linewidth=2, color='g')

    total_time = st[-1].stats.endtime - st[0].stats.starttime
    max_windows = int((total_time - cfg.WINDOW_SIZE) / cfg.WINDOW_STEP_PREDICT)
    print(max_windows)
    for i in range(0, max_windows):
        plt.axvline(x=utils.obspyDateTime2PythonDateTime(st[0].stats.starttime+i*cfg.WINDOW_STEP_PREDICT), linewidth=1, color='b', linestyle='dashed')

    for prediction in predictions:
        plt.axvline(x=utils.obspyDateTime2PythonDateTime(prediction), linewidth=cfg.WINDOW_SIZE, color='r', alpha=0.5)
    #plt.show()
    fig.savefig(outfile)   # save the figure to file
    plt.close(fig) 


def main(args):
    
    ckpt = tf.train.get_checkpoint_state(cfg.CHECKPOINT_DIR)
    

    #Load model just once
    samples = {
            'data': tf.placeholder(tf.float32,
                                   shape=(1, cfg.win_size, 3),
                                   name='input_data'),
            'cluster_id': tf.placeholder(tf.int64,
                                         shape=(1,),
                                         name='input_label')
        }
    model = models.get(cfg.model, samples, cfg,
                       cfg.CHECKPOINT_DIR,
                       is_training=False)
    sess = tf.Session() 
    model.load(sess)
    print 'Evaluating using model at step {}'.format(
            sess.run(model.global_step))

    stream_files = [file for file in os.listdir(args.stream_path) if
                    fnmatch.fnmatch(file, '*.mseed')]
    for stream_file in stream_files:
        predict(args.stream_path, stream_file, sess, model)

    sess.close()

    
def predict(path, stream_file, sess, model):
    setproctitle.setproctitle('quakenet_predict')

    if not os.path.exists(cfg.CHECKPOINT_DIR):
	    print ("\033[91m ERROR!!\033[0m Missing directory "+cfg.CHECKPOINT_DIR+". Run step 4 first.")
	    sys.exit(0)
    
    ckpt = tf.train.get_checkpoint_state(cfg.CHECKPOINT_DIR)

    # Remove previous output directory
    #if os.path.exists(cfg.OUTPUT_PREDICT_BASE_DIR):
    #    shutil.rmtree(cfg.OUTPUT_PREDICT_BASE_DIR)
    if not os.path.exists(cfg.OUTPUT_PREDICT_BASE_DIR):
        os.makedirs(cfg.OUTPUT_PREDICT_BASE_DIR)
    


    # Load stream
    stream_path = args.stream_path
    stream_file = os.path.split(stream_path)[-1]
    stream_file_without_extension = os.path.split(stream_file)[-1].split(".mseed")[0]
    print "+ Loading Stream {}".format(stream_file)
    stream = read(stream_path)
    print '+ Preprocessing stream'
    stream = utils.preprocess_stream(stream)

    os.makedirs(os.path.join(cfg.OUTPUT_PREDICT_BASE_DIR, stream_file_without_extension))
    os.makedirs(os.path.join(cfg.OUTPUT_PREDICT_BASE_DIR+"/"+stream_file_without_extension,"viz"))
    if cfg.save_sac:
        os.makedirs(os.path.join(cfg.OUTPUT_PREDICT_BASE_DIR+"/"+stream_file_without_extension,"sac"))

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
    output_catalog = os.path.join(cfg.OUTPUT_PREDICT_BASE_DIR, catalog_name)
    print 'Catalog created to store events', output_catalog

    # Dictonary to store info on detected events
    events_dic ={"start_time": [],
                 "end_time": [],
                 "cluster_id": [],
                 "clusters_prob": []}

    # Windows generator
    win_gen = stream.slide(window_length=cfg.WINDOW_SIZE,
                           step=cfg.WINDOW_STEP_PREDICT,
                           include_partial_windows=False)

    total_time_in_sec = stream[0].stats.endtime - stream[0].stats.starttime
    max_windows = (total_time_in_sec - cfg.WINDOW_SIZE) / cfg.WINDOW_STEP_PREDICT

    # stream data with a placeholder
    samples = {
            'data': tf.placeholder(tf.float32,
                                   shape=(1, cfg.win_size, 3),
                                   name='input_data'),
            'cluster_id': tf.placeholder(tf.int64,
                                         shape=(1,),
                                         name='input_label')
        }

    # set up model and validation metrics
    model = models.get(cfg.model, samples, cfg,
                       cfg.CHECKPOINT_DIR,
                       is_training=False)

    with tf.Session() as sess:

        model.load(sess)
        print 'Predicting using model at step {}'.format(
                sess.run(model.global_step))

        step = tf.train.global_step(sess, model.global_step)


        n_events = 0
        time_start = time.time()

        try:
            for idx, win in enumerate(win_gen):

                # Fetch class_proba and label
                to_fetch = [samples['data'],
                            model.layers['class_prob'],
                            model.layers['class_prediction']]
                # Feed window and fake cluster_id (needed by the net) but
                # will be predicted
                if utils.check_stream(win, cfg):
                    feed_dict = {samples['data']: utils.fetch_window_data(win, cfg),
                                samples['cluster_id']: np.array([0])}
                    sample, class_prob_, cluster_id = sess.run(to_fetch,
                                                            feed_dict)
                else:
                    continue

                # # Keep only clusters proba, remove noise proba
                clusters_prob = class_prob_[0,1::]
                cluster_id -= 1

                # label for noise = -1, label for cluster \in {0:n_clusters}

                is_event = cluster_id[0] > -1
                if is_event:
                    n_events += 1
                # print "event {} ,cluster id {}".format(is_event,class_prob_)

                if is_event:
                    events_dic["start_time"].append(win[0].stats.starttime)
                    events_dic["end_time"].append(win[0].stats.endtime)
                    events_dic["cluster_id"].append(cluster_id[0])
                    events_dic["clusters_prob"].append(list(clusters_prob))

                if idx % 1000 ==0:
                    print "Analyzing {} records".format(win[0].stats.starttime)

                if is_event:
                    win_filtered = win.copy()
                    # win_filtered.filter("bandpass",freqmin=4.0, freqmax=16.0)
                    win_filtered.plot(outfile=os.path.join(cfg.OUTPUT_PREDICT_BASE_DIR+"/"+stream_file_without_extension,"viz",
                                    "event_{}_cluster_{}.png".format(idx,cluster_id)))

                if cfg.save_sac and is_event:
                    win_filtered = win.copy()
                    win_filtered.write(os.path.join(cfg.OUTPUT_PREDICT_BASE_DIR,"sac",
                            "event_{}_cluster_{}.sac".format(idx,cluster_id)),
                            format="SAC")

                if idx >= max_windows:
                    print "stopped after {} windows".format(max_windows)
                    print "found {} events".format(n_events)
                    break

        except KeyboardInterrupt:
            print 'Interrupted at time {}.'.format(win[0].stats.starttime)
            print "processed {} windows, found {} events".format(idx+1,n_events)
            print "Run time: ", time.time() - time_start

    df = pd.DataFrame.from_dict(events_dic)
    df.to_csv(output_catalog)

    customPlot(stream, cfg.OUTPUT_PREDICT_BASE_DIR+"/"+stream_file+".png", events_dic["start_time"])

    print "Run time: ", time.time() - time_start

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file_path",type=str,default="config_default.ini",
                        help="path to .ini file with all the parameters")
    parser.add_argument("--stream_path",type=str,default=None,
                        help="path to mseed to analyze")

    args = parser.parse_args()

    cfg = config.Config(args.config_file_path)

    main(args)
