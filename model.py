
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

total_error = 0
for id in range(29):
    preprocessing = fp.feature_preprocessing()
    preprocessing.full_preprocess(id)  #Choose the columns you want to use, always keep at least ASS_ID, TIME, WEEK_DAY AND CSPL_RECEIVED_CALLS
    data = preprocessing.data

    Y = data['CSPL_RECEIVED_CALLS']
    X = data.drop(['CSPL_RECEIVED_CALLS'], axis=1)


    #Implement cross validation (10 splits)
    cv_score = 0
    #for size in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
    X_train, X_cv, Y_train, Y_cv = cross_validation.train_test_split(X, Y, test_size = 0.4, random_state=0)

    #RandomForest

    clf = RandomForestRegressor(n_estimators=1000, oob_score=True)
    clf.fit(X_train,Y_train)
    cv_score = clf.score(X_cv,Y_cv)
    print(id , cv_score) # Print average scores

    submission = sp.submission_preprocessing()  #Preprocess submission.txt
    submission.full_preprocess(id, used_columns=['ASS_ID', 'TIME', 'WEEK_DAY', 'CSPL_RECEIVED_CALLS']) #Choose columns
    sub_data = submission.data
    Y_test = data['CSPL_RECEIVED_CALLS']
    X_test = data.drop(['CSPL_RECEIVED_CALLS'], axis=1)

    Y_pred = clf.predict(X_test)            #Predict Y_pred from X_test
    print(id, ln.evalerror_linex(Y_pred,Y_test))  #Print Linex error
    total_error += ln.evalerror_linex(Y_pred, Y_test)
    print(total_error)





#AdaboostRegression

#clf2 = AdaBoostRegressor(n_estimators=100)
#clf2.fit(X_train,Y_train)
#predict_2 = clf2.predict(X_test)
#print(clf2.score(X_test,Y_test))

