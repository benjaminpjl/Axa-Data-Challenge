import pandas as pd
import numpy as np
import datetime as dt


def extract_date(string):
    d = dt.datetime.strptime(string, "%Y-%m-%d %H:%M:%S.000")
    return (d)


def extract_weekday(date):
    return (date.weekday())


def extract_hour(date):
    return (date.hour)


def extract_month(date):
    return (date.month)


def load_data(path):
    ## Loading the data

    nrows = 200000

    data = pd.read_csv(path,
                       sep=";",
                       nrows=nrows)
    # data = data.set_index('DATE')

    data.info()

    ## Creating features jour et nuit

    data['JOUR'] = data['TPER_TEAM'].map({'Jours': 1, 'Nuit': 0}).astype(int)
    data['NUIT'] = data['TPER_TEAM'].map({'Jours': 0, 'Nuit': 1}).astype(int)

    ## Selecting Data

    col_used = ['DATE', 'DAY_OFF', 'WEEK_END', 'SPLIT_COD',
                'ASS_ASSIGNMENT', 'JOUR', 'NUIT', 'CSPL_RECEIVED_CALLS']

    preproc_data = data[col_used]

    ## Creation of Date features


    dates = preproc_data['DATE'].apply(extract_date, 1)

    print('dates',dates)

    preproc_data.loc[:, "WEEKDAY"] = dates.apply(extract_weekday, 1)
    preproc_data.loc[:, "HOUR"] = dates.apply(extract_hour, 1)
    preproc_data.loc[:, "MONTH"] = dates.apply(extract_month, 1)

    # print(used_data.describe())

    print('preproc_data', preproc_data)

    ## Selecting one ASS_ASSIGNEMENT (One model for each)
    

    used_data = preproc_data.loc[preproc_data.loc[:, "ASS_ASSIGNMENT"] == "Téléphonie", :]
    used_data.drop(["SPLIT_COD", "ASS_ASSIGNMENT"], 1, inplace=True)
    print('used_data', used_data)

    rcvcall_data = used_data.groupby(["DATE"])['CSPL_RECEIVED_CALLS'].sum()
    features_data = used_data.groupby(["DATE"]).mean()
    features_data.drop("CSPL_RECEIVED_CALLS", 1, inplace=True)
    used_data = used_data.set_index('DATE')



    return preproc_data,features_data, rcvcall_data

load_data('train_2011_2012_2013.csv')
