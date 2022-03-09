import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


# line chart for number of cases over time
def line_chart(csstats_object,frame):
    comps = csstats_object.num_cases_per_date().keys()
    values = csstats_object.num_cases_per_date().values()
    fig = plt.figure(figsize = (10,5))

    plt.plot(comps, values)
    plt.xticks(rotation='vertical')

    st.pyplot(fig)

# makes the bar chart for components/issues data
def figure(csstats_object,frame):
    comps = csstats_object.components(frame)
    values = csstats_object.values(frame)
    fig = plt.figure(figsize = (10, 5))

    plt.bar(comps, values)
    plt.xlabel("Primary Component")
    plt.ylabel("Number of Cases")
    plt.xticks(rotation='vertical')
    
    st.pyplot(fig)


# creates two side by side plots
# not being used currently
def double_plot(csstats_object,comp):
    sub_fig = plt.figure(figsize = (10, 5))
    #Plot 1
    data = csstats_object.desc_stats(csstats_object.frame)[comp]
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
def pie_plot(csstats_object,comp,frame):
    fig = plt.figure(figsize = (10, 5))

    data = csstats_object.desc_stats(frame)[comp]
    pie_labels = list(data.keys())
    values = np.array(list(data.values()))

    plt.pie(values, labels = pie_labels)
    st.pyplot(fig)
