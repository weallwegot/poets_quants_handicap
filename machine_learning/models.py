from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import *


#input: X_train, Y_train
#output: Y_pred
def linear_regression_pred(X_train, Y_train):
	#train a logistic regression classifier using X_train and Y_train. Use this to predict labels of X_train
	#use default params for the classifier
	lr_model = LinearRegression()
	lr_model.fit(X_train,Y_train)
	Y_pred = lr_model.predict(X_train)
	return Y_pred

#input: Y_pred,Y_true
#output: accuracy, auc, precision, recall, f1-score
def classification_metrics(Y_pred, Y_true):
	#NOTE: It is important to provide the output in the same order
	mean_abs = mean_absolute_error(y_true=Y_true,y_pred=Y_pred)
	mean_squared = mean_squared_error(y_true=Y_true,y_pred=Y_pred)
	r2 = r2_score(y_true=Y_true,y_pred=Y_pred)
	# recall = recall_score(y_true=Y_true,y_pred=Y_pred)
	# f1score = f1_score(y_true=Y_true,y_pred=Y_pred)
	return mean_abs,mean_squared,r2

#input: Name of classifier, predicted labels, actual labels
def display_metrics(classifierName,Y_pred,Y_true):
	print("______________________________________________")

	print("Classifier: {}\n".format(classifierName))
	mean_abs, mean_squared, r2 = classification_metrics(Y_pred,Y_true)
	print("Mean Absolute Error: {}\n".format(mean_abs))
	print("Mean Squared Error: {}\n".format(mean_squared))
	print("R2 Coefficient of Determination: {}\n".format(r2))
	print("______________________________________________")
	print("")