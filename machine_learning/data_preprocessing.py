import itertools
import re


import pandas as pd
import numpy as np

from constants import SCHOOLS_REVERSED, TARGET_LABELS




def _parse_str_nums(num_string):
	"""
	parse strings of numbers and take averages if there are multiple
	Since negative numbers dont occurr that often we are just 
	
	:param num_string: a string of numbers and text
	:type num_string: String

	:return: float of the number found or average of multiple numbers found
	:rtype: Float

	:example:
		>>> _parse_str_nums("40% to 50%")
		>>> 45.
		>>> _parse_str_nums("30%-50%")
		>>> 40.
		>>> _parse_str_nums("-20%")
		>>> -20.

	"""

	num_string.upper().replace("ZERO","0").replace("Forget it","0")
	# regex to find numbers
	nums = re.findall('\d+',num_string)

	# but if theres only one number, then we know its NOT a range and thus we can look for negative numbers
	if len(nums) == 1:
		nums = re.findall('[+-]?\d+(?:\.\d+)?',num_string)

	# cast strings to ints
	nums = [int(n) for n in nums]
	# average ints derived from string
	averaged = np.average(np.asarray(nums))

	return averaged

def _squash_nested_lists(l_of_l):
	"""
	compress list of lists into one single list

	:param l_of_l: list of lists
	:type l_of_l: List

	:return: single list with all elements of list of list
	:rtype: List

	:example:
		>>> _squash_nested_list([['a','b'],['c'],['d','e']])
		>>> ['a','b','c','d','e']

	"""
	return list(itertools.chain.from_iterable(l_of_l))

# TODO: do we care about case sensitivity?
def _preprocess_odds_string(string_of_odds):
	"""
	:param string_of_odds: string scraped from site describing an applicants odds of admittance
	:type string_of_odds: String

	:return: list of strings with entries for either schools or percent chances
	:rtype: list

	:example:
		>>> _preprocess_odds_string("Harvard Business School: 85% Stanford: 80% Wharton: 90% Tuck: 95% Kellogg: 95%")
		>>> ['Harvard Business School', '85', 'Stanford', '80', 'Wharton', '90', 'Tuck', '95', 'Kellogg', '95', '']
	"""
	# split on colons
	divied_list_split_colon = string_of_odds.split(':')
	# split on last occurrence of '%' using rsplit 
	divied_list_percent = [entry.rsplit('%',1) for entry in divied_list_split_colon]
	# recombine list of lists into one list of strings
	divied_list_percent = _squash_nested_lists(divied_list_percent)
	# split again on last occurence of new lines
	# some snarky assessments have only text and no percent sign; i.e. "Forget it" or "Zero"
	divied_list_of_lists = [entry.rsplit('\n',1) for entry in divied_list_percent]
	# recombine list of lists into one continuous list
	compressed_divied_list = _squash_nested_lists(divied_list_of_lists)
	# strip spaces for every entry
	compressed_divied_list = [entry.strip() for entry in compressed_divied_list]

	return compressed_divied_list

def _reduce_majors_dimensionality(data):
	"""
	The original dataset has a high number of majors specified
	The dimensionality of the expanded numeric representation probably
	hurts the model performance (in theory)
	Thus we are reducing the dimensionality by combining all the stem into one category
	and all the non stem into another category.
	"""
	stem_majors = ['Engineering','STEM']
	# get all the majors that are not in the stem category
	nonstem_majors = list(set(list(data.MAJOR.values)) - set(stem_majors))
	majors_df = data.MAJOR
	stem_replaced = majors_df.replace(to_replace=stem_majors,value='STEM')
	reduced_majors_df = stem_replaced.replace(to_replace=nonstem_majors,value='NonSTEM')

	drop_major_df = data.drop(['MAJOR'],axis=1,inplace=False)

	reduced_df = drop_major_df.join(pd.DataFrame({'MAJOR':reduced_majors_df}))

	print reduced_df

	return reduced_df




def _drop_unused_and_expand_categorical_columns(data):
	"""
	Drop data columns that were unused or have mostly NaNs
	Expand categorical datas so they can be represented numerically
	"""
	#drop unused columns
	dropped_data = data.drop(['ODDS','INTERNATIONAL','JOBTITLE'],axis=1,inplace=False)
	# dropped_data = data.drop(['ODDS','INTERNATIONAL','JOBTITLE','UNIVERSITY','MAJOR','GENDER','RACE'],axis=1,inplace=False)

	#change categorical data into numeric
	categorical_cols = ['UNIVERSITY','MAJOR','GENDER','RACE']
	# categorical_cols = []
	df_processed = pd.get_dummies(data=dropped_data,columns=categorical_cols)
	return df_processed

def preprocess_data(data_df,output_path=None):
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

	# dataset currently has a ton of majors as categories. try combining them into STEM/NonSTEM to reduce dimensionality
	# new_df_w_labels = _reduce_majors_dimensionality(new_df_w_labels)
	df_processed = _drop_unused_and_expand_categorical_columns(new_df_w_labels)

	# write dataframe to csv after processing for debugging and things
	if output_path:
		df_processed.to_csv(output_path)


	# a dataframe of ONLY the features
	features_only_df = df_processed.drop(TARGET_LABELS,axis=1,inplace=False)
	# determine the columns that are features by subtracting from labels
	feature_cols = set(df_processed.columns) - set(TARGET_LABELS)
	# a dataframe with ONLY labels
	labels = df_processed.drop(feature_cols,axis=1,inplace=False)

	multi_data_set_dict = {}
	# create a new dataset for each school that we are modeling
	for school in labels.columns:
		# create a dataframe with all the features and the labels for a particular school
		df_for_school = features_only_df.join(pd.DataFrame({school:labels[school]}))
		# a holder dictionary that contains the features numpy ndarray for features and numpy ndarray for school label
		school_dict = {}
		# drop the NaNs from the dataset in any feature column or label. otherwise model training will fail
		df_for_school.dropna(inplace=True)
		# store the features as a numpy ndarray to be fed directly to model training
		school_dict['features'] = df_for_school.drop([school],axis=1,inplace=False).values
		# store the labels for a particular school as a numpy ndarray to be fed directly to model training
		school_dict['labels'] = df_for_school.drop(feature_cols,axis=1,inplace=False).values
		# store the FEATURES & LABELS for a PARTICULAR SCHOOL in the dictionary 
		multi_data_set_dict[school] = school_dict



	return multi_data_set_dict







