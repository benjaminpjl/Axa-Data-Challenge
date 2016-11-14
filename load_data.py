import sys
import os
sys.path.append(os.path.abspath("/Users/benjaminpujol/Desktop/Projet-avec-le-mexicain/Code/"))
import pandas as pd
import time
from configuration import CONFIG


def find_day(day):             #Transforme les jours de la semaine en int compris entre 0 et 1
    if (day == "Dimanche"):
        return 0
    if (day == "Lundi"):
        return 1
    if (day == "Mardi"):
        return 2
    if (day == "Mercredi"):
        return 3
    if (day == "Jeudi"):
        return 4
    if (day == "Vendredi"):
        return 5
    if (day == "Samedi"):
        return 6


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
        data = pd.read_csv('train_2011_2012_2013.csv', sep=";", usecols=CONFIG.useful_columns, nrows = 1000000)  #Choose nrows, number of rows
        week_day = data['DAY_WE_DS'].map(lambda day: find_day(day))  #Dimanche->0, Lundi->1, Mardi->2, etc...
        data['WEEK_DAY'] = week_day
        data['ASS_ID'] = data['ASS_ASSIGNMENT'].apply(lambda x: int(CONFIG.ass_assign[x])) #Create ASS_ID (int between 0 and 28) from ASS_ASSIGNMENT as defined in configuration.py
        data = data.drop(['ASS_ASSIGNMENT', 'DAY_WE_DS', 'WEEK_END'], axis=1) #Drop 3 columns
        self.data = data
        #self.data = data.groupby(['DATE', 'ASS_ID', 'DAY_OFF', 'WEEK_DAY'], sort=False).sum().reset_index()





if __name__ == "__main__":  #Execute uniquement si le fichier load_data est executé directement et pas importé
    loader = load_data()
    loader.data.to_csv('../preprocessed_data.csv', sep=";")
    loaded_data = loader.data
