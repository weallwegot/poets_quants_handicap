#!/usr/bin/env python3
from flask import Flask, request, url_for, redirect
from flask import jsonify, session, current_app
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin
import json
import requests
import random
import os
import logging
import re
import pdb
import pickle
import numpy as np

from ML_AP import ApplicantProfile


ORDERED_FEATURE_INPUTS = ['gmat', 'gpa', 'major', 'race', 'university', 'gender']


# create logger with 'spam_application'
logger = logging.getLogger('mba_models')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('modelMBA.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

app = Flask(__name__)
# the directory of the curent file
working_dir = os.path.dirname(os.path.abspath(__file__))
with open(working_dir + os.sep + 'k.txt') as f:
    k = f.read()
content = k.strip()

app.secret_key = content

# api
api = Api(app)
# cors for cross origin headers
CORS(app)

# the directory of the curent file
working_dir = os.path.dirname(os.path.abspath(__file__))
# the data folder
data_folder_path = os.path.join(working_dir, "models")

VALID_OPTIONS = [f.replace('.pickle', '') for f in os.listdir(
    data_folder_path) if os.path.isfile(os.path.join(data_folder_path, f))]
"""
LyricalApi class takes a GET request
parses the keys, if the artist key is present
look up random lyric from said artist
if its not, look up random lyric from Cardi B

TODO: use jsonify instead of this weird lil custom dictionary thing, no?
"""


def return_constructor(code, body):
    return {
        'code': code,
        'body': body
    }


class ModelMBAApi(Resource):

    def post(self):
        json_data = request.get_json()
        logger.debug('json data received: {}'.format(json_data))

        try:
            school = json_data['school']
        except KeyError:
            logger.info('No school included, defaulting to Stanford')
            school = 'stanford'
        try:
            school_model = load_model(school)
        except FileNotFoundError as fe:
            e_msg = '{school} is not a valid option, try: {opts}'.format(school=school, opts=VALID_OPTIONS)
            logger.error(e_msg)
            return return_constructor(500, {'error': e_msg})

        if school_model:

            if is_direct_input(json_data):

                # features basically preprocessed already
                chance = find_my_chances_with_direct_inputs(
                    SCHOOL_MODEL=school_model,
                    json_data=json_data
                )

            else:
                # need to parse inputs to create features
                chance = find_my_chances_with_parsing(
                    SCHOOL_MODEL=school_model,
                    gpa=json_data['gpa'],
                    gmat=json_data['gmat'],
                    age=json_data['age'],
                    race=json_data['race'],
                    university=json_data['university'],
                    major=json_data['major'],
                    gender=json_data['male']
                )

            return return_constructor(200, {'chance': chance, 'school': school})

        else:
            return return_constructor(500, '{} is not a valid school option'.format(school))

    def get(self):
        return return_constructor(500, 'Get methods are not available, please provide a post body.')


def is_number(s):
    """check if a data type is numeric
    https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float?page=1&tab=votes#tab-top

    Arguments:
        s {[int,float,str]} -- input to test

    Returns:
        bool -- [description]
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_direct_input(data_from_post):
    """check if the input data type can be used directly in a model

    Arguments:
        data_from_post {[dict]} -- dictionary is of course
    """

    for k, v in data_from_post.items():

        if k.upper() == 'SCHOOL':
            continue
        if not is_number(v):
            return False

    logger.info('numeric only input: {}'.format(data_from_post))

    return True


def load_model(school):
    """
    Load model for a particular school from local filesystem
    """
    logger.debug('loading model for: {}'.format(school))

    school_model = None

    #model_path = data_folder_path + os.sep + school + '.pickle'
    model_path = os.path.join(data_folder_path, '{}.pickle'.format(school))
    logger.info('loading from: {}'.format(model_path))
    try:
        with open(model_path, 'rb') as f_h:
            school_model = pickle.load(f_h)

    except ValueError as ve:

        logger.error('Model for {s} is not available at {p}'
                     .format(s=school, p=model_path))

        school_model = None

    return school_model['model']


def find_my_chances_with_direct_inputs(SCHOOL_MODEL, json_data):
    """[summary]

    [description]

    Arguments:
        school {[type]} -- [description]
        gpa {[type]} -- [description]
        gmat {[type]} -- [description]
        age {[type]} -- [description]
        race {[type]} -- [description]
        university {[type]} -- [description]
        major {[type]} -- [description]
        gender {[type]} -- [description]
        SCHOOL_MODEL {[type]} -- [description]
    """

    z = []
    for x in ORDERED_FEATURE_INPUTS:
        z.append(float(json_data[x]))

    array_of_inputs = np.array(z)
    # reshape to create 2D array
    array_of_inputs = array_of_inputs.reshape(1, -1)
    chance = SCHOOL_MODEL.predict(array_of_inputs)
    # returns array of size 1
    return chance[0]


def find_my_chances_with_parsing(school, gpa, gmat, age, race, university, major, gender, SCHOOL_MODEL):

    # create list of strings to trigger the applicant profile parsing
    gpa_str = "{} GPA".format(gpa)
    gmat_str = "{} GMAT".format(gmat)
    demo_str = "{a} year old {r} {g}".format(a=age, r=race, g=gender)
    school_info = "Degree in {m} at {uni} (University)".format(m=major, uni=university)

    app_profile = [gpa_str, gmat_str, demo_str, school_info]
    odds = ""
    for school in TARGET_LABELS:
        odds += "{}: 0.0\n".format(school)
    ap = ApplicantProfile(app_profile, odds)

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

    df = pd.DataFrame(d, index=[0])
    schooldata_dict, mycolnames = preprocess_data(df)

    print("\n {d}".format(d=d))
    for school, indf in schooldata_dict.items():

        # if missing any columns from training set, add them w/ dummy vals
        for col in colnames:
            if col not in indf['features'].columns:
                indf['features'][col] = 0.0

        features_df = indf['features'][colnames]

        # print(features_df)

        df2predictfrom = features_df.values
        df2predictfrom = np.delete(df2predictfrom, 0, axis=1)

        chance = SCHOOL_MODEL.predict(df2predictfrom)

        return chance


@app.route('/')
def hello_world():
    return redirect("https://andcomputers.io", code=302)


api.add_resource(ModelMBAApi, '/api/v1')


if __name__ == "__main__":
    app.run(threaded=True)
