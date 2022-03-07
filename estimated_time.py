import pandas as pd
import numpy as np


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
        return self.assign_avg_to_na(time_dict)

    def assign_avg_to_na(self,time_map_orig):
        time_dict = time_map_orig
        for i in time_dict:
            time_total = 0
            issue_count = 0
            for j in time_dict[i]:
                if j == 'Not Available':
                    pass
                else:
                    time_total += time_dict[i][j]
                    issue_count += 1
            if issue_count == 0:
                pass
            else:
                time_avg = np.round(time_total/issue_count,1)
                time_dict[i]['Not Available'] = time_avg
        return time_dict