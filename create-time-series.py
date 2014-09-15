#!/usr/bin/python

import os
import sys
import argparse
import numpy as np

parser=argparse.ArgumentParser("Create input vectors for libsvm")
parser.add_argument("-c", "--control-file", required=True, help="text file containing control sequences")
args=parser.parse_args()

inputfile=open(args.control_file, "r")
for line in inputfile.readlines():
	[length, mean, sigma] = line.strip().split(' ')
	if int(length) > 0:
		for i in range(0, int(length)):
			o_val=float(mean) + float(sigma) * np.random.normal()
			print(o_val)
