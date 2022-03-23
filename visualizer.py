import datetime

import pandas as pd
import streamlit as st

from cs_stats import CSStats
from plotting import figure,pie_plot,line_chart
from estimated_time import EstimatedTimes



# sorts a dictionary by its values
def sort_dict_by_value(d, reverse=False):
    return dict(sorted(d.items(), key = lambda x: x[1], reverse = reverse))

# streamlit page
def main():
    st.set_page_config(layout='wide')
    

    st.sidebar.write(f"most recent data from: {stat_frame.most_recent_date()}")
    date_type = st.sidebar.radio('How would you like to choose the date?', ['date range','single date'])
    
    if date_type == 'single date':
        date = st.sidebar.date_input("Pick a day",max_value=datetime.date.today())
        # checks for data on selected date
        date_exists = str(date) in stat_frame.frame['cleaned_date'].tolist()
        if date_exists:
            home(date_type,date,True,stat_frame.select_date(date))
        else:
            st.title('No data for that date')
    else:
        time = st.sidebar.selectbox(
            "Date Range",
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

    
    with col1:
        # column 1 title based on time input
        if date_type == 'date range':
            if time == 'all available data':
                st.title('All available CS data')
                #line_chart(stat_frame,frame)
            else:
                st.title(f'CS case data from past {time}')
        else:
            st.title(f"{time} case data")
        
        # adds the bar chart of all data in selected time range
        figure(stat_frame,frame)
        # adds statistics
        st.write(f"number of CS cases: {len(frame)}")
        st.write(f"average number of issues per component: {round(stat_frame.avg_num_issues(frame),1)}")
        st.markdown('Top 5 components: -- '+' -- '.join(list(reversed(list(stat_frame.comp_stats(frame,sort=True).keys())))[:5])+' --')
        tot_time = stat_frame.total_time(frame)
        st.write(f"total repair time: {tot_time} hours")

        # dropdowns for seeing more data about given frame
        with st.expander(f"case titles ( {time} )"):
            st.write(frame['Case Title'])
        with st.expander(f"case details ( {time} )"):
            st.write(frame[stat_frame.case_detail_columns])
        with st.expander("Repair times"):
            st.write(frame[['Primary Components','Issue Description','est_fix_time']])
        
        st.write(frame['spa_created_on'])

        # constant data
        st.title('Estimated Repair Time Key')
        st.write(mytimes.time_frame)


        
    
    # places gap between col 1 and 3 to serve as a visual division
    with col2:
        st.title('')

    with col3:
        # user sets plots to true if they want to see detailed component data
        with st.expander('Component Selector'):
            selected_comp = st.selectbox('Select component',sorted(stat_frame.primary_comps(frame)))
        if plots == True:
            st.title(f"Details for: {selected_comp.upper()}")
            pie_plot(stat_frame,selected_comp,frame)
            # gets the number of issues for specified component in set time range
            stats = stat_frame.comp_stats(frame)[selected_comp]
            st.write(f"number of {selected_comp.upper()} issues: {stats}")
            # dropdowns for various stat breakdowns and frame details
            with st.expander(f"{selected_comp} issue breakdown"):
                st.write(sort_dict_by_value(stat_frame.desc_stats(frame)[selected_comp], reverse=True))
            with st.expander(f"{selected_comp} issue descriptions and case titles"):
                st.write(frame.loc[stat_frame.frame['Primary Components'] == selected_comp][['Case Title','Issue Description']])
            with st.expander(f"{selected_comp} case details"):
                st.write(frame.loc[stat_frame.frame['Primary Components'] == selected_comp][stat_frame.case_detail_columns])

# instantiates a CSStats
# object with gathered excel data
# to create an updated 'aggregate' file, use accompanying 'collect_data.py'   
# aggregate file needs to be in this directory
aggregate_file = 'aggregate.xlsx'
df = pd.read_excel(aggregate_file,index_col=[0])
stat_frame = CSStats(df)

estimated_fix_time_file = 'est_fix_time.xlsx'
mytimes = EstimatedTimes(estimated_fix_time_file)

main()
