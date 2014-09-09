#!/usr/bin/python

import os
import sys
import argparse
import numpy as np


parser=argparse.ArgumentParser()
args=parser.parse_args()

mean=10.0
sigma=1.0

alpha=0.9
mv_avg=mean + sigma * np.random.normal()

beta=0.8
mv_var=0

line_no=1

while True:
	
	o_val=mean + sigma * np.random.normal()
	
	mv_avg=alpha * mv_avg + (1-alpha) * o_val
	diff_sq=(o_val-mv_avg) ** 2
	mv_var=beta * mv_var + (1-beta) * diff_sq
	
	print("%2d %7.1f %4.1f %7.3f %7.3f %4.1f %10.3f %5s" 
		% ( line_no,
			mean, 
			alpha, 
			o_val, 
			o_val - mv_avg, 
			beta,
			np.sqrt(mv_var),
			"X" if np.abs(o_val - mv_avg) > 1.1*np.sqrt(mv_var) else "")
	),

	inp=raw_input().strip().split()

	if len(inp) > 0:
		if inp[0] == "q": break
		if inp[0] == "m": mean=float(inp[1])
		if inp[0] == "s": sigma=float(inp[1])
		if inp[0] == "a": alpha=float(inp[1])
		if inp[0] == "b": beta=float(inp[1])

	line_no += 1

print("quitting")
