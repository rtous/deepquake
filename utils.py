#!/usr/bin/env python
# -------------------------------------------------------------------
# File Name : utils.py
# Creation Date : 11-07-2018
# Last Modified : 11-07-2018 13:21:32 
# Author: Ruben Tous <rtous@ac.upc.edu>
# -------------------------------------------------------------------
""""
Common functions.
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
import matplotlib.pyplot as plt
import obspy
import datetime as dt

def preprocess_stream(stream):
    stream = stream.detrend('constant')
    return stream.normalize()

def obspyDateTime2PythonDateTime(odt):
    return dt.datetime(odt.year, odt.month, odt.day, odt.hour, odt.minute, odt.second)

def check_stream(stream, cfg):    
    if len(stream) != 3:
        print ("\033[91m WARNING!!\033[0m Only "+str(len(stream))+" channels.")
        return False
    if stream[0].stats.sampling_rate != 100.0:
        print ("\033[91m WARNING!!\033[0m Wrong sampling rate ("+str(stream[0].stats.sampling_rate)+").")
        return False
    data_size = len(stream[0].data) + len(stream[1].data) + len(stream[2].data)
    if data_size != cfg.win_size*3:
        print ("\033[91m WARNING!!\033[0m Not enough data points  ("+str(data_size)+").")
        return False 
    return True

def fetch_window_data(stream, cfg):
    """fetch data from a stream window and dump in np array"""
    data = np.empty((cfg.win_size, 3))
    for i in range(3):
        data[:, i] = stream[i].data.astype(np.float32)
    data = np.expand_dims(data, 0)
    return data



