import pandas as pd
import datetime
import numpy as np

#class used to hold dataframes and return various data/subselections
class CSStats(object):
    # list of columns that doesn't include 'index' and 'created on'
    case_detail_columns = ['Serial Number','Case Number','Case Title','Primary Components','Issue Description','Customer','Dealer','Created By','cleaned_date']

    def __init__(self, frame):
        self.frame = frame

    # returns self.frame that is filtered to past 'x' weeks
    def past_week(self,weeks):
        num_days = 7*weeks
        now = datetime.datetime.now()
        newframe = self.frame.loc[(now - self.frame['Created On']) < datetime.timedelta(num_days)]
        return newframe
    
    # returns self.frame that is filtered to past 'x' months
    def past_month(self,months):
        num_days = 31*months
        now = datetime.datetime.now()
        newframe = self.frame.loc[(now - self.frame['Created On']) < datetime.timedelta(num_days)]
        return newframe
    
    # rturns self.frame that is filtered to selected single date
    def select_date(self,date):
        selected_date = str(date)[:10]
        newframe = self.frame.loc[self.frame['cleaned_date'] == selected_date]
        #newframe = self.frame
        #st.write(newframe)
        return newframe

    # returns all of the unique primary components
    def primary_comps(self,frame):
        primary_comps = []
        for i in frame['Primary Components']:
            if i not in primary_comps:
                primary_comps.append(i)
        return primary_comps

    # returns the unique issues for each component
    # dict (key=component) (value=list of unique issues)
    def descriptors(self,frame):
        descriptors = {}

        for i in range(len(self.frame)):
            component = frame['Primary Components'].iloc[i]
            issue = frame['Issue Description'].iloc[i]
            if component in descriptors:
                if issue in descriptors[component]:
                    pass
                else:
                    descriptors[component].append(issue)
            else:
                descriptors[component] = [issue]
        return descriptors

    # returns number of cases each component has
    # dict (key=component) (value=int representing number of cases)
    def comp_stats(self,frame,sort=False):
        comp_stats = {}
        for i in frame['Primary Components']:
            if i in comp_stats:
                comp_stats[i] += 1
            else:
                comp_stats[i] = 1
        if sort:
            sortedlist = sorted(comp_stats.items(), key=lambda x:x[1])
            return dict(sortedlist)
        else:
            return comp_stats
    
    # returns avg number of issues per component in given frame
    def avg_num_issues(self,frame):
        return np.average(list(self.comp_stats(frame).values()))

    # returns a sorted list of components
    def components(self,frame):
        return list(self.comp_stats(frame,sort=True).keys())
    # returns a list of number of cases that matches the above components
    def values(self,frame):
        return list(self.comp_stats(frame,sort=True).values())

    # returns a dictionary holding the issue count for each component
    # dict (key=component) (value=dict [key=issue] [value=int tally/count for issue])
    def desc_stats(self,frame):
        desc_stats = {}
        for i in range(len(frame)):
            component = frame['Primary Components'].iloc[i]
            issue = frame['Issue Description'].iloc[i]
            if pd.isnull(issue):
                issue = 'N/A'
            if component in desc_stats:
                if issue in desc_stats[component]:
                    desc_stats[component][issue] += 1
                else:
                    desc_stats[component][issue] = 1
            else:
                desc_stats[component] = {issue:1}
        return desc_stats