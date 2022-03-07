import pandas as pd


class EstimatedTimes(object):

    def __init__(self,excel_time_file):
        self.excel_time_file = excel_time_file
        self.time_frame = pd.read_excel(self.excel_time_file,index_col=[0])

    # map an estimated fix time to each issue of a component
    def time_map(self):
        time_dict = {}
        for i in range(len(self.time_frame)):
            primary = self.time_frame['primary'].iloc[i]
            issue = self.time_frame['issue'].iloc[i]
            time = self.time_frame['total time'].iloc[i]
            if primary in time_dict.keys():
                if issue in time_dict[primary].keys():
                    pass
                else:
                    time_dict[primary][issue] = time
            else:
                time_dict[self.time_frame['primary'].iloc[i]] = {}
        return time_dict

file = 'est_fix_time.xlsx'

my_est_times = EstimatedTimes(file)

print(my_est_times.time_map())