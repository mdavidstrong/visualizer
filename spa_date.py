import datetime

class SpaDate(object):

    def __init__(self, cs_frame):
        self.cs_frame = cs_frame
    
    def add_spa_date_column(self):
        temp_frame = self.cs_frame
        temp_frame['spa_created_on'] = temp_frame.apply(lambda row: self.convert_serial_number(row),axis=1)
        return temp_frame

    def convert_serial_number(self, row):
        raw = str(row['Serial Number'])[:6]
        try:
            if raw.isnumeric():
                year = '20' + raw[-2:]
                month = raw[:2]
                if int(month) not in range(1,13):
                    return f'invalid format: {raw} *** month: {month}'
                day = raw[2:4]
                date_str = datetime.date(int(year),int(month),int(day))
                
                return date_str
        except:
            a = f"invalid format {raw}"
            print(a)
            return a
        