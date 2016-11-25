
import sys
import os
sys.path.append(os.path.abspath("/Users/benjaminpujol/Desktop/Projet-avec-le-mexicain"))
import features_preprocessing as fp
import submission_preprocessing as sp
from configuration import CONFIG
import linex as ln
import numpy as np
from sklearn import cross_validation
from sklearn.cross_validation import cross_val_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import AdaBoostRegressor
import pandas as pd
from sklearn import linear_model

total_error = 0
preprocessing = fp.feature_preprocessing('train_2011_2012_2013.csv', ';')
submission = pd.read_csv('submission.txt', sep = '\t')
submission['ASS_ID'] = submission['ASS_ASSIGNMENT'].apply(lambda x: int(CONFIG.ass_assign[x]))
#print(submission)
print('Ready for training...')
for id in [22]:
    preprocessing_id = fp.feature_preprocessing()
    preprocessing_id.data = preprocessing.data.copy()
    preprocessing_id.full_preprocess(id)  #Choose the columns you want to use, always keep at least ASS_ID, TIME, WEEK_DAY AND CSPL_RECEIVED_CALLS
    data = preprocessing_id.data.reset_index()
    print('Loading ended')
    print(data.head(n=20))
#
#    Y = data['CSPL_RECEIVED_CALLS']
#    X = data.drop(['CSPL_RECEIVED_CALLS'], axis=1)
##    print(X,Y)
#
#
#    #Implement cross validation (10 splits)
#    cv_score = 0
#    #for size in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
#    X_train, X_cv, Y_train, Y_cv = cross_validation.train_test_split(X, Y, test_size = 0.02, random_state=0)
#    print('Cross validation OK')
#    #RandomForest
#
#    clf = RandomForestRegressor(n_estimators=50, oob_score=True)
#    clf.fit(X_train,Y_train)
#    print('Model training done')
##    print(clf.predict(X_cv),Y_cv)
#    cv_score = clf.score(X_cv,Y_cv)
#    print(id , cv_score) # Print average scores
##////////////////////////////////////////////////
    print('Loading submission')
    submission_id = sp.submission_preprocessing()
    print('Preprocessing submission')
    #Preprocess submission.txt
    submission_id.full_preprocess(id) #Choose columns
    X_test = submission_id.data
    print(X_test.head(n=20))
#///////////////////////////////////////////
#    Y_pred = clf.predict(X_test)
#    
#    print(Y_pred)
#    
#    submission[submission['ASS_ID'] == id]['CSPL_RECEIVED_CALLS'] = Y_pred
#
#submission = submission.drop(['ASS_ID'], axis = 1)
#submission.to_csv('test.csv', sep = '/')          #Predict Y_pred from X_test
#




#AdaboostRegression

#clf2 = AdaBoostRegressor(n_estimators=100)
#clf2.fit(X_train,Y_train)
#predict_2 = clf2.predict(X_test)
#print(clf2.score(X_test,Y_test))

