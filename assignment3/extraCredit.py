#!/usr/bin/env python3

from csv import reader
from pyspark.mllib.clustering import KMeans
from pyspark import SparkContext
import sys
import numpy as np


if __name__ == "__main__":
    sc = SparkContext(appName="extraCredit.py")
    sc.setLogLevel("ERROR")


    data = sc.textFile("hdfs://10.230.119.206:54310/user/cc/crimeData/")

    splitWeap = data.mapPartitions(lambda x: reader(x)).filter(lambda x: "DANGEROUS WEAPONS" in x)
    splitDrug = data.mapPartitions(lambda x: reader(x)).filter(lambda x: "DANGEROUS DRUGS" in x)

    def f(x):
        location = x[16]
        crime = x[7]
        if crime == "DANGEROUS WEAPONS":
            return (crime, location)
        if crime == "DANGEROUS DRUGS":
            return (crime, location)
        return ("", "")

    parsedData = data.map(f)
    #parsedData = data.map(np.array([f]))

    weaponLen = splitWeap.reduce(lambda a, b: a + b)
    drugsLen = splitDrug.reduce(lambda a, b: a + b)



    #build the model
    model = KMeans.train(parsedData, 4, maxIterations=10, initializationMode="random")


    #print the results
	#print("Cluster Centers: ", model.clusterCenters)
	#print("Number of Clusters= ", model.k)


    #sc.stop()                              #Not sure if this is needed, saw it in the pi.py example

