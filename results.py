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

# Single result file:
#{
#            "dataset": "datos1",
#            "window_size": 10,
#            "n_traces": 1,
#            "n_clusters": 1,
#            "model": "experiments/config_model2.ini",
#            "truePositives": 1,
#            "falsePositives": 1,
#            "trueNegatives": 1,
#            "falseNegatives": 1,
#            "accuracy": 1.0,
#            "precision": 1.0,
#            "recall": 1.0,
#            "f1": 1.0,
#            "locationAccuracy": 1.0,    
#            "round": 1,
#            "dataset": "datos1"
#}

class Results():

    def __init__(self):
        self.results = []

    @staticmethod
    def harvest_results(round):
        rs = Results()
        result_files = [file for file in os.listdir("output") if
                    fnmatch.fnmatch(file, "*.json")]
        for result_file in result_files:
            r = Result.import_json(os.path.join("output", result_file))
            if r.round == round:
                rs.results.append(r)
        return rs

    def get_list_of_datasets(self): 
        datasets = []
        for r in self.results:
            if r.dataset not in datasets:
                datasets.append(r.dataset)
        return datasets

    def get_list_of_window_sizes(self): 
        window_sizes = []
        for r in self.results:
            if r.window_size not in window_sizes:
                window_sizes.append(r.window_size)
        return window_sizes

    def get_list_of_models(self): 
        models = []
        for r in self.results:
            if r.model not in models:
                models.append(r.model)
        return models

    def get_result(self, dataset, windows_size, model, n_traces, n_clusters): 
        #We assume that only results for a given round have been harvested.
        #print("get result("+dataset+", "+str(windows_size)+", "+model+", "+str(n_traces)+")")
        rs = []
        for r in self.results:
            if r.dataset == dataset and r.window_size == windows_size and r.model == model and r.n_traces == n_traces and r.n_clusters == n_clusters:
                rs.append(r)

        #Only one mathching the given criteria is expected
        if len(rs) != 1:
            print ("[results] \033[91m ERROR!!\033[0m Expecting one result but found "+str(len(rs))+" .")
            sys.exit(0)
        else:
            return rs[0]

    def any_result(self, dataset, windows_size, model, n_traces, n_clusters): 
        for r in self.results:
            if r.dataset == dataset and r.window_size == windows_size and r.model == model and r.n_traces == n_traces and r.n_clusters == n_clusters:
                return True
        return False

    def export_gnuplot(self): 
        datasets = self.get_list_of_datasets()
        models = self.get_list_of_models()
        windows_sizes = self.get_list_of_window_sizes()
        sys.stdout.write("\t\t\t\t")
        for model in models:  
            for windows_size in windows_sizes: 
                sys.stdout.write("\t" + model + "-" + str(windows_size))        
        for dataset in datasets:
            print
            sys.stdout.write(dataset+" (Z component)\t\t") 
            for model in models:  
                for windows_size in windows_sizes:
                    r =  self.get_result(dataset, windows_size, model, 1, 2)
                    sys.stdout.write(str(r.f1)+"\t")  
            #Not all datasets have results with 3 components
            if self.any_result(dataset, windows_sizes[0], models[0], 3, 2):
                print
                sys.stdout.write(dataset+" (3 components)\t\t") 
                for model in models:  
                    for windows_size in windows_sizes:
                        r =  self.get_result(dataset, windows_size, model, 3, 2)
                        sys.stdout.write(str(r.f1)+"\t") 
        print          

class Result():
    def __init__(self, window_size, n_traces, n_clusters, model,
        truePositives, falsePositives, trueNegatives, falseNegatives, 
        accuracy, precision, recall, f1, locationAccuracy, round, dataset):

        self.window_size = window_size
        self.n_traces = n_traces
        self.n_clusters = n_clusters
        self.model = model
        self.truePositives = truePositives
        self.falsePositives = falsePositives
        self.trueNegatives = trueNegatives
        self.falseNegatives = falseNegatives
        self.accuracy = accuracy
        self.precision = precision
        self.recall = recall
        self.f1 = f1
        self.locationAccuracy = locationAccuracy 
        self.round = round
        self.dataset = dataset

    @staticmethod
    def import_json(path):
        with open(path) as f:  
            jdata = json.load(f)
            r = Result(jdata['window_size'], jdata['n_traces'], jdata['n_clusters'], jdata['model'], 
                jdata['truePositives'], jdata['falsePositives'], jdata['trueNegatives'], jdata['falseNegatives'], 
                jdata['accuracy'], jdata['precision'], jdata['recall'], jdata['f1'], jdata['locationAccuracy'], jdata['round'], jdata['dataset'])
            return r

    def export_json(self, path):
        with open(path, 'w') as f:
            jdata = {}  
            jdata["window_size"] = self.window_size
            jdata["n_traces"] = self.n_traces
            jdata["n_clusters"] = self.n_clusters
            jdata["model"] = self.model
            jdata["truePositives"] = self.truePositives
            jdata["falsePositives"] = self.falsePositives
            jdata["trueNegatives"] = self.trueNegatives
            jdata["falseNegatives"] = self.falseNegatives
            jdata["accuracy"] = self.accuracy
            jdata["precision"] = self.precision
            jdata["recall"] = self.recall
            jdata["f1"] = self.f1
            jdata["locationAccuracy"] = self.locationAccuracy
            jdata["round"] = self.round
            jdata["dataset"] = self.dataset
            json.dump(jdata, f, indent=4)
        
if __name__ == "__main__":
    print ("\033[92m******************** TESTING RESULTS MODULE *******************\033[0m ")
    
    r = Result.import_json("result_template.json")
    r.export_json("borrar.json")
    print("TEST 1 OK :-)")

    rs = Results.harvest_results(round = 1)
    print("TEST 2 OK :-)")

    rs.export_gnuplot()




    

        