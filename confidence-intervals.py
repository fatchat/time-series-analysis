import os
import sys
import argparse
import datetime
import numpy
import scipy.stats
from collections import defaultdict

parser=argparse.ArgumentParser()
parser.add_argument("--input", required=True)
args=parser.parse_args()

def bayes_CF(_data,confidence=0.95):
    data=1.0*numpy.array(_data)
    (m,v,s)=scipy.stats.bayes_mvs(data,confidence)
    return (m,s)

def get_mean(_data):
    data=1.0*numpy.array(_data)
    mean=numpy.mean(data)
    return mean

def mean_confidence_interval(_data, confidence=0.95):
    data=1.0 * numpy.array(_data)
    std_error=scipy.stats.sem(data)
    width=std_error * scipy.stats.t._ppf((1+confidence)/2., len(data)-1)
    return width

tvals=[]
avals=[]
pvals=[]
errors=[]
N=0
inputfile=open(args.input, "r")
min_error = 100
max_error = -100
for line in inputfile.readlines():
    [dt_str, act_str, pred_str]=line.split(',')
    #dt=datetime.datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")        # 2013-07-12 09:10:00
    actual=float(act_str)
    predicted=float(pred_str)

    tvals.append(dt_str)
    avals.append(actual)
    pvals.append(predicted)
    error=actual-predicted
    errors.append(error)
    N+=1
    if error<min_error: min_error=error
    if error>max_error: max_error=error

# print(min_error)
# print(max_error)
# for i in range(0,N):
#     print ("%f" % (errors[i]))
# sys.exit(0)

def get_count_in_range(data,lb,ub):
    yc=0
    for i in range(0,len(data)):
        if data[i]>=lb and data[i]<=ub:
            yc+=1
    return yc

mean=get_mean(errors)
print("Mean Error, %f" % (mean))

# brute-force to get what we want
def get_lb_ub(data,pctg):
    N=len(data)
    mean=get_mean(data)
    lb=mean
    ub=mean
    yc=0
    while True:
        yc=get_count_in_range(data,lb,ub)
        if 1.0*yc/N < pctg:
            lb-=0.1
            ub+=0.1
        else:
            break
    return (lb,ub,yc,1.0*yc/N)

width=100
for i in range(0,int(len(errors)/width)):
    (lb,ub,yes_count,p)=get_lb_ub(errors[width*i:width*(i+1)],0.95);   print ("step %d, lb=%f, ub=%f, width=%f" % (i*width, lb,ub,ub-lb))
sys.exit(0)

std=numpy.std(errors)
print("STD,%f" % std)


conf_interval=mean_confidence_interval(errors, 0.95)
print("95%% Conf.Int., %f" % (conf_interval))

(m,s)=bayes_CF(errors,0.95)
(m_center, (m_lower, m_upper))=m
print("bayes_CF mean=%f %f %f" % (m_center, m_lower, m_upper))
yes_count=get_count_in_range(errors,m_lower,m_upper)
print("yc=%d / %d = %f" % (yes_count, N, 1.0*yes_count/N))

# verify that this means what we think it means
yes_count=get_count_in_range(errors,mean-conf_interval,mean+conf_interval)
print("yc=%d / %d = %f" % (yes_count, N, 1.0*yes_count/N))

# print("Time, LCL, UCL, Actual")
# for i in range(0,N):
#     print("%s, %f, %f" % (tvals[i], pvals[i]+mean-conf_interval, pvals[i]+mean+conf_interval, avals[i]))

