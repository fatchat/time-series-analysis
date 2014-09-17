library("e1071")
training_data=array(data=c(10,9,9,10,11,10,11,11,9,10), dim=c(10,1))
model <- svm(training_data, factor(rep(1,dim(training_data)[1])), scale=TRUE, type="one-classification")
model["SV"]
model["index"]
model["coefs"]
