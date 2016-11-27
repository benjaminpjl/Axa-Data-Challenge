import pandas as pd
from configuration import CONFIG
import numpy as np
import datetime as dt


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


def extract_date(string):
    d = dt.datetime.strptime(string, "%Y-%m-%d %H:%M:%S.000")
    return(d)

def extract_weekday(date):
    return(date.weekday())

def extract_hour(date):
    return(date.hour)

def extract_month(date):
    return(date.month)

def extract_year(date):
    return(date.year)

class feature_preprocessing():

    def __init__(self, filename = None, sepa = None, usecols = CONFIG.useful_columns):
        if filename == None and sepa == None:
            self.data = pd.DataFrame()
        else:
            self.data = pd.read_csv(filename, sep=sepa , usecols=usecols, nrows = 500000)
    

    def preprocess_date(self):
        self.data["DATE"] = self.data ["DATE"].apply(extract_date)
        #self.data = self.data.groupby(['DATE','ASS_ID','DAY_OFF','WEEK_DAY']).sum()
        #self.data = self.data.reset_index()

    def select_assid(self, assid):
        self.data=self.data.loc[self.data['ASS_ID'] == assid]
    
    

    def date_vector(self):
        self.data['YEAR'] = self.data['DATE'].apply(extract_year)
        for year in ['2011','2012','2013']:
            self.data[year] = self.data['YEAR'].apply(lambda x: (int(year) == x)*1)

        self.data['MONTH'] = self.data['DATE'].apply(extract_month)
        for key, month in CONFIG.months.items():
            self.data[month] = self.data['MONTH'].apply(lambda x: int(x == key))
        
        self.data['TIME']= self.data['DATE'].apply(extract_hour)
        #self.data['TIME'] = self.data['TIME'].apply(lambda x: x in range(450,1411)*(x[0]-450)/30 + x in range(0,451)*(x/30+1) + x in range(1411,1441)*0)
        self.data['YEAR_DAY']= self.data["DATE"].apply(extract_weekday)
        

    def ass_id_creation(self): # Create ASS_ID (int between 0 and 28) from ASS_ASSIGNMENT as defined in configuration.py
        self.data['ASS_ID'] = self.data['ASS_ASSIGNMENT'].apply(lambda x: int(CONFIG.ass_assign[x]))
    
    def ass_assignement_to_vector(self): # Create 28 features for each ASS_ASSIGNMENT with values 0 or 1
        its = self.data['ASS_ASSIGNMENT'].unique()
        for it in its:
            self.data[it]= self.data['ASS_ASSIGNMENT'].apply(lambda x: int(x==it))

    def hourlymean_past(date, y):
    
        nday_before = 7
        ysel = y.loc[(y.index > date - dt.timedelta(nday_before))]
        ysel = ysel.loc[(ysel.index < date)]
        h = extract_hour(date)
        if (len(ysel.loc[ysel.loc[:,'HOUR'] == h]) < 0):
            return(0)
        else:
            return(ysel.loc[ysel.loc[:,'HOUR'] == h].loc[:,"CSPL_RECEIVED_CALLS"].mean())


    def lastvalue(date, y):
        nday_before = 7
        try:
            v = y.loc[date - dt.timedelta(nday_before)]["CSPL_RECEIVED_CALLS"]
            try:
                w = y.loc[date - 2*dt.timedelta(nday_before)]["CSPL_RECEIVED_CALLS"]
            except:
                w = v
        except KeyError:
            v = y.loc[date]["CSPL_RECEIVED_CALLS"] + np.random.normal(scale = 3)
            w = v
        return((3*v + w)/4)


    def jour_nuit_creation(self):  #Création de la feature jour nuit

        tper_team = self.data['TPER_TEAM'].values.tolist()
        jour = []
        nuit = []
        self.data.set_index('DATE')
        nrows = len(self.data.index)

        for i in range(nrows):
            if(tper_team[i] == "Jours"):
                jour.append(1)
                nuit.append(0)
            else:
                nuit.append(1)
                jour.append(0)
    
        self.data['JOUR'] = jour
        self.data['NUIT'] = nuit

    def week_day_to_vector(self):  #Création des Features SUNDAY, MONDAY, TUESDAY, etc qui prennent les valeurs 0 ou 1
        week_day = self.data['DAY_WE_DS'].map(lambda day: find_day(day))
        self.data['WEEK_DAY'] = week_day
        for key,day in CONFIG.days.items():
            self.data[day] = self.data['WEEK_DAY'].apply(lambda x: int(x == key))
    

    def full_preprocess(self, assid, keep_all_ass_id = False, used_columns=CONFIG.default_columns, keep_all = False, remove_columns = []):
        self.ass_id_creation()
        if keep_all_ass_id!=True:
            self.select_assid(assid)
        self.preprocess_date()
        self.date_vector()
        self.hourlymean_past(self.data['DATE'],self.data)
        self.jour_nuit_creation()
        self.week_day_to_vector()
        #self.ass_assignement_to_vector()
        print(self.data.head(100))
        self.data = self.data[CONFIG.default_columns]
        
 
        


        if not keep_all:
            print(used_columns)
            self.data = self.data[used_columns]
        else:
            self.data = self.data.drop(remove_columns, axis=1)


if __name__ == "__main__": #execute the code only if the file is executed directly and not imported
    pp = feature_preprocessing()
    pp.full_preprocess(6, keep_all = False)
    print(pp.data)
    pp.data.to_csv('../preprocessed_data.csv', sep=";")





    #print(pp.data.sort_values(by=['CSPL_CALLS'], ascending=[0]))


