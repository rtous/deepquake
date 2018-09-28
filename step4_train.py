#!/usr/bin/env python
# encoding: utf-8
# -------------------------------------------------------------------
# File:    train.py
# Author:  Michael Gharbi <gharbi@mit.edu>
# Created: 2016-10-25
# -------------------------------------------------------------------
# 
# 
# 
# ------------------------------------------------------------------#
"""Train a model."""

import argparse
import os
import time
import numpy as np
import tensorflow as tf
import setproctitle
import quakenet.models as models
import quakenet.data_pipeline as dp
import config as config
import sys

def main(args):
  print ("\033[92m******************** STEP 4/5. TRAINING *******************\033[0m ")
  setproctitle.setproctitle('quakenet')

  tf.set_random_seed(1234)

  #pos_path = os.path.join(cfg.DATASET,"positive")
  pos_path = os.path.join(os.path.join(dataset_dir, "train"), cfg.output_tfrecords_dir_positives)
  if not os.path.exists(pos_path):
    print ("[train] \033[91m ERROR!!\033[0m Missing directory "+pos_path+". Run step 2 first.")
    sys.exit(0)
  neg_path = os.path.join(os.path.join(dataset_dir, "train"), cfg.output_tfrecords_dir_negatives)
  if not os.path.exists(neg_path):
    print ("[train] \033[91m ERROR!!\033[0m Missing directory "+neg_path+". Run step 3 first.")
    sys.exit(0)

  # data pipeline for positive and negative examples
  pos_pipeline = dp.DataPipeline(pos_path, cfg, True)
  neg_pipeline = dp.DataPipeline(neg_path, cfg, True)

  pos_samples = {
    'data': pos_pipeline.samples,
    'cluster_id': pos_pipeline.labels
    }
  neg_samples = {
    'data': neg_pipeline.samples,
    'cluster_id': neg_pipeline.labels
    }

  samples = {
    "data": tf.concat(0,[pos_samples["data"],neg_samples["data"]]),
    "cluster_id" : tf.concat(0,[pos_samples["cluster_id"],neg_samples["cluster_id"]])
    }

  # model
  model = models.get(cfg.model, samples, cfg, checkpoint_dir, is_training=True)

  # train loop
  model.train(
    cfg.learning_rate,
    resume=cfg.resume,
    profiling=cfg.profiling,
    summary_step=10,
    checkpoint_step=cfg.checkpoint_step,
    max_checkpoint_step=cfg.max_checkpoint_step
    )

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--config_file_path",type=str,default="config_default.ini",
                        help="path to .ini file with all the parameters")
  parser.add_argument("--tfrecords_dir",type=str)
  parser.add_argument("--checkpoint_dir",type=str)
  #parser.add_argument("--redirect_stdout_stderr",type=bool, default=False)

  args = parser.parse_args()

  cfg = config.Config(args.config_file_path)
  
  dataset_dir = args.tfrecords_dir
  checkpoint_dir = args.checkpoint_dir
  
  #if args.redirect_stdout_stderr:
  #    stdout_stderr_file = open(os.path.join(checkpoint_dir, 'stdout_stderr_file.txt'), 'w')
  #    sys.stdout = stderr = stdout_stderr_file

  main(args)

  #if args.redirect_stdout_stderr:  
  #      stdout_stderr_file.close()
