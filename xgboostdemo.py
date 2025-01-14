#importing libraries
import pandas as pd
import xgboost as xgb
import numpy as np
import os

# import dataset
file_path = '/Users/juliettewilliamson/Desktop/XGBoost/XGBoost for Business in Python and R/bank-full.csv'
dataset = pd.read_csv(file_path, sep = ";")
dataset.select_dtypes(include=[float, int])

print(dataset.head())

# isolate x and y variables
y = dataset.iloc[:, -1].values
X = dataset._get_numeric_data()

# split dataset into training and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size =0.2, 
                                                    random_state=1502)

#transform y factor variables
y_train = np.where(y_train == "yes", 1, 0)
y_test = np.where(y_test == "yes", 1, 0)
print(np.mean(y_train))
print(np.mean(y_test))

# create xgboost matrices
Train = xgb.DMatrix(X_train, label = y_train) 
Test = xgb.DMatrix(X_test, label = y_test)

# setting our XGBoost parameters
parameters1 = {'learning_rate' : 0.3, 
               'max_depth': 2, 
               'colsample_bytree': 1,
               'subsample': 1,
               'min_child_weight': 1,
               'gamma' : 0,
               'random_state': 1502,
               'eval_metric': "auc",
               'Objective': "binary:logistic",
               }

# run XGBoost
model1 = xgb.train(params = parameters1, 
                   dtrain = Train, 
                   num_boost_round = 200,
                   evals = [(Test, "Yes")],
                   verbose_eval = 50)

# Predictions
predictions1 = model1.predict(Test)
predictions1 = np.where(predictions1 > 0.5, 1, 0)

# Confusion Matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
confusion_matrix1 = confusion_matrix(y_test, predictions1)
print(confusion_matrix1)
report1 = classification_report(y_test, predictions1)
print(report1)

##################################################################

#isolate the categorical variables
dataset_categorical = dataset.select_dtypes(exclude = "number")

# transform categorical vars into dummy vars
dataset_categorical = pd.get_dummies(data = dataset_categorical,
                                     drop_first= True)

# forming the last dataset by joining numerical and categorical datasets
final_dataset = pd.concat([X, dataset_categorical],  axis = 1)

# getting names of columns - data preparation
feature_columns = list(final_dataset.columns.values)
feature_columns = feature_columns[:-1]

###################################################################

# isolate x and y variables part 2
y = final_dataset.iloc[:, -1].values
X = final_dataset.iloc[:, :-1].values

# split dataset into training and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y,
                                                    test_size =0.2, 
                                                    random_state=1502)

# create xgboost matrices part 2
Train = xgb.DMatrix(X_train, label = y_train, feature_names = feature_columns)
Test = xgb.DMatrix(X_test, label = y_test, feature_names = feature_columns)

# setting our XGBoost parameters part 2
parameters2 = {'learning_rate' : 0.3, 
               'max_depth': 2, 
               'colsample_bytree': 1,
               'subsample': 1,
               'min_child_weight': 1,
               'gamma' : 0,
               'random_state': 1502,
               'eval_metric': "auc",
               'Objective': "binary:logistic",
               }

# run XGBoost
model2 = xgb.train(params = parameters2, 
                   dtrain = Train, 
                   num_boost_round = 200,
                   evals = [(Test, "Yes")],
                   verbose_eval = 50)

# Predictions part 2
predictions2 = model2.predict(Test)
predictions2 = np.where(predictions1 > 0.5, 1, 0)

# Confusion Matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
confusion_matrix2 = confusion_matrix(y_test, predictions1)
print(confusion_matrix2)
report2 = classification_report(y_test, predictions2)
print(report2)


###########################################################################

# checking how many cores we have
import multiprocessing
multiprocessing.cpu_count()

# setting the cross validation parameters
from sklearn.model_selection import KFold
tune_control = KFold(n_splits = 5, 
                     shuffle= True, 
                     random_state= 1502).split(X = X_train, 
                                               y = y_train)

# set parameter tuning
tune_grid = {'learning_rate' : [0.05, 0.3], 
             'max_depth': range(2, 9, 2), 
             'colsample_bytree': [0.5, 1],
             'subsample': [1],
             'min_child_weight': [1],
             'gamma' : [0],
             'random_state': [1502],
             'n_estimators': range(200, 2000, 200),
             'booster': ["gbtree"],
            }

# low learning rate pairs well with high number of n-estimators
# high learning rate pairs well with low number of n-estimators
# booster for tree-like algorithms

# State that we are doing a classification problem
from xgboost import XGBClassifier
classifier = XGBClassifier(objective = "binary:logistic")

# Cross Validation Assembly
from sklearn.model_selection import GridSearchCV
grid_search = GridSearchCV(estimator= classifier, 
                           param_grid= tune_grid,
                           scoring= "roc_auc",
                           n_jobs = 6, 
                           cv = tune_control, 
                           verbose=5)

# Setting evaluation parameters
evaluation_parameters = {"early_stopping_rounds": 100,
                         "eval_metric": "auc",
                         "eval_set": [(X_test, y_test)]}

# hyperparameter tuning and cross validation
tune_model = grid_search.fit(X = X_train, 
                             y = y_train)

# figure out what the best model parameters are
grid_search.best_params_, grid_search.best_score_

#############################################################################

# setting the cross validation parameters
from sklearn.model_selection import KFold
tune_control = KFold(n_splits = 5, 
                     shuffle= True, 
                     random_state= 1502).split(X = X_train, 
                                               y = y_train)

# set parameter tuning part 2
tune_grid2 = {'learning_rate' : [0.05], 
             'max_depth': [6],
             'colsample_bytree': [0.5],
             'subsample': [0.9, 1],
             'min_child_weight': range(1, 5, 1),
             'gamma' : [0, 0.1],
             'random_state': [1502],
             'n_estimators': range(200, 2000, 200),
             'booster': ["gbtree"],
            }

# low learning rate pairs well with high number of n-estimators
# high learning rate pairs well with low number of n-estimators
# booster for tree-like algorithms


# Cross Validation Assembly
from sklearn.model_selection import GridSearchCV
grid_search2 = GridSearchCV(estimator= classifier, 
                           param_grid= tune_grid2,
                           scoring= "roc_auc",
                           n_jobs = 6, 
                           cv = tune_control, 
                           verbose=5)

# hyperparameter tuning and cross validation
tune_model2 = grid_search2.fit(x = X_train, 
                             y = y_train)

# figure out what the best model parameters are
grid_search2.best_params_, grid_search2.best_score_

############################################################

# setting our XGBoost parameters part 3
parameters3 = {'learning_rate' : 0.05, 
               'max_depth': 6, 
               'colsample_bytree': 0.5,
               'subsample': 1,
               'min_child_weight': 2,
               'gamma' : 0,
               'random_state': 1502,
               'eval_metric': "auc",
               'Objective': "binary:logistic",
               }

# run XGBoost part 3
model3 = xgb.train(params = parameters3, 
                   dtrain = Train, 
                   num_boost_round = 800,
                   evals = [(Test, "Yes")],
                   verbose_eval = 50)

# maximizing AOC does not mean maximizing revenue - there is a trade-off
# expected value (EV) == gaining a customer