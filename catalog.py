import json
from obspy.core import read
from quakenet.data_io import load_catalog
from obspy.core.utcdatetime import UTCDateTime
import argparse
import os
import fnmatch
import seisobs #https://github.com/d-chambers/seisobs
import sys 

class Catalog():

    def __init__(self):
        self.events = []
   
    def import_sfiles(self, input_metadata_dir):
        metadata_files = [file for file in os.listdir(input_metadata_dir) if
            fnmatch.fnmatch(file, "*")]
        print "[obtain training windows] List of metadata files to anlayze: ", metadata_files
        for metadata_file in metadata_files:
            #1. Process metadata
            print("[preprocessing metadata] Reading metadata file "+os.path.join(input_metadata_dir, metadata_file))
            obspyCatalogMeta = seisobs.seis2cat(os.path.join(input_metadata_dir, metadata_file)) 
            
            if len(obspyCatalogMeta.events) == 0 :
                print ("[preprocessing metadata] \033[91m ERROR!!\033[0m Cannot process metadata sfile "+os.path.join(input_metadata_dir, metadata_file))
                sys.exit(0)

            #print("[preprocessing metadata] Imported sfile "+str(obspyCatalogMeta.events[0]))
            eventOriginTime = obspyCatalogMeta.events[0].origins[0].time
            lat = obspyCatalogMeta.events[0].origins[0].latitude
            lon = obspyCatalogMeta.events[0].origins[0].longitude
            depth = obspyCatalogMeta.events[0].origins[0].depth
            e = Event(eventOriginTime, lat, lon, depth)
            self.events.append(e)
            for pick in obspyCatalogMeta.events[0].picks:
                if pick.phase_hint == 'P':
                    station_code = pick.waveform_id.station_code
                    d = Detection(station_code, pick.time)
                    e.detections.append(d)

    #def export_json(self, path):
    #    with open(path, 'w') as f:
    #        s = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
    #        json.dump(s, f)

    def export_json(self, path):
        with open(path, 'w') as f:
            jevents = {"events":[]}  
            for e in self.events:
                jevent = {"detections":[]}
                jevent["eventOriginTime"] = str(e.eventOriginTime)
                jevent["lat"] = e.lat
                jevent["lon"] = e.lon
                jevent["depth"] = e.depth
                for d in e.detections:
                    jevent["detections"].append({"station":d.station, "ptime":str(d.ptime)})
                jevents["events"].append(jevent)
            json.dump(jevents, f, indent=4)

    def import_json(self, path):
        with open(path) as f:  
            jdata = json.load(f)
            for jevent in jdata['events']:
                e = Event(UTCDateTime(jevent['eventOriginTime']), jevent['lat'], jevent['lon'], jevent['depth'])
                self.events.append(e)
                for jdetection in jevent['detections']:
                    d = Detection(jdetection['station'], UTCDateTime(jdetection['ptime']))
                    e.detections.append(d)

    def getPtime(self, window_start, window_end, station):
        ptime = None
        for e in self.events:
            for d in e.detections:
                if ((d.station == station) and (d.ptime >= window_start) and (d.ptime <= window_end)):
                    ptime = d.ptime
        return ptime

    def getLocations(self):
        locations = []
        for e in self.events:
            locations.append([e.lat, e.lon, e.depth])
            print(str(e.lat)+","+str(e.lon)+","+str(e.depth))
        return locations

class Event():
    def __init__(self, eventOriginTime, lat, lon, depth):
        self.eventOriginTime = eventOriginTime
        self.lat = lat
        self.lon = lon
        self.depth = depth
        self.detections = [] 

class Detection():
    def __init__(self, station, ptime):
        self.station = station
        self.ptime = ptime

#if __name__ == "__main__":
#    print ("\033[92m******************** STEP 1/5. PREPROCESSING STEP 1/4. IMPORT METADATA *******************\033[0m ")
#    parser = argparse.ArgumentParser()
#    parser.add_argument("--input_path", type=str)
#    parser.add_argument("--output_path", type=str)
#    args = parser.parse_args()
#    if not os.path.exists(os.path.dirname(args.output_path)):
#        os.makedirs(os.path.dirname(args.output_path))
#    c = Catalog()
#    c.import_sfiles(args.input_path)
#    c.export_json(args.output_path)
#    c.import_json(args.output_path)
#    c.export_json("out2.json")


    

        