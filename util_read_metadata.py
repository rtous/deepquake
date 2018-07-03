import os
import numpy as np
import argparse
import time
import re
import seisobs #https://github.com/d-chambers/seisobs

def main(args):
    dir_path = args.stream_path

    #nordic format to obspy format
    cat = seisobs.seis2cat(dir_path)   
    print(cat)

    #write to .xml
    cat.write('output/metadata.xml', format='QUAKEML', nsmap={'my_ns': 'http://test.org/xmlns/0.1'})

    print("Resource ID = "+str(cat.resource_id))
    for event in cat.events:
        print event
        for event_description in event.event_descriptions:
            print event_description
        for comment in event.comments:
            print comment
        for pick in event.picks:
            print pick
            print pick.waveform_id.station_code
        for origin in event.origins:
            print origin
        for magnitude in event.magnitudes:
            print magnitude

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--stream_path",type=str,default=None,
                        help="path to mseed to analyze")
    args = parser.parse_args()
    main(args)
