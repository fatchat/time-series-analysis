# R code to send package list to an ML Azure output port
out <- data.frame(installed.packages())
maml.mapOutputPort("out")