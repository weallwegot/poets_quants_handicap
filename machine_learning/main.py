import os

import pandas as pd
import numpy as np

from data_preprocessing import preprocess_data, preprocess_data_4_catboost
from models import fit_train_test_cv,gboosting_train_test,catboost_pred,gboosting_pred,linear_regression_pred,linear_ridge_pred,linear_ridge_cv_pred,display_metrics
from ML_AP import ApplicantProfile
from constants import SCHOOLS_REVERSED, TARGET_LABELS

from sklearn.linear_model import LinearRegression, SGDRegressor, ElasticNet, Lasso, Ridge, RidgeCV
from sklearn.ensemble import GradientBoostingRegressor



OUT_DIR = os.path.join(os.path.dirname(__file__),'data_out')

IN_FILE_NAME = 'pq_data_4_24_18.csv'
IN_FILE_NAME2 = 'pq_data_10_20_17.csv'
IN_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data_out',IN_FILE_NAME)
IN_FILE_PATH2 = os.path.join(os.path.dirname(os.path.dirname(__file__)),'data_out',IN_FILE_NAME2)

OUT_FILE_PATH = os.path.join(OUT_DIR,"{}_processed.csv".format(IN_FILE_NAME.replace('.csv','')))
input_data_df = pd.read_csv(IN_FILE_PATH)
other_data_df = pd.read_csv(IN_FILE_PATH2)

combined_df = input_data_df.append(other_data_df)

combined_df.reset_index(inplace=True)


# catboost_data_dict = preprocess_data_4_catboost(data_df=input_data_df)

# for school, catboostpool in catboost_data_dict.items():

# 	predicted_labels = catboost_pred(catboostpool)

# 	labels = catboostpool.get_label()

# 	display_metrics("Catboost for {}".format(school),predicted_labels,labels)



school_data_dict,colnames = preprocess_data(data_df=combined_df,output_path=OUT_FILE_PATH)
print(colnames)
MODELS = {}
# would use iteritems, but what if i want to port to python 3.5
for school,feature_label_d in school_data_dict.items():

	features = feature_label_d['features'].values
	labels = feature_label_d['labels'].values

	print "Number of Samples for {}: {}\n".format(school,features.shape[0])

	# drop indices from the model
	features = np.delete(features,0,axis=1)

	# test model against train data. we are using ALL of the data for training. 
	# Not splitting for cross validation because the dataset for each school is TINY
	# predicted_labels_lr = linear_regression_pred(features,labels)

	# predicted_labels_ridge = linear_ridge_pred(features,labels)

	# predicted_labels_ridge_cv = linear_ridge_cv_pred(features,labels)

	# predicted_labels_gboost = gboosting_pred(features,labels)


	# colnames[1:] so you dont include index
	model = fit_train_test_cv(model_obj=None,X_train=features,Y_labels=labels,column_names=colnames[1:])


	#real_gb,preds_gb = gboosting_train_test(features,labels)

	# display metrics for predicting on the training data for each model

	#display_metrics("Gboost Regression for {}".format(school),preds_gb,real_gb)

	# display_metrics("Linear Regression for {}".format(school),predicted_labels_lr,labels)

	# display_metrics("Ridge for {}".format(school),predicted_labels_ridge,labels)

	# display_metrics("Ridge with Parameter Tuning for {}".format(school),predicted_labels_ridge_cv,labels)

	MODELS[school] = model

def find_my_chances(gpa,gmat,age,race,university,major,gender):

	# create list of strings to trigger the applicant profile parsing
	gpa_str = "{} GPA".format(gpa)
	gmat_str = "{} GMAT".format(gmat)
	demo_str = "{a} year old {r} {g}".format(a=age,r=race,g=gender)
	school_info = "Degree in {m} at {uni} (University)".format(m=major,uni=university)

	app_profile = [gpa_str,gmat_str,demo_str,school_info]
	odds = ""
	for school in TARGET_LABELS:
		odds += "{}: 0.0\n".format(school)
	ap = ApplicantProfile(app_profile,odds)



	d = {}
	d["GMAT"] = ap.gmat_score
	d["GPA"] = ap.gpa
	d["UNIVERSITY"] = ap.uni
	d["MAJOR"] = ap.major
	d["JOBTITLE"] = ap.job_title
	d["GENDER"] = ap.gender
	d["RACE"] = ap.race
	d["AGE"] = ap.age
	d["INTERNATIONAL"] = ap.international
	d["ODDS"] = ap.odds.encode('utf-8').strip()

	df = pd.DataFrame(d,index=[0])
	schooldata_dict,mycolnames = preprocess_data(df)


	print("\n {d}".format(d=d))
	for school,indf in schooldata_dict.items():

		# if missing any columns from training set, add them w/ dummy vals
		for col in colnames:
			if col not in indf['features'].columns:
				indf['features'][col] = 0.0


		features_df = indf['features'][colnames]

		#print(features_df)


		df2predictfrom = features_df.values
		df2predictfrom = np.delete(df2predictfrom,0,axis=1)

		chance = MODELS[school].predict(df2predictfrom)
		try:
			pass
			#print("Coefficients: {}".format(MODELS[school].coef_))
		except AttributeError as ae:
			continue

		if school in ['Harvard','Wharton','Stanford','Booth']:
			print("{s} odds: {c}".format(s=school,c=chance))


find_my_chances(
	gpa=4.0,
	gmat=800,
	age=21,
	race='black',
	university='stanford university',
	major='chemical engineering',
	gender='male')

