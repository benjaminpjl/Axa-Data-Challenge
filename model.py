import sys
import os
sys.path.append(os.path.abspath("/Users/benjaminpujol/Desktop/Projet-avec-le-mexicain"))
import features_preprocessing as fp
import submission_preprocessing as sp
import linex as ln
import numpy as np
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
import pandas as pd
from sklearn import linear_model

preprocessing = fp.feature_preprocessing()
preprocessing.full_preprocess(used_columns=['ASS_ID', 'TIME', 'WEEK_DAY', 'CSPL_RECEIVED_CALLS'])
data = preprocessing.data
Y = data['CSPL_RECEIVED_CALLS']
X = data.drop(['CSPL_RECEIVED_CALLS'], axis=1)
print(np.unique(X['WEEK_DAY'].values))



Y = data['CSPL_RECEIVED_CALLS']
X= data.drop(['CSPL_RECEIVED_CALLS'], axis=1)
X_train, X_cv, Y_train, Y_cv = cross_validation.train_test_split(X, Y, test_size=0.4, random_state=0)

#RandomForest


clf = RandomForestRegressor(n_estimators=1000, oob_score=True)
clf.fit(X_train,Y_train)
print(clf.score(X_cv,Y_cv))


submission = sp.submission_preprocessing()
submission.full_preprocess(used_columns=['ASS_ID', 'TIME', 'WEEK_DAY', 'CSPL_RECEIVED_CALLS'])
sub_data = submission.data
Y_test = data['CSPL_RECEIVED_CALLS']
X_test = data.drop(['CSPL_RECEIVED_CALLS'], axis=1)

Y_pred = clf.predict(X_test)
print(ln.evalerror_linex(Y_pred,Y_test))








#AdaboostRegression

#clf2 = AdaBoostRegressor(n_estimators=100)
#clf2.fit(X_train,Y_train)
#predict_2 = clf2.predict(X_test)
#print(clf2.score(X_test,Y_test))
