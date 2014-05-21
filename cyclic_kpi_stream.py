#!/usr/bin/python

import os
import sys
import argparse
import random

# handle command-line arguments
parser=argparse.ArgumentParser()
parser.add_argument("--dim", type=int, required=True)
parser.add_argument("--npoints", type=int, required=True)
parser.add_argument("--threshold", type=float, default=30.0)
parser.add_argument("--libsvm", action="store_true", help="libsvm output format")
args=parser.parse_args()

# Generator for stream
class StreamSource:

	# the cyclic pattern underlying our output stream. modify at will
	# note that the generated points will start at the SECOND element of the cycle
	cycle=[10,15,20,21,16,12,18,35,35,34,29,27,22,18,14,15,14,13,11]

	# get the size of the point. could be done in multiple ways, for now we just take the max coordinate
	max_coord=max(cycle)

	# constructor, takes the dimension of the space in which points will be generated
	def __init__(self, dim):

		# save the dimension provided
		self.dim=dim

		# initialize the starting index
		self.current_index=0

		# track the last generated point. upon each iteration we will only generate one new coordinate, shifting the others left
		self.current_point=[]

		# initial fill up
		for _ in range(0, self.dim):
			
			# get next coordinate, with noise added. append it as a coordinate to this initial point
			self.current_point.append(self.get_next_coordinate())

	# add some random noise, +/- 0.005 of the value, and new coordinate is non-negative
	def add_noise(self,coordinate):
		return max(0, coordinate * (1 + 0.01 * (random.random()-0.5)))

	# generate a new coordinate using the specified point in the cycle, with noise added
	def get_next_coordinate(self):

		# get the value from the cycle
		clean_coord=StreamSource.cycle[self.current_index]
		
		# update the starting index for the next round
		self.current_index=(self.current_index + 1) % len(StreamSource.cycle)

		# add some noise to this value and return
		return self.add_noise(clean_coord)

	# this is the generator. to be called repeatedly
	def get_next_point(self):

		# get the new coordinate from the cycle, with noise added. the self.current_index is guaranteed ot
		self.current_point.append(self.get_next_coordinate())

		# truncate the head of the list
		self.current_point=self.current_point[1:]

		# now the dimension is correct, return it
		return self.current_point

# check if any coordinate of the supplied point is greater than the given threshold
def above_threshold(point,  threshold):
	return filter(None, map(lambda _: _ > threshold, point))

# -- start --
# create the stream source
source=StreamSource(args.dim)

# generate as many points as the user requests
nclass1=0
for _ in range(0,args.npoints):

	# get the next generated point
	point=source.get_next_point()

	# get the class
	if above_threshold(point, args.threshold):
		class_ = -1
		nclass1 += 1
	else:
		class_ = 1

	# send to stdout
	if args.libsvm:
		output = "%d " % class_
		for index,value in enumerate(point):
			output += "%d:%d " % (1 + index, value) 
		print(output)
	else:
		print("point=%s => %d" % (point, class_))
	
sys.stderr.write("Class 1 = %d Class 2 = %d\n" % (nclass1, args.npoints - nclass1))
