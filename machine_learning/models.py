import pdb
import pandas as pd
import numpy as np


from sklearn.linear_model import LinearRegression, SGDRegressor, ElasticNet, Lasso, Ridge, RidgeCV
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.svm import LinearSVR
from sklearn.model_selection import ShuffleSplit, cross_val_score


from sklearn import metrics
#from sklearn.model_selection import cross_validate
#from sklearn.grid_search import GridSearchCV

from catboost import CatBoostRegressor, Pool, FeaturesData
from constants import RANDOM_STATE


def fit_train_test_cv(X_train, Y_labels, column_names, model_obj=None):

    if not model_obj:
        model_obj = GradientBoostingRegressor()

    # model_obj.fit(X_train,Y_labels)
    #pred_labels = model_obj.predict(X_train)

    #cv_score = cross_val_score(model_obj, X_train, Y_labels, cv=5,scoring='neg_mean_squared_error')

    splitter = ShuffleSplit(test_size=0.05, n_splits=10)
    # this creates multiple splits (im using it wrong i know)
    rmses = []
    for trn, tst in splitter.split(X_train, Y_labels):
        train_idx = trn
        test_idx = tst

        # train_idx,test_idx = splitter.split(X_train,Y_labels)

        #gboost_model = GradientBoostingRegressor()
        model_obj.fit(X_train[train_idx], Y_labels[train_idx])

        pred_labels = model_obj.predict(X_train[test_idx])

        real_labels = Y_labels[test_idx]

        #z = np.sqrt( np.sum((real_labels-pred_labels)**2.)/(len(real_labels))  )

        #print("Number of Test Samples: {}".format(len(real_labels)))
        z = np.sqrt(np.sum((real_labels.flatten() - pred_labels)**2) / len(pred_labels))

        # pdb.set_trace()

        #print("RMSE: {}".format(z))
        rmses.append(z)

    print("Median RMSE: {}".format(np.median(rmses)))
    print("pred_labels: {}".format(pred_labels))
    print("real_labels: {}".format(real_labels.flatten()))
    print("Differences: {}".format((real_labels.flatten() - pred_labels)))

    #print("Model Report \n")
    #print("Accuracy: {}".format(metrics.accuracy_score(Y_labels, pred_labels)))
    # print("RMSE: {}".format(metrics.mean_squared_error(y_true=Y_labels,y_pred=pred_labels)))

    #print("CV Score : Mean {} | Std {}| Min {} | Max {}".format(np.mean(cv_score),np.std(cv_score),np.min(cv_score),np.max(cv_score)))

    print("{}".format(column_names))
    try:
        feat_imp = pd.Series(model_obj.feature_importances_, column_names).sort_values(ascending=False)
        print(feat_imp)
    except AttributeError as ae:
        pass
    #feat_imp.plot(kind='bar', title='Feature Importances')
    #plt.ylabel('Feature Importance Score')

    return model_obj


def catboost_pred(catboost_pool):
    """
    Train a Catboost model, gradient boosting decision tree
    specially implemented to preprocess categorical variables
    https://towardsdatascience.com/https-medium-com-talperetz24-mastering-the-new-generation-of-gradient-boosting-db04062a7ea2
    """
    catboost_model = CatBoostRegressor(
        iterations=1300,
        depth=12,
        learning_rate=0.5,
        loss_function='RMSE',
        eval_metric='AUC',
        silent=True)

    # fit the model (the pool contains features & labels)
    catboost_model.fit(catboost_pool)
    # pred on same dataset as train

    Y_pred = catboost_model.predict(catboost_pool)
    return Y_pred


def gboosting_pred(X_train, Y_train):
    """
    Train a XG Boost model with default hyperparameters
    """
    gboost_model = GradientBoostingRegressor()
    gboost_model.fit(X_train, Y_train)
    Y_pred = gboost_model.predict(X_train)
    return Y_pred


