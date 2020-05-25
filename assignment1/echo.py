#!/usr/bin/env python3
from mpi4py import MPI
import numpy as np
import sys
#mpi setup
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

if rank != 0:
	src = rank - 1 #set the source process to recv from
else:
	src = size - 1
if rank != size - 1:
	dst = rank + 1 #set the destination process to send to
else:
	dst = 0 #this is the last process, send to the master
#master
if rank == 0:
	x = 1 #initialize x
	while x >= 0: #loop on user input until you get a negative value
		x = int(input('Enter a number (negative to end): \n'))
		if x >= 0:
			print("\nProcess %d got  %d" % (rank, x))
			comm.send(x, dest = dst, tag = 11) #x = user number
		
    	#negative value
	if x < 0:
		comm.send(-1, dest = dst, tag = 11)
		sys.exit(0)

#slaves
if rank >= 1:
	#get user number
	#x = comm.recv(source = src, tag = 11)
	while True:
		x = comm.recv(source = src, tag = 11)#get new x value
		if x < 0:#negative number
			if rank != size - 1:
				comm.send(x, dest = dst, tag = 11)
			sys.exit(0)
		print("Process %d got  %d" % (rank, x))
		if rank != size - 1 and x >= 0: #dont let the last process hang on sending
			comm.send(x, dest = dst, tag = 11)
		#x = comm.recv(source = src, tag = 11)#get new x value
