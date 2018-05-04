import itertools
import re


import pandas as pd
import numpy as np

from constants import SCHOOLS_REVERSED




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

	df_processed = _process_data_df(new_df_w_labels)
	if output_path:
		df_processed.to_csv(output_path)
	print df_processed
	return df_processed