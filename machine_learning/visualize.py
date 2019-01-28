import pandas as pd
import numpy as np
import os

from data_preprocessing import preprocess_data, preprocess_data_4_catboost
from constants import SCHOOLS_REVERSED, TARGET_LABELS

import plotly.offline as py
import plotly.graph_objs as go
from plotly import tools


IN_FILE_NAME = 'pq_data_4_24_18_processed.csv'
IN_FILE_NAME2 = 'pq_data_10_20_17_processed.csv'
IN_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'machine_learning', 'data_out', IN_FILE_NAME)
IN_FILE_PATH2 = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'machine_learning', 'data_out', IN_FILE_NAME2)

input_data_df = pd.read_csv(IN_FILE_PATH)
other_data_df = pd.read_csv(IN_FILE_PATH2)

combined_df = input_data_df.append(other_data_df)

combined_df = combined_df[combined_df['GPA'] <= 4.0]


combined_df.reset_index(inplace=True)

#bardata = [combined_df.GPA.values]

gpa_data = [go.Histogram(x=combined_df.GPA.values, nbinsx=13)]
gpa_layout = go.Layout(title='Training Data GPA Distribution',
                       xaxis=dict(
                           title='GPA')
                       )

gpa_fig = go.Figure(data=gpa_data, layout=gpa_layout)
# py.plot(gpa_fig)

gmat_data = [go.Histogram(x=combined_df.GMAT.values)]
gmat_layout = go.Layout(title='Training Data GMAT Score Distribution',
                        xaxis=dict(
                            title='GMAT Scores')
                        )
gmat_fig = go.Figure(data=gmat_data, layout=gmat_layout)
# py.plot(gmat_fig)


minority_df = combined_df[combined_df['STEM_MAJOR'] == 1]
majority_df = combined_df[combined_df['STEM_MAJOR'] == 0]


segment_1 = go.Histogram(
    x=minority_df.GMAT.values,
    opacity=0.75
)
segment_2 = go.Histogram(
    x=majority_df.GMAT.values,
    opacity=0.75
)

comp_data = [segment_1, segment_2]
comparison_layout = go.Layout(title='Compared GMAT Distribution',
                              barmode='overlay')
comp_fig = go.Figure(data=comp_data, layout=comparison_layout)
py.plot(comp_fig)
