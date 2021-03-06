import os
import numpy as np
import argparse
import time
import re
import seisobs #https://github.com/d-chambers/seisobs
import fnmatch

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--bigsfile_path",type=str,default=None, help="path to the big sfile to split into multiple ones")
    parser.add_argument("--output_path",type=str,default=None)
    args = parser.parse_args()

    with open(args.bigsfile_path, "r") as ins:    
        first_line = True
        i = 0
        for line in ins:
            if line.isspace():
                first_line = True
                i = i + 1 
            elif first_line:
                #tokens = line.split(" ")
                #sfile_name = tokens[2]+"-"+tokens[3]+"-"+tokens[4]+".S"+tokens[0]+tokens[1]
                sfile_name = "01-0000-00M.S"+"%04d" % (i+1900,)+"01"
                dest_file = open(args.output_path+"/"+sfile_name, 'w')
                dest_file.write(line)
                first_line = False
            else:
                #line = line.rstrip()
                dest_file.write(line)


