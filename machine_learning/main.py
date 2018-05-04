import os
import itertools
import re


import pandas as pd
import numpy as np

from sklearn.linear_model import LinearRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import *

# setup the random state
RANDOM_STATE = 545510477
OUT_DIR = os.path.join(os.path.dirname(__file__),'data_out')

IN_FILE_NAME = 'pq_data_4_24_18.csv'
# IN_FILE_NAME = 'pq_data_10_20_17.csv'
IN_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data_out',IN_FILE_NAME)
OUT_FILE_PATH = os.path.join(OUT_DIR,"{}_processed.csv".format(IN_FILE_NAME.replace('.csv','')))
data_df = pd.read_csv(IN_FILE_PATH)

# schools and their synonyms for label creation
SCHOOLS = {'Harvard':['Harvard'],
		   'Stanford':['Stanford'],
		   'Berkeley':['Berkeley','Haas'],
		   'Wharton':['Wharton'],
		   'Tuck':['Tuck','Dartmouth'],
		   'Kellogg':['Kellogg','Northwestern'],
		   'Cornell':['Cornell'],
		   'Duke':['Duke'],
		   'Booth':['Booth','Chicago'],
		   'Columbia':['Columbia'],
		   'Michigan':['Michigan','Ross'],
		   'NYU':['NYU','New York University'],
		   'UCLA':['UCLA','Anderson'],
		   'Sloan':['Sloan','MIT'],
		   'Yale':['Yale'],
		   'INSEAD':['INSEAD']
			}

# create another dictionary with the keys and values reversed
SCHOOLS_REVERSED = {}
for k,v in SCHOOLS.iteritems():
	for name in v:
		SCHOOLS_REVERSED[name] = k

print SCHOOLS_REVERSED

def _parse_str_nums(num_string):
	"""
	parse strings of numbers and take averages if there are multiple
	i.e for odds strings like: "40% to 50%" returns 45.0
	"""
	num_string.upper().replace("ZERO","0").replace("Forget it","0")
	# regex to find numbers
	# negative numbers. hard to distinguish from ranges given as "30-50"
	nums = re.findall('\d+',num_string)
	# cast strings to ints
	nums = [int(n) for n in nums]
	# average ints
	averaged = np.average(np.asarray(nums))

	return averaged
def _squash_nested_lists(l_of_l):
	"""
	compress list of lists into one single list
	"""
	return list(itertools.chain.from_iterable(l_of_l))

# TODO: do we care about case sensitivity?
def _preprocess_odds_string(string_of_odds):
	# split on colons
	divied_list_split_colon = string_of_odds.split(':')
	# split on last occurrence of '%' using rsplit 
	divied_list_percent = [entry.rsplit('%',1) for entry in divied_list_split_colon]
	# recombine list of lists into one list of strings
	divied_list_percent = _squash_nested_lists(divied_list_percent)
	# split again on last occurence of new lines
	# some snarky assessments have only text; i.e. "Forget it" or "Zero"
	divied_list_of_lists = [entry.rsplit('\n',1) for entry in divied_list_percent]
	# recombine list of lists into one continues list
	compressed_divied_list = _squash_nested_lists(divied_list_of_lists)
	# strip spaces for matches... 
	compressed_divied_list = [entry.strip() for entry in compressed_divied_list]

	return compressed_divied_list


def _process_data_df(data):
	#drop unused columns
	data.drop(['ODDS','INTERNATIONAL','JOBTITLE'],axis=1,inplace=True)
	#change categorical data into numeric
	categorical_cols = ['UNIVERSITY','MAJOR','GENDER','RACE']
	df_processed = pd.get_dummies(data=data,columns=categorical_cols)
	return df_processed

def create_odds_labels():
	new_df_w_labels = data_df.copy()
	for idx,odds_string in data_df.ODDS.iteritems():
		# skip data qual errors and abnormalities
		if not isinstance(odds_string,str):
			continue

		divied_list = _preprocess_odds_string(odds_string)
		for school_or_perc in divied_list:
			if school_or_perc in SCHOOLS_REVERSED.keys():
				school_idx = divied_list.index(school_or_perc)
				perc = divied_list[school_idx+1]
				# print "School: {};Odds: {}".format(school_or_perc,perc)
				# use the standardized name
				standard_school_name = SCHOOLS_REVERSED[school_or_perc]
				# insert the specific name value for the correct row
				new_df_w_labels.at[idx,standard_school_name] = _parse_str_nums(perc)

	df_processed = _process_data_df(new_df_w_labels)
	df_processed.to_csv(OUT_FILE_PATH)
	print df_processed
	return df_processed

create_odds_labels()



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

