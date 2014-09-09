#!/usr/bin/python

import os
import sys
import argparse
import numpy as np


parser=argparse.ArgumentParser()
parser.add_argument("--alpha", type=float, default=0.9, help="update weight for moving average")
parser.add_argument("--beta", type=float, default=0.9, help="update weight for moving diff")
parser.add_argument("--gamma", type=float, default=0.9, help="update weight for moving variance")
parser.add_argument("--mean", type=float, default=10, help="initial mean for generated series")
parser.add_argument("--sigma", type=float, default=1.0, help="initial std. dev. for generated series")
args=parser.parse_args()

mean=args.mean
sigma=args.sigma

alpha=args.alpha
beta=args.beta
gamma=args.gamma

# reading 1
o_val=mean + sigma * np.random.normal()
mv_avg=o_val

# reading 2
o_val=mean + sigma * np.random.normal()
mv_avg=alpha * mv_avg + (1-alpha) * o_val

diff=o_val-mv_avg
mv_diff=diff
mv_var=diff * diff

line_no=1

while True:
	
	o_val=mean + sigma * np.random.normal()
	mv_avg=alpha * mv_avg + (1-alpha) * o_val

	diff=o_val-mv_avg
	mv_diff=beta*mv_diff + (1-beta) * diff

	diff_sq=diff * diff
	mv_var=gamma * mv_var + (1-gamma) * diff_sq
	mv_sigma=np.sqrt(mv_var)
	
	print("[%4d] mean=%4.1f  alpha=%3.1f  obs=%6.3f  diff=%7.3f  beta=%3.1f  mv_diff=%7.3f  gamma=%3.1f  mv_sigma=%6.3f %5s\t" 
		% ( line_no,
			mean, 
			alpha, 
			o_val, 
			diff, 
			beta,
			mv_diff,
			gamma,
			mv_sigma,
			"X" if np.abs(diff) > 2*mv_sigma else "")
	),

	inp=raw_input().strip().split()

	if len(inp) > 0:
		if inp[0] == "q": break
		if inp[0] == "m": mean=float(inp[1])
		if inp[0] == "s": sigma=float(inp[1])
		if inp[0] == "a": alpha=float(inp[1])
		if inp[0] == "b": gamma=float(inp[1])

	line_no += 1

print("quitting")
