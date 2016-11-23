import datetime
import time

import pandas as pd

from configuration import CONFIG


def date_reducer(date):                                         #From string date format get hour, year_day, day, month, year
    parsedTime = time.strptime(date, "%Y-%m-%d %H:%M:%S.000")
    year = int(parsedTime.tm_year)
    month = int(parsedTime.tm_mon)
    day = int(parsedTime.tm_mday)
    hour = int(parsedTime.tm_hour * 60 + parsedTime.tm_min)
    year_day = int(parsedTime.tm_yday)

    return hour, year_day, day, month, year


def get_week_day(date):                                                             # From the day, month, year gives the day of the week in int Dimanche -> 0, Lundi -> 1, etc...
    return (datetime.datetime(date[4], date[3], date[2]).weekday() + 1) % 7


class submission_preprocessing():
                                                                    #Initialisation: read submission.txt

    def __init__(self):
        self.data = pd.read_csv("submission.txt", sep="\t")


    def preprocess_date(self):                                           #Apply date reducer and create WEEK_DAY
        self.data["DATE"] = self.data["DATE"].apply(date_reducer)
        self.data["WEEK_DAY"] = self.data["DATE"].apply(get_week_day)

    def select_assid(self, assid):                                          #Select the Ass_id
        self.data=self.data.loc[self.data['ASS_ID'] == assid]


    def date_vector(self):                                                      #Create YEAR, MONTH and YEAR_DAY
        self.data['YEAR'] = self.data['DATE'].apply(lambda x: x[4])
        self.data['MONTH'] = self.data['DATE'].apply(lambda x: x[3])

        for key, month in CONFIG.months.items():
            self.data[month] = self.data['MONTH'].apply(lambda x: int(x == key))
        self.data['TIME'] = self.data["DATE"].apply(lambda x: x[0])
        self.data['YEAR_DAY'] = self.data["DATE"].apply(lambda x: x[1])


    def transform_week_day_to_vector(self):  #Add columns SUNDAY, SATURDAY, FRIDAY, MONDAY....
        for key, day in CONFIG.days.items():
            self.data[day] = self.data['WEEK_DAY'].apply(lambda x: int(x == key))

    def ass_assignement_to_vector(self):  #Create one column for each ASS_ID and the column ASS_ID
        assignments = CONFIG.ass_assign
        for ass in assignments:
            self.data[ass] = self.data['ASS_ASSIGNMENT'].apply(lambda x: int(x == ass))
        self.data['ASS_ID'] = self.data['ASS_ASSIGNMENT'].apply(lambda x: int(CONFIG.ass_assign[x]))


    #def add_day_off(self):
        #self.data['YEAR_DAY_AND_YEAR'] = self.data['DATE'].apply(lambda date: get_year_day(date))
        #self.data['DAY_DS'] = self.data['YEAR_DAY_AND_YEAR'].apply(lambda date: find_day_off(date[0], date[1]))
        #self.data['DAY_OFF'] = self.data['DAY_DS'].apply(lambda label: int(label != "nan"))


    #def ass_assignement_to_vector(self):
        #ids = self.data['ASS_ID'].unique()
        #for id in ids:
         #   self.data[id] = self.data['ASS_ID'].apply(lambda x: int(x == id))

    def full_preprocess(self,assid, used_columns=CONFIG.default_columns, keep_all=False, remove_columns=[]): #Apply all the preprocess
        self.ass_assignement_to_vector()
        self.select_assid(assid)
        self.preprocess_date()
        self.date_vector()
        self.transform_week_day_to_vector()
        self.data = self.data.rename(columns={'prediction': 'CSPL_RECEIVED_CALLS'})      #Rename 'prediction' -> 'CSPL_RECEIVED_CALLS'


        if not keep_all:
            self.data = self.data[used_columns]
        else:
            self.data = self.data.drop(remove_columns, axis=1)


if __name__ == "__main__":  #execute the code only if the file is executed directly and not imported
    pp = submission_preprocessing()
    pp.full_preprocess(5, used_columns=CONFIG.default_columns[:], keep_all=True)
    submission_data = pp.data
    print(submission_data)
