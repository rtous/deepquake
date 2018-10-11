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
from sklearn.metrics import confusion_matrix
import logging


truePositives = 0
falsePositives = 0
trueNegatives = 0
falseNegatives = 0

def eval(args, positivesOrNegatives):
    global truePositives
    global falsePositives
    global trueNegatives
    global falseNegatives
    #summary_dir = os.path.join(output_dir, "eval_summary_events")   

    datasetDir = None

    if positivesOrNegatives:
        datasetDir = os.path.join(args.tfrecords_dir, cfg.output_tfrecords_dir_positives)
    else:
        datasetDir = os.path.join(args.tfrecords_dir, cfg.output_tfrecords_dir_negatives)
    
    #print(datasetDir)

    cfg.batch_size = 1
    cfg.n_epochs = 1
    cfg.add = 1

    try:
        # data pipeline
        data_pipeline = DataPipeline(datasetDir, config=cfg, 
                                        is_training=False)
        samples = {
            'data': data_pipeline.samples,
            'cluster_id': data_pipeline.labels,
            "start_time": data_pipeline.start_time,
            "end_time": data_pipeline.end_time}

        #print("data_pipeline.samples="+str(data_pipeline.samples))

        # set up model and validation metrics
        model = models.get(cfg.model, samples, cfg,
                   checkpoint_dir,
                   is_training=False)

        metrics = model.validation_metrics()
        # Validation summary writer
        #summary_writer = tf.train.SummaryWriter(summary_dir, None)

        with tf.Session() as sess:
            coord = tf.train.Coordinator()
            tf.initialize_local_variables().run()
            threads = tf.train.start_queue_runners(sess=sess, coord=coord)

            model.load(sess)
            print  'Evaluating at step {}'.format(sess.run(model.global_step))

            #step = tf.train.global_step(sess, model.global_step)
            mean_metrics = {}
            for key in metrics:
                mean_metrics[key] = 0

            n = 0
            pred_labels = np.empty(1)
            true_labels = np.empty(1)
            while True:
                try:
                    to_fetch  = [metrics,
                                 model.layers["class_prediction"],
                                 samples["cluster_id"],
                                 samples["start_time"],
                                 samples["end_time"]]
                    metrics_, batch_pred_label, batch_true_label, starttime, endtime = sess.run(to_fetch)

                    if positivesOrNegatives: 
                        if batch_true_label[0]==0 and batch_pred_label[0]==1:
                            truePositives = truePositives+1
                            #sys.stdout.write("\033[92mP\033[0m")
                        else:
                            falsePositives = falsePositives+1
                            #sys.stdout.write("\033[91mP\033[0m")
                    else:
                        if batch_true_label[0]==-1 and batch_pred_label[0]==0:
                            trueNegatives = trueNegatives+1
                            #sys.stdout.write("\033[92mN\033[0m")
                        else:
                            falseNegatives = falseNegatives+1
                            #sys.stdout.write("\033[91mN\033[0m")

                    #print("batch_true_label="+str(batch_true_label))
                    #print("batch_pred_label="+str(batch_pred_label))
                    batch_pred_label -=1 
                    pred_labels = np.append(pred_labels,batch_pred_label)
                    true_labels = np.append(true_labels, batch_true_label)

                    # print  true_labels
                    for key in metrics:
                        mean_metrics[key] += cfg.batch_size*metrics_[key]
                    n += cfg.batch_size

                    #mess = model.validation_metrics_message(metrics_)
                    #print '{:03d} | '.format(n)+mess

                except KeyboardInterrupt:
                    print 'stopping evaluation'
                    break

                except tf.errors.OutOfRangeError:
                    print 'Evaluation completed ({} epochs).'.format(cfg.n_epochs)
                    print "{} windows seen".format(n)
                    break

            if n > 0:
              for key in metrics:
                mean_metrics[key] /= n
                summary = tf.Summary(value=[tf.Summary.Value(
                  tag='{}/val'.format(key), simple_value=mean_metrics[key])])
                #if args.save_summary:
                #    summary_writer.add_summary(summary, global_step=step)

            #summary_writer.flush()

            mess = model.validation_metrics_message(mean_metrics)
            #print 'Average | '+mess
            coord.request_stop()
    finally:
        pass
        #print 'joining data threads'

    pred_labels = pred_labels[1::]
    true_labels = true_labels[1::]
    # np.save("output/pred_labels_noise.npy",pred_labels)
    # np.save("output/true_labels_noise.npy",true_labels)
    #print "---Confusion Matrix----"
    #print confusion_matrix(true_labels, pred_labels)

    coord.join(threads)

    # if args.save_false:
    #     false_preds = np.array((false_start, false_end)).transpose()
    #     df =  pd.Dataframe(false_preds, columns=["start_time, end_time"])
    #     df.to_csv(os.path.join(false_dir,"false_preds.csv")

if __name__ == "__main__":

    logging.getLogger("tensorflow").setLevel(logging.ERROR)

    print ("\033[92m******************** STEP 5/5. EVALUATION *******************\033[0m ")

    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file_path",type=str,default="config_default.ini",
                        help="path to .ini file with all the parameters")
    parser.add_argument("--pattern",type=str, default="*.mseed")
    parser.add_argument("--output_dir",type=str)
    parser.add_argument("--checkpoint_dir",type=str)
    parser.add_argument("--catalog_path",type=str) #For datos2, which have just one global catalog
    #parser.add_argument("--redirect_stdout_stderr",type=bool, default=False)
    parser.add_argument("--tfrecords_dir",type=str)
    args = parser.parse_args()

    cfg = config.Config(args.config_file_path)

    checkpoint_dir = args.checkpoint_dir

    if not os.path.exists(checkpoint_dir):
        print ("[train] \033[91m ERROR!!\033[0m Missing directory "+checkpoint_dir+". Run step 3 (train) first.")
        sys.exit(0)

    output_dir = args.output_dir

    dataset_dir = args.tfrecords_dir



    #if args.redirect_stdout_stderr:
    #    stdout_stderr_file = open(os.path.join(output_dir, 'stdout_stderr_file.txt'), 'w')
    #    sys.stdout = stderr = stdout_stderr_file
    
    eval(args, True)
    tf.reset_default_graph()
    eval(args, False)

    print("[validation] true positives = "+str(truePositives))
    print("[validation] false positives = "+str(falsePositives))
    print("[validation] true negatives = "+str(trueNegatives))
    print("[validation] false negatives = "+str(falseNegatives))

    if truePositives+falsePositives>0:
        print("[validation] precission = "+str(100*float(truePositives)/(truePositives+falsePositives))+"%")
    else:
        print("[validation] cannot compute precission as truePositives+falsePositives == 0")

    if truePositives+falseNegatives>0:
        print("[validation] recall = "+str(100*float(truePositives)/(truePositives+falseNegatives))+"%")
    else:
        print("[validation] cannot compute recall as truePositives+falseNegatives == 0")

    if truePositives+falsePositives+trueNegatives+falseNegatives>0:
        print("[validation] accuracy = "+str(100*float(truePositives+trueNegatives)/(truePositives+falsePositives+trueNegatives+falseNegatives))+"%")
    else:
        print("[validation] cannot compute accuracy as truePositives+falsePositives+trueNegatives+falseNegatives == 0")


    #if args.redirect_stdout_stderr:  
    #    stdout_stderr_file.close()

