from sklearn.linear_model import LinearRegression, SGDRegressor, ElasticNet, Lasso, Ridge, RidgeCV
from sklearn.svm import LinearSVR
from sklearn.metrics import *

from constants import RANDOM_STATE


#input: X_train, Y_train
#output: Y_pred
def linear_regression_pred(X_train, Y_train):
	"""
	Train a Linear Regression model with default hyperparameters
	"""

	lr_model = LinearRegression()
	lr_model.fit(X_train,Y_train)
	Y_pred = lr_model.predict(X_train)
	return Y_pred

def linear_sgd_pred(X_train, Y_train):
	"""
	Train a linear model with Stochastic Gradient Descent
	"""

	sgd_model = SGDRegressor(random_state=RANDOM_STATE)
	sgd_model.fit(X_train,Y_train)
	Y_pred = sgd_model.predict(X_train)
	return Y_pred


def linear_svr_pred(X_train, Y_train):
	"""
	Train a linear model with Support Vector Regression
	"""

	svr_model = LinearSVR(random_state=RANDOM_STATE)
	svr_model.fit(X_train,Y_train)
	Y_pred = svr_model.predict(X_train)
	return Y_pred

def linear_elasticnet_pred(X_train, Y_train):
	"""
	Train a linear model with Elastic Net
	"""

	enet_model = ElasticNet(random_state=RANDOM_STATE)
	enet_model.fit(X_train,Y_train)
	Y_pred = enet_model.predict(X_train)
	return Y_pred

def linear_lasso_pred(X_train, Y_train):
	"""
	Train a linear model with Lasso Regularization
	"""

	lasso_model = Lasso(random_state=RANDOM_STATE)
	lasso_model.fit(X_train,Y_train)
	Y_pred = lasso_model.predict(X_train)
	return Y_pred


def linear_ridge_pred(X_train, Y_train):
	"""
	Train a linear model with Ridge regularization
	"""

	ridge_model = Ridge(random_state=RANDOM_STATE)
	ridge_model.fit(X_train,Y_train)
	Y_pred = ridge_model.predict(X_train)
	return Y_pred

def linear_ridge_cv_pred(X_train, Y_train):
	"""
	Train a linear model with Ridge regularization but cross validations
	across different learning rates
	"""

	ridge_model = RidgeCV(alphas=[0.1,0.3,0.5,1.0,10.0])
	ridge_model.fit(X_train,Y_train)
	Y_pred = ridge_model.predict(X_train)
	return Y_pred

#input: Y_pred,Y_true
#output: accuracy, auc, precision, recall, f1-score
def classification_metrics(Y_pred, Y_true):
	#NOTE: It is important to provide the output in the same order
	# mean_abs = mean_absolute_error(y_true=Y_true,y_pred=Y_pred)
	mean_squared = mean_squared_error(y_true=Y_true,y_pred=Y_pred)
	r2 = r2_score(y_true=Y_true,y_pred=Y_pred)
	exp_var = explained_variance_score(y_true=Y_true,y_pred=Y_pred)
	return mean_squared,exp_var,r2

#input: Name of classifier, predicted labels, actual labels
def display_metrics(classifierName,Y_pred,Y_true):
	print("______________________________________________")

	print("Classifier: {}\n".format(classifierName))
	mean_squared,exp_var_score,r2 = classification_metrics(Y_pred,Y_true)
	print("Mean Squared Error: {}\n".format(mean_squared))
	print("Explained Variance Score: {}\n".format(exp_var_score))
	print("R2 Coefficient of Determination: {}\n".format(r2))
	print("______________________________________________")
	print("")