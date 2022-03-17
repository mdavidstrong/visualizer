import pandas as pd
import datetime

class SpaDate(object):

    def __init__(self, cs_frame):
        self.cs_frame = cs_frame
    
    def add_spa_date_column(self):
        self.cs_frame['spa_created_on'] = self.cs_frame.apply(lambda row: self.convert_serial_number(row),axis=1)
        

    def convert_serial_number(self, row):
        raw = row['Serial Number'][:6]
        year = '20' + raw[-2:]
        month = raw[:2]
        day = raw[2:4]
        date_str = datetime.date(int(year),int(month),int(day))
        
        return date_str