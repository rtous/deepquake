import os
import numpy as np
import argparse
import time
import re
import seisobs #https://github.com/d-chambers/seisobs


def readSFile():
    # Load stream
    stream_path = args.stream_path
    stream_file = os.path.split(stream_path)[-1]
    print "+ Analyzing metadata file {}".format(stream_file)
    infile = open(stream_path, 'r')
    s = infile.readline()
    infile.close()

    #2015  110 0517 30.4 L  10.352 -62.472 19.3  FUN 24 0.6 4.0WFUN  
    #2015-01-10T05:17:30.400000Z | +10.352,  -62.472 | 4.0 MW
    #Check: https://docs.python.org/3/howto/regex.html
    s = "2015  110 0517 30.4 L  10.352 -62.472"              
    #pattern = re.compile('(\d\d\d\d)\s(\S\d)(\d\d)\s(\d\d)(\d\d)')
    pattern = re.compile('(\d\d\d\d)\s(.\d)(.\d)\s(\d\d)(\d\d)\s(\d\d\.\d)\s(.)\s(.......)\s(.......)')
    match = pattern.match(s)
    year = match.group(1)
    month = match.group(2)
    day = match.group(3)
    hours = match.group(4)
    minutes = match.group(5)
    seconds = match.group(6)
    type = match.group(7)
    lat = match.group(8)
    long = match.group(9)
    print("year = "+year)
    print("month = "+month)
    print("day = "+day)
    print("hours = "+hours)
    print("minutes = "+minutes)
    print("seconds = "+seconds)
    print("type = "+type)
    print("lat = "+lat)
    print("long = "+long)


def main(args):
    dir_path = args.stream_path
    cat = seisobs.seis2cat(dir_path)   
    print(cat)
    cat.write('my_catalog.xml', format='QUAKEML', nsmap={'my_ns': 'http://test.org/xmlns/0.1'})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream_path",type=str,default=None,
                        help="path to mseed to analyze")
    args = parser.parse_args()
    main(args)
