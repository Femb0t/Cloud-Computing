#!/usr/bin/env python3
import math
import csv
import re
from collections import Counter
import sys

# reducer
bureauCount = 0
lineNum = 1
bDict = {
    "Bureau": ["Offense"]
}
for line in sys.stdin:
    # remove whitespace
    if lineNum == 1:
        lineNum += 1
        continue  # skip first line
    # separate based on ','
    line = re.sub(r'(".+?),(.+?")', r'\1#.#\2', line)
    line = line.split(",")  # break up columns by commas
    month = line[0]
    offense = line[1]
    offense = re.sub(r'(".+?)#\.#(.+?")', r'\1,\2', offense)
    bureau = line[2]
    if bureau in bDict:  # if bureau already exists append the offense to the list
        bDict[bureau].append(offense)
    else:
        bDict[bureau] = [offense]
# loop through each bureau in the dictionary and count the offenses and bureau occurrences
maxCount = 0
for key in bDict:
    offenseMatrix = Counter(bDict[key])  # count number of occurrences of each item in an array
    for crime in offenseMatrix:
        if maxCount < offenseMatrix[crime]:
            maxCount = offenseMatrix[crime]  # count of max crime occurrence
            maxBureau = key  # name of location max crime was committed
            maxOffense = Counter(bDict[maxBureau])  # dictionary of offenses for printing

print("Number of Crimes: %d" % maxCount)
print("Location Committed: %s\n" % maxBureau)
for x in maxOffense:
    print(x)
