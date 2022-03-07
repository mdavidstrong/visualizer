import datetime

import pandas as pd
import streamlit as st

from cs_stats import CSStats
from plotting import figure,pie_plot



# sorts a dictionary by its values
def sort_dict_by_value(d, reverse=False):
    return dict(sorted(d.items(), key = lambda x: x[1], reverse = reverse))

# streamlit page
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
        figure(stat_frame,frame)
        # adds statistics
        st.write(f"number of cases: {len(frame)}")
        st.write(f"average number of issues per component: {round(stat_frame.avg_num_issues(frame),1)}")
        st.markdown('Top 5 component issues: -- '+' -- '.join(list(reversed(stat_frame.comp_stats(frame,sort=True).keys()))[:5])+' --')

        # dropdowns for seeing more data about given frame
        with st.expander(f"case titles ( {time} )"):
            st.write(frame['Case Title'])
        with st.expander(f"case details ( {time} )"):
            st.write(frame[stat_frame.case_detail_columns])
        
    
    # places gap between col 1 and 3 to serve as a visual division
    with col2:
        st.title('')

    with col3:
        # user sets plots to true if they want to see detailed component data
        if plots == True:
            st.title(f"{comp.upper()}")
            pie_plot(stat_frame,comp,frame)
            # gets the number of issues for specified component in set time range
            stats = stat_frame.comp_stats(frame)[comp]
            st.write(f"number of {comp.upper()} issues: {stats}")
            # dropdowns for various stat breakdowns and frame details
            with st.expander(f"{comp} issue breakdown"):
                st.write(sort_dict_by_value(stat_frame.desc_stats(frame)[comp], reverse=True))
            with st.expander(f"{comp} issue descriptions and case titles"):
                st.write(frame.loc[stat_frame.frame['Primary Components'] == comp][['Case Title','Issue Description']])
            with st.expander(f"{comp} case details"):
                st.write(frame.loc[stat_frame.frame['Primary Components'] == comp][stat_frame.case_detail_columns])

# instantiates a CSStats
# object with gathered excel data
# to create an updated 'aggregate' file, use accompanying 'collect_data.py'   
# aggregate file needs to be in this directory
df = pd.read_excel('aggregate.xlsx',index_col=[0])
stat_frame = CSStats(df)

main()
