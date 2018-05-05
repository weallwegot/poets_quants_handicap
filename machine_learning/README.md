
Input Data: [Poets & Quants Webscrape](..\data_out\pq_data_4_24_18.csv)

Preprocessing Steps: [Checkout Methods Here](data_preprocessing.py)

Created one model for each school.


#### Notes & Issues

Tons of overfitting going on (check out Michigan, Cornell, and INSEAD). Right now, just testing Proof of Concept and Things.

Tiny number of samples for each school, currently experimenting with ways to reduce dimensionality of categorical features like majors. 

Data quality is a work in progress. The webscrape parsing piece leaves much to be desired.

Looking to try some more techniques apart from Linear Regression.


---------------------------------------------------------------------

## Results




Number of Samples for Duke: 22

______________________________________________
Classifier: LinearRegression for Duke

Mean Absolute Error: 3.58485224787

Mean Squared Error: 22.0921411102

R2 Coefficient of Determination: 0.795259046485

______________________________________________

Number of Samples for Columbia: 29

______________________________________________
Classifier: LinearRegression for Columbia

Mean Absolute Error: 3.46662790023

Mean Squared Error: 18.7949446535

R2 Coefficient of Determination: 0.790745676603

______________________________________________

Number of Samples for Stanford: 47

______________________________________________
Classifier: LinearRegression for Stanford

Mean Absolute Error: 4.60340588495

Mean Squared Error: 33.0629974013

R2 Coefficient of Determination: 0.462376435337

______________________________________________

Number of Samples for Cornell: 9

______________________________________________
Classifier: LinearRegression for Cornell

Mean Absolute Error: 7.83570739158e-14

Mean Squared Error: 1.19461589438e-26

R2 Coefficient of Determination: 1.0

______________________________________________

Number of Samples for Berkeley: 26

______________________________________________
Classifier: LinearRegression for Berkeley

Mean Absolute Error: 4.3932741025

Mean Squared Error: 36.3744266231

R2 Coefficient of Determination: 0.733180197792

______________________________________________

Number of Samples for Michigan: 10

______________________________________________
Classifier: LinearRegression for Michigan

Mean Absolute Error: 1.98951966013e-14

Mean Squared Error: 7.27014210252e-28

R2 Coefficient of Determination: 1.0

______________________________________________

Number of Samples for Tuck: 25

______________________________________________
Classifier: LinearRegression for Tuck

Mean Absolute Error: 4.57402835951

Mean Squared Error: 39.4828064477

R2 Coefficient of Determination: 0.605171935523

______________________________________________

Number of Samples for UCLA: 17

______________________________________________
Classifier: LinearRegression for UCLA

Mean Absolute Error: 2.0019628512

Mean Squared Error: 15.5555829657

R2 Coefficient of Determination: 0.886868487522

______________________________________________

Number of Samples for NYU: 8

______________________________________________
Classifier: LinearRegression for NYU

Mean Absolute Error: 2.62012633812e-14

Mean Squared Error: 1.06180677843e-27

R2 Coefficient of Determination: 1.0

______________________________________________

Number of Samples for Wharton: 40

______________________________________________
Classifier: LinearRegression for Wharton

Mean Absolute Error: 5.31598176412

Mean Squared Error: 50.9461001814

R2 Coefficient of Determination: 0.402145237385

______________________________________________

Number of Samples for Kellogg: 43

______________________________________________
Classifier: LinearRegression for Kellogg

Mean Absolute Error: 5.13166042293

Mean Squared Error: 40.8422677543

R2 Coefficient of Determination: 0.486276509675

______________________________________________

Number of Samples for Harvard: 49

______________________________________________
Classifier: LinearRegression for Harvard

Mean Absolute Error: 5.92251808645

Mean Squared Error: 59.1383837851

R2 Coefficient of Determination: 0.350563103457

______________________________________________

Number of Samples for Booth: 29

______________________________________________
Classifier: LinearRegression for Booth

Mean Absolute Error: 4.71861838448

Mean Squared Error: 34.9298834845

R2 Coefficient of Determination: 0.659999629509

______________________________________________

Number of Samples for Yale: 18

______________________________________________
Classifier: LinearRegression for Yale

Mean Absolute Error: 1.78430864078

Mean Squared Error: 9.84162846404

R2 Coefficient of Determination: 0.945117252627

______________________________________________

Number of Samples for Sloan: 21

______________________________________________
Classifier: LinearRegression for Sloan

Mean Absolute Error: 1.7679722085

Mean Squared Error: 8.05797198748

R2 Coefficient of Determination: 0.947393550755

______________________________________________

Number of Samples for INSEAD: 6

______________________________________________
Classifier: LinearRegression for INSEAD

Mean Absolute Error: 3.07901852163e-14

Mean Squared Error: 1.31266454629e-27

R2 Coefficient of Determination: 1.0

______________________________________________