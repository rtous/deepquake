import os
import numpy as np
import argparse
import time
import re
import seisobs #https://github.com/d-chambers/seisobs
import fnmatch

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream_path",type=str,default=None,
                        help="path to mseed DIRECTORY to analyze")
    args = parser.parse_args()

    stream_files = [file for file in os.listdir(args.stream_path) if
                    fnmatch.fnmatch(file, "*")]

    for stream_file in stream_files:
        stream_file_without_extension = os.path.split(stream_file)[-1].split(".")[0]
        tokens = stream_file_without_extension.split("-")
        #2018-03-03-1929-00M
        sfile_name = tokens[2]+"-"+tokens[3]+"-"+tokens[4]+".S"+tokens[0]+tokens[1]
        #03-1908-S201803
        print(sfile_name)
