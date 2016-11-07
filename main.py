
from numpy import *
from matplotlib.pyplot import *
import pandas as pd
import pylab as P
matplotlib.pyplot.style.use('ggplot');

#Uploading the data
df = pd.read_csv('train_2011_2012_2013.csv',sep=';', header=0, nrows=100000)
print("Size of the data: ", df.shape)

# See data (five rows) using pandas toolss
print(df.head())

#Cleaning the data

#Converting string to int
df['Jours'] = df['TPER_TEAM'].map( {'Jours': 1, 'Nuit': 0} ).astype(int)
df['Nuits'] = df['TPER_TEAM'].map( {'Jours': 0, 'Nuit': 1} ).astype(int)


#Drop useless features
df = df.drop(['DATE','DAY_DS','DAY_WE_DS','TPER_TEAM','ACD_LIB','ASS_SOC_MERE','ASS_DIRECTORSHIP','ASS_ASSIGNMENT','ASS_PARTNER','ASS_POLE','ASS_BEGIN','ASS_END','ASS_COMENT'], axis=1)



#Replacing null values with the mean value of the features: no null values
print('NULL TEST',df[df.isnull().any(axis=1)])


#Creating X and y and convert to numpy array with 'values'

X = df.drop(['CSPL_RECEIVED_CALLS'],axis=1).values
y = df['CSPL_RECEIVED_CALLS'].values
print('X',X)
print('y',y)

#Creating training and cross validation sets
from sklearn.cross_validation import train_test_split

X_train, X_cv, y_train, y_cv = train_test_split(
    X, y, test_size=0.2, random_state=None)

print('X_train shape', X_train.shape)
print('X_cv shape', X_cv.shape)
print('y_train shape', y_train.shape)
print('y_cv shape', y_cv.shape)


#import the random forest package
from sklearn.ensemble import RandomForestRegressor

# Create the random forest object which will include all the parameters
# for the fit
forest = RandomForestRegressor(n_estimators = 100)

# Fit X_train to y_train and create the decision trees
forest = forest.fit(X_train,y_train)

# Take the same decision trees and run it on the test data
output = forest.predict(X_cv)
print('output',output)
print('y_cv',y_cv)
print('score',forest.score(X_cv,y_cv))