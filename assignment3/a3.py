#!/usr/bin/env python3

from csv import reader
from pyspark.mllib.clustering import KMeans
from pyspark import SparkContext
import sys
import numpy as np


if __name__ == "__main__":



        sc = SparkContext(appName="a3.py")
        sc.setLogLevel("ERROR")

        data = sc.textFile("hdfs://10.230.119.206:54310/user/cc/crimeData/")

        splitdata = data.mapPartitions(lambda x: reader(x))
        #pairs has the date and the offense description
        #map function to extract the month, crime type and assign a value of 1 if in july, 0 otherwise
        def f(x):
                date = x[5].split('/')#split the date
                month = date[0]#get the month
                crime = x[7]#get the crime type
                #return a key value pair where the month and crime is the key and 1 is the value
                if month == "07":
                        return ((month, crime), 1)
                return ((month, crime), 0)#this key is not in july, ignore with a value of 0
        pairs = splitdata.map(f)#run the map function

        #retrieve two results, the first one is the top 3 crimes in july,
        # 2nd is the number of crimes reported for DANGEROUS WEAPONS in july
        #result2 = pairs.collect()#super experimental
        result = pairs.reduceByKey(lambda a, b: a + b).takeOrdered(3, lambda (key, value): -1 * value)
        result2 = pairs.reduceByKey(lambda a, b: a + b).collect()
        #print the results
        print("Top 3 crime types that were reported in July")
        for line in result:
                print (line)
        #Also experimental
        for line in result2:
                if (line[0] == ('07', 'DANGEROUS WEAPONS')):
                        print("Number of crimes of type DANGEROUS WEAPONS reported in July: %s" % line[1])
        #sc.stop()#Not sure if this is needed, saw it in the pi.py example

