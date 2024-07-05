# setting the cross validation parameters
from sklearn.model_selection import KFold
tune_control = KFold(n_split = 5, 
                     shuffle= True, 
                     random_state= 1502).split(X = X_train, 
                                               y = y_train)