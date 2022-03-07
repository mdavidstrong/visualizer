import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import numpy as np
import datetime

#class used to hold dataframes and return various data/subselections
class cs_stats(object):
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


# makes the bar chart for components/issues data
def figure(frame):
    comps = stat_frame.components(frame)
    values = stat_frame.values(frame)
    fig = plt.figure(figsize = (10, 5))

    plt.bar(comps, values)
    plt.xlabel("Primary Component")
    plt.ylabel("Number of Cases")
    plt.xticks(rotation='vertical')
    
    st.pyplot(fig)


# creates two side by side plots
# not being used currently
def double_plot(comp):
    sub_fig = plt.figure(figsize = (10, 5))
    #Plot 1
    data = stat_frame.desc_stats(stat_frame.frame)[comp]
    labels = list(data.keys())
    values = list(data.values())

    plt.xlabel("component issues")
    plt.ylabel("number of issues")

    plt.subplot(1, 2, 1)
    plt.bar(labels, values)
    plt.xticks(rotation='vertical')

    #Plot 2
    x = np.array(values)
    mylabels = labels
    plt.subplot(1, 2, 2)
    plt.pie(x, labels = mylabels)

    st.pyplot(sub_fig)

# makes a pie chart for a given component and time selection
def pie_plot(comp,frame):
    fig = plt.figure(figsize = (10, 5))

    data = stat_frame.desc_stats(frame)[comp]
    pie_labels = list(data.keys())
    values = np.array(list(data.values()))

    plt.pie(values, labels = pie_labels)
    st.pyplot(fig)

# sorts a dictionary by its values
def sort_dict_by_value(d, reverse=False):
    return dict(sorted(d.items(), key = lambda x: x[1], reverse = reverse))


def main():
    st.set_page_config(layout='wide')
    
    date_type = st.sidebar.radio('Date selection', ['single date','date range'])
    
    if date_type == 'single date':
        date = st.sidebar.date_input("PICK A DATE",max_value=datetime.date.today())
        # checks for data on selected date
        date_exists = str(date) in stat_frame.frame['cleaned_date'].tolist()
        if date_exists:
            home(date_type,date,True,stat_frame.select_date(date))
        else:
            st.title('No data for that date')
    else:
        time = st.sidebar.selectbox(
            "TIME RANGE",
            [
                "all",
                "1 week",
                "2 weeks",
                "3 weeks",
                "1 month",
                "2 months",
                "3 months",
            ]
        )
        # makes the right component detail page based on the above selected time dropdown
        # time_str returns a gramatically correct time description for various *f'*
        if time == 'all':
            time_str = 'all available data'
            home(date_type,time_str,True,stat_frame.frame)
        elif time == '1 week':
            time_str = 'week'
            home(date_type,time_str,True,stat_frame.past_week(1))
        elif time == '2 weeks':
            time_str = '2 weeks'
            home(date_type,time_str,True,stat_frame.past_week(2))
        elif time == '3 weeks':
            time_str = '3 weeks'
            home(date_type,time_str,True,stat_frame.past_week(3))
        elif time == '1 month':
            time_str = 'month'
            home(date_type,time_str,True,stat_frame.past_month(1))
        elif time == '2 months':
            time_str = '2 months'
            home(date_type,time_str,True,stat_frame.past_month(2))
        elif time == '3 months':
            time_str = '3 months'
            home(date_type,time_str,True,stat_frame.past_month(3))


def home(date_type,time,plots,frame):
    # sets the three columns
    # 5,1,5 are the ratio of widths (visuals)
    col1, col2, col3 = st.columns([5,1,5])
    #creates list of radio buttons for each primary component in selected time frame of data
    comp = st.sidebar.radio('COMPONENTS',sorted(stat_frame.primary_comps(frame)))

    
    with col1:
        # column 1 title based on time input
        if date_type == 'date range':
            if time == 'all available data':
                st.title('All available case data')
            else:
                st.title(f'Case data from past {time}')
        else:
            st.title(f"{time} case data")
        
        # adds the bar chart of all data in selected time range
        figure(frame)
        # adds statistics
        st.write(f"number of cases: {len(frame)}")
        st.write(f"average number of issues per component: {round(stat_frame.avg_num_issues(frame),1)}")
        st.markdown('Top 5 component issues: -- '+' -- '.join(list(reversed(stat_frame.comp_stats(frame,sort=True).keys()))[:5])+' --')

        # dropdowns for seeing more data about given frame
        with st.expander(f"case titles ( {time} )"):
            st.write(frame['Case Title'])
        with st.expander(f"case details ( {time} )"):
            st.write(frame)
        
    
    # places gap between col 1 and 3 to serve as a visual division
    with col2:
        st.title('')

    with col3:
        # user sets plots to true if they want to see detailed component data
        if plots == True:
            st.title(f"{comp.upper()}")
            pie_plot(comp,frame)
            # gets the number of issues for specified component in set time range
            stats = stat_frame.comp_stats(frame)[comp]
            st.write(f"number of {comp.upper()} issues: {stats}")
            # dropdowns for various stat breakdowns and frame details
            with st.expander(f"{comp} issue breakdown"):
                st.write(sort_dict_by_value(stat_frame.desc_stats(frame)[comp], reverse=True))
            with st.expander(f"{comp} issue descriptions and case titles"):
                st.write(frame.loc[stat_frame.frame['Primary Components'] == comp][{'Case Title','Issue Description'}])
            with st.expander(f"{comp} case details"):
                st.write(frame.loc[stat_frame.frame['Primary Components'] == comp])

# instantiates a cs_stats object with gathered excel data
# to create an updated 'aggregate' file, use accompanying 'collect_data.py'   
# aggregate file needs to be in this directory
df = pd.read_excel('aggregate.xlsx',index_col=[0])
stat_frame = cs_stats(df)

main()
