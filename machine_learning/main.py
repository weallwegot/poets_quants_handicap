import os

import pandas as pd

from data_preprocessing import preprocess_data
from models import linear_regression_pred,linear_ridge_pred,linear_ridge_cv_pred,display_metrics


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
	predicted_labels_lr = linear_regression_pred(features,labels)

	predicted_labels_ridge = linear_ridge_pred(features,labels)

	predicted_labels_ridge_cv = linear_ridge_cv_pred(features,labels)


	# display metrics for predicting on the training data for each model
	display_metrics("Linear Regression for {}".format(school),predicted_labels_lr,labels)

	display_metrics("Ridge for {}".format(school),predicted_labels_ridge,labels)

	display_metrics("Ridge with Parameter Tuning for {}".format(school),predicted_labels_ridge_cv,labels)



