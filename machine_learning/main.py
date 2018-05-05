import os

import pandas as pd

from data_preprocessing import preprocess_data
from models import linear_regression_pred,display_metrics

# setup the random state for fitting
RANDOM_STATE = 545510477
OUT_DIR = os.path.join(os.path.dirname(__file__),'data_out')

IN_FILE_NAME = 'pq_data_4_24_18.csv'
# IN_FILE_NAME = 'pq_data_10_20_17.csv'
IN_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data_out',IN_FILE_NAME)
OUT_FILE_PATH = os.path.join(OUT_DIR,"{}_processed.csv".format(IN_FILE_NAME.replace('.csv','')))
input_data_df = pd.read_csv(IN_FILE_PATH)



school_data_dict = preprocess_data(data_df=input_data_df,output_path=OUT_FILE_PATH)

# would use iteritems, but what if i want to port to python 3.5
for school,feature_label_d in school_data_dict.items():

	features = feature_label_d['features']
	labels = feature_label_d['labels']

	print "Number of Samples for {}: {}\n".format(school,features.shape[0])

	# test model against train data. we are using ALL of the data for training. 
	# Not splitting for cross validation because the dataset for each school is TINY
	predicted_labels = linear_regression_pred(features,labels)

	# display metrics for predicting on the training data for each model
	display_metrics("LinearRegression for {}".format(school),predicted_labels,labels)




