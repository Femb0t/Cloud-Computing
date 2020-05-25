#!/usr/bin/env python3
from mpi4py import MPI
import numpy as np
import math
import sys

file = open("data.txt", "r") #open the data file
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()
num = []
num4 = []
terminate = 0
i = 1
#master
if rank == 0:
    lines = 0 #initialize lines
    #print("Size: %d" % (size))
    while True:
        inputLine = file.readline() #read a line
        if inputLine == "":
            break
        lines += 1 #keep the line count for splitting lines
        inputLine = inputLine.rstrip('\n')
        num.append(int(inputLine))
	
    linesPerArray = math.floor(len(num)/size) #number of lines per array
    #These are made for readability when the master runs
    masterStart = 0
    masterEnd = (int) (1 * linesPerArray)
    #print("Lines per array: %d" % (linesPerArray))
    for i in range(1, size-1): #send array and line number to other ranks
        #num[] chunk, starting line number for array
        start  = (int) (i * linesPerArray)
        end = (int) ((i + 1) * linesPerArray)
        #print("destination is rank %d start %d end %d" % (i,start, end))
        #This might hang with .send, change to isend to prevent blocking if necessary
        comm.send([num[start:end], (start)], dest = i, tag = 11) #sent line number was bugged w/ slice1
    if(i < size - 1): #size == 2
        i += 1
    if(i == size):
        i = 0
    start = (int) (i * linesPerArray)
    #print("destination is rank %d start %d end %d" % (i,start,len(num)))
    comm.send([num[start:], (start)], dest = i, tag = 11) #sent line number was bugged w/ slice1
    
    #print("Start line for (master) rank %d: %d" % (rank, masterStart))
    num4 = num[masterStart:masterEnd] #final array for master
    
    terminate = comm.irecv(source = MPI.ANY_SOURCE, tag = 13)
    line = 0 #Master starts at line 0
    for value in num4:
        line += 1
        if terminate.Test() == True:
            #print("Slave %d got kill signal" % (rank))
            break
        #loop checks all other processes for an interrupt
        if value == 11: #slave found the number
            #print index and rank
            print("Process (master) %d got 11 at line %d\n" % (rank, line)) #line may need to be line+1
            #notify other processes
            for killRank in range(0, size):
                if killRank != rank:
                    comm.isend(1, dest = killRank, tag = 13)
                    #print("Slave %d sent kill to process %d" % (rank, killRank))
            break

    #print("Slave (Master) %d terminating" % (rank))
    #master finished

#slaves
if rank >= 1:
    #print("Slave %d is running" % (rank))
    
    #get array and starting line number
    num, line = comm.recv(source = 0, tag = 11)
    #print("Slave %d got starting line %d" % (rank, line))
    terminate = comm.irecv(source = MPI.ANY_SOURCE, tag = 13)
    for value in num:
        line += 1
        if terminate.Test() == True:
            #print("Slave %d Got kill signal" % (rank))
            break
        #loop checks all other processes for an interrupt
        if value == 11: #slave found the number
            #print index and rank
            print("Process %d got 11 at line %d\n" % (rank, line)) #line may need to be line+1
            #notify other processes
            for killRank in range(0, size):
                if killRank != rank:
                    comm.isend(1, dest = killRank, tag = 13)
                    #print("Slave %d sent kill to process %d" % (rank, killRank))
            break
    #print("Slave %d terminating" % (rank))
    #slave finished
