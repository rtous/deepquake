import os
import numpy as np
import argparse
import time
import re
import seisobs #https://github.com/d-chambers/seisobs
from obspy.core.utcdatetime import UTCDateTime
import csv
import pandas as pd
import config as config

#python util_datos2_metadata2csv.py --input_metadata_file input/datos2/Eventos.txt --output_csv_metadata_file output/datos2/catalog.csv

def main(args):

    if not os.path.exists(os.path.dirname(args.output_csv_metadata_file)):
        os.makedirs(os.path.dirname(args.output_csv_metadata_file))
    
    events_dic ={"start_time": [],
     "end_time": [],
     "cluster_id": [],
     "clusters_prob": []}

    with open(args.input_metadata_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=" ", skipinitialspace=True)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1
                year = int(row[0])
                month = int(row[1])
                day = int(row[2])
                hour = int(row[3])
                minute = int(row[4])
                sec = int(float(row[5]))
                print(str(year)+","+str(month)+","+str(day)+","+str(hour)+","+str(minute)+","+str(sec))
                timeP = UTCDateTime(year=year, month=month, day=day, hour=hour, minute=minute, second=sec)
                events_dic["start_time"].append(timeP - cfg.pwave_window/2)
                events_dic["end_time"].append(timeP + cfg.pwave_window/2)
                events_dic["cluster_id"].append(0) #TODO
                events_dic["clusters_prob"].append(1) #manually annotated event

    df = pd.DataFrame.from_dict(events_dic)
    df.to_csv(args.output_csv_metadata_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config_file_path",type=str,default="config_default.ini",
                        help="path to .ini file with all the parameters")
    parser.add_argument("--input_metadata_file",type=str)
    parser.add_argument("--output_csv_metadata_file",type=str)
    args = parser.parse_args()
    cfg = config.Config(args.config_file_path)
    main(args)
