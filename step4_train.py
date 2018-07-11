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
  setproctitle.setproctitle('quakenet')

  tf.set_random_seed(1234)

  pos_path = os.path.join(cfg.DATASET,"positive")
  if not os.path.exists(pos_path):
    print ("\033[91m ERROR!!\033[0m Missing directory "+cfg.DATASET+"/positive. Run step 2 first.")
    sys.exit(0)
  neg_path = os.path.join(cfg.DATASET,"negative")
  if not os.path.exists(neg_path):
    print ("\033[91m ERROR!!\033[0m Missing directory "+cfg.DATASET+"/negative. Run step 3 first.")
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
  model = models.get(cfg.model, samples, cfg, cfg.CHECKPOINT_DIR, is_training=True)

  # train loop
  model.train(
    cfg.learning_rate,
    resume=cfg.resume,
    profiling=cfg.profiling,
    summary_step=10)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("--config_file_path",type=str,default="config_default.ini",
                        help="path to .ini file with all the parameters")
  args = parser.parse_args()

  cfg = config.Config(args.config_file_path)

  main(args)
