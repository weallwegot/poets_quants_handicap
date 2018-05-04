import os
import itertools
import re


import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import *

from data_preprocessing import preprocess_data

# setup the random state
RANDOM_STATE = 545510477
OUT_DIR = os.path.join(os.path.dirname(__file__),'data_out')

IN_FILE_NAME = 'pq_data_4_24_18.csv'
# IN_FILE_NAME = 'pq_data_10_20_17.csv'
IN_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data_out',IN_FILE_NAME)
OUT_FILE_PATH = os.path.join(OUT_DIR,"{}_processed.csv".format(IN_FILE_NAME.replace('.csv','')))
input_data_df = pd.read_csv(IN_FILE_PATH)



processed_df = preprocess_data(data_df=input_data_df,output_path=OUT_FILE_PATH)



#input: X_train, Y_train
#output: Y_pred
def logistic_regression_pred(X_train, Y_train):
	#train a logistic regression classifier using X_train and Y_train. Use this to predict labels of X_train
	#use default params for the classifier
	lr_model = LinearRegression(random_state=RANDOM_STATE)
	lr_model.fit(X_train,Y_train)
	Y_pred = lr_model.predict(X_train)
	return Y_pred

"""
TODO: Parse out the csv from pure text into features that can be used for ML algorithms
TODO: try out with linear regression for predicting percent likelihood of admission
"""

