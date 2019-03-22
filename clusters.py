import json
from obspy.core import read
from quakenet.data_io import load_catalog
from obspy.core.utcdatetime import UTCDateTime
import argparse
import os
import fnmatch
import seisobs #https://github.com/d-chambers/seisobs
import sys 
import csv
from sklearn.neighbors.nearest_centroid import NearestCentroid
import numpy as np
from shapely.geometry import Polygon
from shapely.geometry import Point

class Clusters():

    def __init__(self):
        self.clusters = []
        self.type = None
        self.nearest_centroid_model = None
   
    def nearest_cluster(self, lat, lon, depth):
        if self.type == "kmeans":
            cluster_id = self.nearest_centroid_model.predict([[lat, lon, depth]])[0]
            for c in self.clusters:
                if c.id == cluster_id:
                    return c
            print ("[clusters] \033[91m ERROR!!\033[0m No nearest cluster found for the given lat, lon, depth")
            sys.exit(0)
        elif self.type == "lines":
            c_with_min_distance = None
            min_distance = None
            for c in self.clusters:
                p1 = np.array([c.lat1,c.lon1])
                p2 = np.array([c.lat2,c.lon2])
                p3 = np.array([lat,lon])
                d = np.cross(p2-p1,p3-p1)/np.linalg.norm(p2-p1)
                #print ("[clusters] dist ("+str(lat)+", "+str(lon)+") to cluster "+str(c.id)+"=="+str(d))
                if min_distance == None or min_distance > d:
                    min_distance = d
                    c_with_min_distance = c
            return c_with_min_distance
        elif self.type == "polygons":
            p = Point(lat, lon)
            for c in self.clusters:
                #print("checking cluster "+c.label)
                poly = Polygon(((c.x1, c.y1), (c.x2, c.y2), (c.x3, c.y3), (c.x4, c.y4)))
                if p.within(poly):
                    return c
            return None #this clustering can result in None. The earthquake should be discarded during the generation of tfrecords.
        else:
            print ("[clusters] \033[91m ERROR!!\033[0m Wrong value for clusters type = "+self.type)
            sys.exit(0)  
    
    def import_json(self, path):
        with open(path) as f:  
            jdata = json.load(f)
            if jdata['clusters_type'] == "kmeans":   
                self.type = "kmeans"
                for jcluster in jdata['clusters']:
                    c = KmeansCluster(jcluster['lat'], jcluster['lon'], jcluster['depth'], jcluster['id'], jcluster['label'])
                    self.clusters.append(c)
                #centroids = np.array([[10.33908571, -68.01505714], [8.246, -72.21366667], [10.352, -62.472]]) #centroids
                centroids = np.zeros(shape=(len(self.clusters),3))
                #centroid_numbers = np.array([0, 1, 2])
                centroid_numbers = np.zeros(shape=(len(self.clusters)))
                for i, c in enumerate(self.clusters):
                    centroids[i, 0] = c.lat
                    centroids[i, 1] = c.lon
                    centroids[i, 2] = c.depth
                    centroid_numbers[i] = c.id
                self.nearest_centroid_model = NearestCentroid()
                self.nearest_centroid_model.fit(centroids, centroid_numbers)
            elif jdata['clusters_type'] == "lines":
                self.type = "lines"
                for jcluster in jdata['clusters']:
                    c = LineCluster(jcluster['lat1'], jcluster['lon1'], jcluster['lat2'], jcluster['lon2'], jcluster['id'], jcluster['label'])
                    self.clusters.append(c)
            elif jdata['clusters_type'] == "polygons":
                self.type = "polygons"
                for jcluster in jdata['clusters']:
                    c = PolygonCluster(jcluster['x1'], jcluster['y1'], jcluster['x2'], jcluster['y2'], jcluster['x3'], jcluster['y3'], jcluster['x4'], jcluster['y4'], jcluster['id'], jcluster['label'])
                    self.clusters.append(c)
            else:
                print ("[clusters] \033[91m ERROR!!\033[0m Unrecognized clusters option: "+jdata['clusters_type'])
                sys.exit(0)   
                
class KmeansCluster():
    def __init__(self, lat, lon, depth, id, label):
        self.lat = lat
        self.lon = lon
        self.depth = depth
        self.id = id
        self.label = label

class LineCluster():
    def __init__(self, lat1, lon1, lat2, lon2, id, label):
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2
        self.id = id
        self.label = label

class PolygonCluster():
    def __init__(self, x1, y1, x2, y2, x3, y3, x4, y4, id, label):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.x4 = x4
        self.y4 = y4
        self.id = id
        self.label = label
        
if __name__ == "__main__":
    print ("\033[92m******************** TESTING CLUSTERING MODULE *******************\033[0m ")
    #parser = argparse.ArgumentParser()
    #parser.add_argument("--clusters_file_path", type=str)
    #args = parser.parse_args()
    cs = Clusters()
    print("kmeans...")
    cs.import_json("clusters_kmeans_template.json")
    c = cs.nearest_cluster(41.47744336, 2.07199462, 0.0)
    print("Nearest cluster id = "+str(c.id))
    print("Nearest cluster label = "+str(c.label))

    cs = Clusters()
    print("lines...")
    cs.import_json("clusters_lines_template.json")
    c = cs.nearest_cluster(41.47744336, 2.07199462, 0.0)
    print("Nearest cluster id = "+str(c.id))
    print("Nearest cluster label = "+str(c.label))

    cs = Clusters()
    print("polygons (Andorra)...")
    cs.import_json("clusters_polygons_template.json")
    c = cs.nearest_cluster(42.505479, 1.581206, 0.0) 
    if c is not None:
        print("Nearest cluster id = "+str(c.id))
        print("Nearest cluster label = "+str(c.label))
    else:
        print("No nearest cluster (polygon) found.")
    cs = Clusters()
    print("polygons (Cubelles)...")
    cs.import_json("clusters_polygons_template.json")
    c = cs.nearest_cluster(41.209584, 1.627644, 0.0) 
    if c is not None:
        print("Nearest cluster id = "+str(c.id))
        print("Nearest cluster label = "+str(c.label))
    else:
        print("No nearest cluster (polygon) found.")
    cs = Clusters()
    print("polygons (Huesca)...")
    cs.import_json("clusters_polygons_template.json")
    c = cs.nearest_cluster(42.138258, -0.401985, 0.0) 
    if c is not None:
        print("Nearest cluster id = "+str(c.id))
        print("Nearest cluster label = "+str(c.label))
    else:
        print("No nearest cluster (polygon) found.")





    

        