def gboosting_train_test(X_full, Y_labels):
    """
    Traing a Gradient Boost model on a split version of 
    the full dataset and test it against a withheld subset
    of the data
    """
    splitter = ShuffleSplit(test_size=0.1)
    # this creates multiple splits (im using it wrong i know)
    for trn, tst in splitter.split(X_full, Y_labels):
        train_idx = trn
        test_idx = tst
        break
    # import pdb
    # pdb.set_trace()
    # train_idx,test_idx = splitter.split(X_full,Y_labels)

    gboost_model = GradientBoostingRegressor()
    gboost_model.fit(X_full[train_idx], Y_labels[train_idx])

    pred_labels = gboost_model.predict(X_full[test_idx])

    real_labels = Y_labels[test_idx]

    #display_metrics("Gboost Regression for {}".format(school),predicted_labels_gboost,labels)

    return real_labels, pred_labels


# input: X_train, Y_train
# output: Y_pred
def linear_regression_pred(X_train, Y_train):
    """
    Train a Linear Regression model with default hyperparameters
    """

    lr_model = LinearRegression()
    lr_model.fit(X_train, Y_train)
    Y_pred = lr_model.predict(X_train)
    return Y_pred


def linear_sgd_pred(X_train, Y_train):
    """
    Train a linear model with Stochastic Gradient Descent
    """

    sgd_model = SGDRegressor(random_state=RANDOM_STATE)
    sgd_model.fit(X_train, Y_train)
    Y_pred = sgd_model.predict(X_train)
    return Y_pred


def linear_svr_pred(X_train, Y_train):
    """
    Train a linear model with Support Vector Regression
    """

    svr_model = LinearSVR(random_state=RANDOM_STATE)
    svr_model.fit(X_train, Y_train)
    Y_pred = svr_model.predict(X_train)
    return Y_pred


def linear_elasticnet_pred(X_train, Y_train):
    """
    Train a linear model with Elastic Net
    """

    enet_model = ElasticNet(random_state=RANDOM_STATE)
    enet_model.fit(X_train, Y_train)
    Y_pred = enet_model.predict(X_train)
    return Y_pred


def linear_lasso_pred(X_train, Y_train):
    """
    Train a linear model with Lasso Regularization
    """

    lasso_model = Lasso(random_state=RANDOM_STATE)
    lasso_model.fit(X_train, Y_train)
    Y_pred = lasso_model.predict(X_train)
    return Y_pred


def linear_ridge_pred(X_train, Y_train):
    """
    Train a linear model with Ridge regularization
    """

    ridge_model = Ridge(random_state=RANDOM_STATE)
    ridge_model.fit(X_train, Y_train)
    Y_pred = ridge_model.predict(X_train)
    return Y_pred


def linear_ridge_cv_pred(X_train, Y_train):
    """
    Train a linear model with Ridge regularization but cross validations
    across different learning rates
    """

    ridge_model = RidgeCV(alphas=[0.1, 0.3, 0.5, 1.0, 10.0])
    ridge_model.fit(X_train, Y_train)
    Y_pred = ridge_model.predict(X_train)
    return Y_pred

# input: Y_pred,Y_true
# output: accuracy, auc, precision, recall, f1-score


def classification_metrics(Y_pred, Y_true):
    # NOTE: It is important to provide the output in the same order
    # mean_abs = mean_absolute_error(y_true=Y_true,y_pred=Y_pred)
    mean_squared = metrics.mean_squared_error(y_true=Y_true, y_pred=Y_pred)
    r2 = metrics.r2_score(y_true=Y_true, y_pred=Y_pred)
    exp_var = metrics.explained_variance_score(y_true=Y_true, y_pred=Y_pred)
    return mean_squared, exp_var, r2

# input: Name of classifier, predicted labels, actual labels


def display_metrics(classifierName, Y_pred, Y_true):
    print("______________________________________________")

    print("Classifier: {}\n".format(classifierName))
    mean_squared, exp_var_score, r2 = classification_metrics(Y_pred, Y_true)
    print("Mean Squared Error: {}\n".format(mean_squared))
    print("Explained Variance Score: {}\n".format(exp_var_score))
    print("R2 Coefficient of Determination: {}\n".format(r2))
    print("______________________________________________")
    print("")
