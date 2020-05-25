#!/usr/bin/env python3

import sys
import re
import os.path
from os import path

#if path.exists("reduce2Out.txt"):  # remove reduce output file before reducer creates it
#    os.remove("reduce2Out.txt")

#output = open('map2Out.txt', 'w')
lineNum = 1
i = 0
# get input from stdin
for line in sys.stdin:  # read each line
    if lineNum == 1:  # skip first line
        lineNum += 1
        continue
    while i < 5:  # check for quoted strings 5 times (no need to check every word)
        matched = re.search(r'".+?,[^"]*"', line)  # catch the first quoted string in the data
        # This quoted string appears in the offense description column sometimes
        if matched:
            newString = re.sub(r'\,', r'!', matched.group())  # remove ALL commas in a quoted string (rep w/ !)
            newString = re.sub(r'"', r'%', newString)  # temp swap " with %
            line = re.sub(r'".+?,[^"]*"', '{}'.format(newString), line, 1)  # insert the cleaned quoted string back in
            # the offense description column should have all commas in its quotes removed now
        i = i + 1
    i = 0
    columns = line.split(",")  # split the columns by commas
    date = columns[5]
    date, *junk = date.split('/')
    offense = columns[7]
    offense = re.sub(r'!', r',', offense)  # change all ! to , that we swapped before
    offense = re.sub(r'%', r'"', offense)  # change all % to " that we swapped before
    month = date[0]  # get month from date

    print("%s,%s" % (date, offense))  # month x, crime y

