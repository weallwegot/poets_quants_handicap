import itertools
import re


import pandas as pd
import numpy as np

from catboost import Pool, FeaturesData

from constants import SCHOOLS_REVERSED, TARGET_LABELS


def _parse_str_nums(num_string):
    """
    parse strings of numbers and take averages if there are multiple

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

    num_string.upper().replace("ZERO", "0").replace("Forget it", "0")
    # regex to find numbers
    nums = re.findall(r'\d+', num_string)

    # but if theres only one number, then we know its NOT a range and thus we can look for negative numbers
    if len(nums) == 1:
        nums = re.findall(r'[+-]?\d+(?:\.\d+)?', num_string)

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
    divied_list_percent = [entry.rsplit('%', 1) for entry in divied_list_split_colon]
    # recombine list of lists into one list of strings
    divied_list_percent = _squash_nested_lists(divied_list_percent)
    # split again on last occurence of new lines
    # some snarky assessments have only text and no percent sign; i.e. "Forget it" or "Zero"
    divied_list_of_lists = [entry.rsplit('\n', 1) for entry in divied_list_percent]
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
    stem_majors = ['Engineering', 'STEM']
    # get all the majors that are not in the stem category
    nonstem_majors = list(set(list(data.MAJOR.values)) - set(stem_majors))

    majors_df = data.MAJOR

    stem_replaced = majors_df.replace(to_replace=stem_majors, value=1.0)

    new_majors_col = stem_replaced.replace(to_replace=nonstem_majors, value=0.0)

    df_without_major_col = data.drop(['MAJOR'], axis=1, inplace=False)

    reduced_df = df_without_major_col.join(pd.DataFrame({'STEM_MAJOR': new_majors_col}))

    # print reduced_df

    return reduced_df


def _reduce_race_dimensionality(data):
    """
    The original dataset has a high number of races specified
    The dimensionality of the expanded numeric representation probably
    hurts the model performance (in theory)
    Thus we are reducing the dimensionality by combining all the underrepresented into one category
    and all the others into another
    """
    underrepresented = ['Black', 'Latinx', 'Native American']
    # get all the non-under represented races
    non_underrepresented = list(set(list(data.RACE.values)) - set(underrepresented))

    races_df = data.RACE

    replace_races = races_df.replace(to_replace=underrepresented, value=1.0)

    race_column = replace_races.replace(to_replace=non_underrepresented, value=0.0)

    df_without_race_col = data.drop(['RACE'], axis=1, inplace=False)

    reduced_df = df_without_race_col.join(pd.DataFrame({'UNDER_REP': race_column}))

    return reduced_df


def _reduced_university_dimensionality(data):
    """
    Use only binary classification. Tier 1 University Yes / No
    """

    name_brand_schools = ['Tier 1', 'Tier 2']

    small_schools = ['Tier 3']

    uni_df = data.UNIVERSITY

    replace_uni = uni_df.replace(to_replace=name_brand_schools, value=1.0)

    uni_column = replace_uni.replace(to_replace=small_schools, value=0.0)

    df_without_uni_col = data.drop(['UNIVERSITY'], axis=1, inplace=False)

    reduced_df = df_without_uni_col.join(pd.DataFrame({'NAME_BRAND_SCHOOL': uni_column}))

    return reduced_df


def _reduce_gender_dimensionality(data):
    """
    Use only binary classification for simplifying dimensions
    """

    gen_df = data.GENDER

    replace_gen = gen_df.replace(to_replace=['Female'], value=1.0)

    gen_column = replace_gen.replace(to_replace=['MALE'], value=0.0)

    df_without_gen_col = data.drop(['GENDER'], axis=1, inplace=False)

    reduced_df = df_without_gen_col.join(pd.DataFrame({'FEMALE': gen_column}))

    return reduced_df


def _drop_unused_and_expand_categorical_columns(data):
    """
    Drop data columns that were unused or have mostly NaNs
    Expand categorical datas so they can be represented numerically
    """
    # drop unused columns
    data_after_drop = data.drop(['ODDS', 'INTERNATIONAL', 'JOBTITLE', 'AGE'], axis=1, inplace=False)
    # dropped_data = data.drop(['ODDS','INTERNATIONAL','JOBTITLE','UNIVERSITY','MAJOR','GENDER','RACE'],axis=1,inplace=False)

    # #change categorical data into numeric
    # categorical_cols = ['UNIVERSITY','MAJOR','GENDER','RACE']
    # # categorical_cols = []
    # df_processed = pd.get_dummies(data=data_after_drop,columns=categorical_cols)
    return data_after_drop


def preprocess_data_4_catboost(data_df, output_path=None):
    """
    preprocess data for working with gradient boosting techniques
    specifically with the catboost library. since this is going to use
    the preprocessing built into the catboost library there are slightly
    different steps to be done
    """

    """
	train_data = Pool(
		data=FeaturesData(
			num_feature_data=np.array([[1, 4, 5, 6], 
									   [4, 5, 6, 7], 
									   [30, 40, 50, 60]], 
									   dtype=np.float32),
			cat_feature_data=np.array([[b"a", b"b"], 
									   [b"a", b"b"], 
									   [b"c", b"d"]], 
									   dtype=object)
		),
		label=[1, 1, -1]
	)
	"""

    new_df_w_labels = data_df.copy()
    for idx, odds_string in data_df.ODDS.iteritems():
        # skip data qual errors and abnormalities
        if not isinstance(odds_string, str):
            continue

        divied_list = _preprocess_odds_string(odds_string)
        for school_or_perc in divied_list:
            if school_or_perc in SCHOOLS_REVERSED.keys():
                school_idx = divied_list.index(school_or_perc)
                # the percent is always the next index after the school
                perc = divied_list[school_idx + 1]
                # print "School: {};Odds: {}".format(school_or_perc,perc)
                # use the standardized name
                standard_school_name = SCHOOLS_REVERSED[school_or_perc]
                # insert the specific name value for the correct row
                new_df_w_labels.at[idx, standard_school_name] = _parse_str_nums(perc)

    new_df_w_labels = _reduce_majors_dimensionality(new_df_w_labels)

    # drop unused columns
    data_after_drop = new_df_w_labels.drop(['ODDS', 'INTERNATIONAL', 'JOBTITLE'], axis=1, inplace=False)

    # change categorical data into numeric
    categorical_cols = ['UNIVERSITY', 'MAJOR', 'GENDER', 'RACE']

    # a dataframe of ONLY the features
    features_only_df = data_after_drop.drop(TARGET_LABELS, axis=1, inplace=False)
    # determine the columns that are features by subtracting from labels
    feature_cols = set(data_after_drop.columns) - set(TARGET_LABELS)
    # a dataframe with ONLY labels
    labels = data_after_drop.drop(feature_cols, axis=1, inplace=False)

    multi_data_set_dict = {}
    for school in labels.columns:

        df_for_school = features_only_df.join(pd.DataFrame({school: labels[school]}))
        # a holder dictionary that contains the features numpy ndarray for features and numpy ndarray for school label
        school_dict = {}
        # drop the NaNs from the dataset in any feature column or label. otherwise model training will fail
        df_for_school.dropna(inplace=True)
        # store the features as a numpy ndarray to be fed directly to model training

        numerical_features_np_array = df_for_school.drop([school] + categorical_cols, axis=1, inplace=False).values

        categorical_features_np_array = df_for_school[categorical_cols].values
        # store the labels for a particular school as a numpy ndarray to be fed directly to model training
        labels_as_list = df_for_school.drop(feature_cols, axis=1, inplace=False)[school].tolist()

        datasetpool = Pool(
            data=FeaturesData(
                num_feature_data=np.array(numerical_features_np_array,
                                          dtype=np.float32),
                cat_feature_data=np.array(categorical_features_np_array,
                                          dtype=object)
            ),
            label=labels_as_list
        )

        multi_data_set_dict[school] = datasetpool

    return multi_data_set_dict


def preprocess_data(data_df, output_path=None):
    """
    preprocess data for general regression modeling
    combines many steps such as working with the odds strings
    and one hot encoding categorical features

    input is a pandas dataframe of features and labels 

    output is a dictionary of datasets, where each key
    is the feature set + lables for one school.
    Since each school uses its own model, each school also needs its
    own set of features/labels
    """

    new_df_w_labels = data_df.copy()
    for idx, odds_string in data_df.ODDS.iteritems():
        # skip data qual errors and abnormalities
        if isinstance(odds_string, bytes):
            odds_string = odds_string.decode("utf-8")
        elif not isinstance(odds_string, str):
            continue
        else:
            print(odds_string)
            print(type(odds_string))

        divied_list = _preprocess_odds_string(odds_string)
        for school_or_perc in divied_list:
            if school_or_perc in SCHOOLS_REVERSED.keys():
                school_idx = divied_list.index(school_or_perc)
                perc = divied_list[school_idx + 1]
                # print "School: {};Odds: {}".format(school_or_perc,perc)
                # use the standardized name
                standard_school_name = SCHOOLS_REVERSED[school_or_perc]
                # insert the specific name value for the correct row
                new_df_w_labels.at[idx, standard_school_name] = _parse_str_nums(perc)

    # dataset currently has a ton of majors as categories. try combining them into STEM/NonSTEM to reduce dimensionality
    new_df_w_labels = _reduce_majors_dimensionality(new_df_w_labels)
    new_df_w_labels = _reduce_race_dimensionality(new_df_w_labels)
    new_df_w_labels = _reduced_university_dimensionality(new_df_w_labels)

    new_df_w_labels = _reduce_gender_dimensionality(new_df_w_labels)
    df_processed = _drop_unused_and_expand_categorical_columns(new_df_w_labels)

    # write dataframe to csv after processing for debugging and things
    if output_path:
        df_processed.to_csv(output_path)

    # a dataframe of ONLY the features

    features_only_df = df_processed.drop(TARGET_LABELS, axis=1, inplace=False)
    # determine the columns that are features by subtracting from labels
    feature_cols = set(df_processed.columns) - set(TARGET_LABELS)
    # a dataframe with ONLY labels
    labels = df_processed.drop(feature_cols, axis=1, inplace=False)

    multi_data_set_dict = {}
    # create a new dataset for each school that we are modeling
    for school in labels.columns:
        # create a dataframe with all the features and the labels for a particular school
        df_for_school = features_only_df.join(pd.DataFrame({school: labels[school]}))
        # a holder dictionary that contains the features numpy ndarray for features and numpy ndarray for school label
        school_dict = {}
        # drop the NaNs from the dataset in any feature column or label. otherwise model training will fail
        df_for_school.dropna(inplace=True)
        # store the features as a numpy ndarray to be fed directly to model training
        school_dict['features'] = df_for_school.drop([school], axis=1, inplace=False)
        # store the labels for a particular school as a numpy ndarray to be fed directly to model training
        school_dict['labels'] = df_for_school.drop(feature_cols, axis=1, inplace=False)
        # store the FEATURES & LABELS for a PARTICULAR SCHOOL in the dictionary
        multi_data_set_dict[school] = school_dict

    feature_col_names = features_only_df.columns
    return multi_data_set_dict, feature_col_names
