#!/usr/bin/env python3
import math
import csv
import re
import os.path
from os import path
from collections import Counter
import sys

# reducer part 2
if path.exists("reduce2Out.txt"):  # output to pt2 file then pt1 file if 2 reduce tasks called
    output = open('reduce2OutPt2.txt', 'w')
else:
    output = open('reduce2Out.txt', 'w')

monthArr = "JAN", "FEB", "MAR", "APR", "MAY", "JUNE", "JULY", "AUG", "SEPT", "OCT", "NOV", "DEC"
print("%-37s" % "CRIME TYPE", end="")
for i in monthArr:
    print("%-4s " % i, end="")
print()
dictOfCrimes = {  # holds all the crimes:[month array]

}
for line in sys.stdin:
    # separate based on ','
    month, *crime = line.split(',')
    crime = crime[0]
    crime = crime.strip()  # remove newlines
    month = int(month)
    for num in range(1, 13):  # loop through every month
        if month == num:  # if same as read in month add crime to dictionary
            if crime in dictOfCrimes:  # if the crime already exists
                listArr = dictOfCrimes[crime]  # get array of months for the crime
                listArr[month-1] += 1  # add 1 to the month
                dictOfCrimes[crime] = listArr  # add updated array to the crime
            else:  # if crime doesn't exist in the list
                tempArray = []  # array of month counter for new dictionary entry
                for j in range(1, 13):  # loop through the months
                    if j != month:  # if month is not the same as the current month for the crime set as 0
                        tempArray.append(0)
                    else:  # if month is same as crime month then set as 1
                        tempArray.append(1)
                dictOfCrimes[crime] = tempArray  # add new entry to dictionary
for item in dictOfCrimes:
    print("%-37s" % item, end="")
    for n in dictOfCrimes[item]:
        print("%-4s " % n, end="")
    print()
print()

