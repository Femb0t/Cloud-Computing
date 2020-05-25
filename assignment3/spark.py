#!/usr/bin/env python3

from csv import reader
from pyspark.mllib.clustering import KMeans
from pyspark import SparkContext
import sys
import numpy as np

sc = SparkContext(appName="spark.py")
sc.setLogLevel("ERROR")

data = sc.textFile("hdfs://ipaddr:54310/hw2-input/")

splitdata = data.mapPartitions(lambda x: reader(x))
# x[16] = PREM_TYPE_DES (location) | x[7] = OFNS_DESC (crimetype)
scMap = splitdata.map(lambda x: (x[16], x[7]))
for item in scMap:
	print("%s" % item)

