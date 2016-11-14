import pandas as pd
import time
from configuration import CONFIG

def date_reducer(date):
    parsedTime =  time.strptime(date, "%Y-%m-%d %H:%M:%S.000")
    year = int(parsedTime.tm_year)
    month = int(parsedTime.tm_mon)
    day = int(parsedTime.tm_mday)
    hour = int(parsedTime.tm_hour*60 + parsedTime.tm_min)
    year_day = int(parsedTime.tm_yday)

    return hour, year_day, day, month, year

class feature_preprocessing():

    def __init__(self):
        self.data = pd.read_csv('../preprocessed_data.csv', sep=";")


    def preprocess_date(self):
        self.data["DATE"] = self.data ["DATE"].apply(date_reducer)
        #self.data = self.data.groupby(['DATE','ASS_ID','DAY_OFF','WEEK_DAY']).sum()
        #self.data = self.data.reset_index()


    def date_vector(self):
        self.data['YEAR'] = self.data['DATE'].apply(lambda x: x[4])
        self.data['MONTH'] = self.data['DATE'].apply(lambda x: x[3])

        for key, month in CONFIG.months.items():
            self.data[month] = self.data['MONTH'].apply(lambda x: int(x == key))
        self.data['TIME'] = self.data ["DATE"].apply(lambda x: x[0])
        self.data['YEAR_DAY']= self.data["DATE"].apply(lambda x: x[1])
    

    def full_preprocess(self, used_columns=CONFIG.default_columns, keep_all = False, remove_columns = []):
        self.preprocess_date()
        self.date_vector()
        self.data = self.data.drop(['DATE', 'DAY_OFF', 'YEAR'], axis=1)
        


        if not keep_all:
            print(used_columns)
            self.data = self.data[used_columns]
        else:
            self.data = self.data.drop(remove_columns, axis=1)


if __name__ == "__main__": #execute the code only if the file is executed directly and not imported
    pp = feature_preprocessing()
    pp.full_preprocess(keep_all=True)
    print(pp.data)



    #print(pp.data.sort_values(by=['CSPL_CALLS'], ascending=[0]))


