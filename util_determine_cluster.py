import os
import numpy as np
import argparse
import time
import re
import seisobs #https://github.com/d-chambers/seisobs
import fnmatch
from sklearn.neighbors.nearest_centroid import NearestCentroid

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    ##parser.add_argument("--bigsfile_path",type=str,default=None, help="path to the big sfile to split into multiple ones")
    ##parser.add_argument("--output_path",type=str,default=None)
    args = parser.parse_args()

    X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]]) #centroids
    y = np.array([0, 1, 2, 3, 4, 5])
    clf = NearestCentroid()
    clf.fit(X, y)
    print(clf.predict([[1.6, 1]]))
                
