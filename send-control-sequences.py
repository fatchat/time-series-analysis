#!/usr/bin/python

import os
import sys
import argparse
import numpy as np

parser=argparse.ArgumentParser("Provide pre-recorded input to moving-average-spike-detection.py")
parser.add_argument("--control-file", required=True, help="text file containing control sequences")
parser.add_argument("--vlen", type=int, required=True, help="length of output vectors")
args=parser.parse_args()

full_series=[]

inputfile=open(args.control_file, "r")
for line in inputfile.readlines():
	[length, mean, sigma] = line.strip().split(' ')
	if int(length) > 0:
		for i in range(0, int(length)):
			o_val=float(mean) + float(sigma) * np.random.normal()
			full_series.append(o_val)

inputfile.close()

for starting_index in range(0, len(full_series) - args.vlen):
	sequence=full_series[starting_index:starting_index+args.vlen]
	print("+1 %s" % " ".join(["%d:%f " % (1+index, sequence[index]) for index in range(0, len(sequence)) ]))
