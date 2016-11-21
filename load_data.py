import sys
import os
sys.path.append(os.path.abspath("/Users/benjaminpujol/Desktop/Projet-avec-le-mexicain"))
import pandas as pd
import time
from configuration import CONFIG



def get_year_day(date):                                             #Retourne le jour de l'année
    parsedTime = time.strptime(date, "%Y-%m-%d %H:%M:%S.000")
    return parsedTime.tm_yday, parsedTime.tm_year



def normalize(df, column):
    moyenne = df[column].mean()
    var = (((df[column] - moyenne) ** 2).mean()) ** 0.5
    df[column] = df[column].apply(lambda pre: (pre - moyenne) / (var))

#Loading data
class load_data:
    def __init__(self):
        data = pd.read_csv('train_2011_2012_2013.csv', sep=";", usecols=CONFIG.useful_columns, nrows = 300000)
        
        week_day = data['DAY_WE_DS'].map(lambda day: find_day(day))  #Dimanche->0, Lundi->1, Mardi->2, etc...
        data['WEEK_DAY'] = week_day
        
        data = data.drop(['DAY_WE_DS', 'WEEK_END'], axis=1) #Drop 3 columns
        self.data = data
        print(self.data)
        #self.data = data.groupby(['DATE', 'ASS_ID', 'DAY_OFF', 'WEEK_DAY'], sort=False).sum().reset_index()





if __name__ == "__main__":  #Execute uniquement si le fichier load_data est executé directement et pas importé
    loader = load_data()
    loader.data.to_csv('../preprocessed_data.csv', sep=";")
    loaded_data = loader.data
