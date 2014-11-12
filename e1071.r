library("e1071")

# dataset1 <- maml.mapInputPort(1) # class: data.frame
# training_data=array(data=dataset1, dim=c(5,2))

training_data=array(data=c(10,9,9,10,11,10,11,11,9,10), dim=c(2,5))
model <- svm(training_data, 
			factor(rep(1,dim(training_data)[1])), 
			scale=TRUE, 
			type="one-classification")

data.coefs=data.frame(model["coefs"], model["SV"], model["index"], model["x.scale"])

validation_data=array(data=c(10,10,9,9,8,8), dim=c(3,2))
preds<-predict(model, validation_data)

# maml.mapOutputPort("data.coefs");