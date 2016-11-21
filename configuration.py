class _Config:
    def __init__(self):
        # All samples
        self.useful_columns = ['DATE', 'DAY_OFF', 'DAY_WE_DS', 'WEEK_END', 'ASS_ASSIGNMENT', 'TPER_TEAM', 'CSPL_CALLS', 'CSPL_RECEIVED_CALLS']
        self.months = { 1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sept', 10: 'Oct', 11: 'Nov', 12: 'Dec'}
        self.days = {1: "MONDAY", 2: "TUESDAY", 3: "WEDNESDAY", 4: "THURSDAY", 5: 'FRIDAY', 6: "SATURDAY", 0: "SUNDAY"}
        self.ass_assign = {'Téléphonie':0, 'RTC':1, 'Gestion Renault':2, 'Nuit':3,'Gestion - Accueil Telephonique':4, 'Regulation Medicale':5, 'Services':6,'Tech. Total':7, 'Gestion Relation Clienteles':8, 'Crises':9, 'Japon':10, 'Médical':11, 'Gestion Assurances':12, 'Domicile':13, 'Gestion':14, 'SAP':15, 'RENAULT':16, 'Gestion Amex':18, 'Tech. Inter':19, 'Gestion Clients':20, 'Manager':21, 'Tech. Axa':22, 'CAT':23, 'Gestion DZ':24, 'Mécanicien':25, 'CMS':26, 'Prestataires':27, 'Evenements':28}

        self.default_columns = list(self.days.values())+ ['TIME', 'JOUR','NUIT','DAY_OFF','ASS_ID']+ ['CSPL_RECEIVED_CALLS']
CONFIG = _Config()

print (CONFIG.default_columns)

