#!/usr/bin/python

import os
import sys
import argparse
import numpy as np

parser=argparse.ArgumentParser("Create input vectors for libsvm. Input is provided on STDIN")
parser.add_argument("--vlen", type=int, required=True, help="length of output vectors")
args=parser.parse_args()

full_series=sys.stdin.readlines()

for start in range(0, len(full_series) - args.vlen):
	values=["%d:%f " % (1+index-start, float(full_series[index].strip())) for index in range(start, start+args.vlen)]
	print("0 %s" % " ".join(values))
