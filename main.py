import pandas as pd
import sys
import streamlit as st
import matplotlib
import datetime
def main():

    #load dataset
    df = pd.read_csv("bigmac.csv")

    #get names of countries
    country_list = df['name'].unique()
    print("List of countries: ", country_list)
    value_type_list = list(df.columns[-3:])
    print("List of price types to compare: ", value_type_list)

    #group by name
    grouped = df.groupby('name')
    print("GROUPING BY NAME")
    for group in grouped:
        print(group)

    #get mean and std
    statictics = grouped[['local_price','dollar_ex','dollar_price']].agg(['mean','std'])

    price_means = statictics['dollar_price']['mean']

    #find cheapest and the most expensive big-mac
    print(price_means.min())
    print(price_means.max())

    #Initialize dashboard
    st.set_page_config(page_title="Business DashBoard",
                       page_icon=":bar_chart:",
                       layout="wide",
                       initial_sidebar_state="expanded")
    
    # Options
    st.sidebar.header("Dashboard Options")
    selected_country = st.sidebar.selectbox('Country',country_list)
    selected_value_type = st.sidebar.selectbox('Value Type',value_type_list)
    time_constraint = st.sidebar.toggle(label="Date constraint")
    date_start = None
    date_end = None
    if time_constraint:
        date_tuple = st.sidebar.date_input('Time period:', (datetime.date(2000,4,1),datetime.date(2020,1,15)),min_value=datetime.date(2000,4,1),max_value=datetime.date(2020,1,15))
        if len(date_tuple) == 2:
            date_start = date_tuple[0]
            date_end = date_tuple[1]
    

    labelY = None
    match selected_value_type:
        case "local_price":
            labelY = "Local Price"
        case "dollar_ex":
            labelY = "Dollar Exchange Rate"
        case "dollar_price":
            labelY = "Dollar Price"

    #Dashboard
    st.write("""
# Big Mac DataSet
Explore how prices of **Big Mac** changed over time
             """)
    mask = (df['name'] == selected_country)
    group = df.loc[mask]
    if time_constraint and date_start != None and date_end != None:
        group = group.loc[(pd.to_datetime(group['date']) >= pd.to_datetime(date_start)) & (pd.to_datetime(group['date']) <= pd.to_datetime(date_end))]

    st.bar_chart(group,x="date",x_label="Date",y=selected_value_type,y_label=labelY,color="#f54e42")
    st.line_chart(group,x="date",x_label="Date",y=selected_value_type,y_label=labelY,color="#7bf542")
    st.area_chart(group,x="date",x_label="Date",y=selected_value_type,y_label=labelY,color="#3035c9")

    minValue = group[selected_value_type].min()
    maxValue = group[selected_value_type].max()
    minRow = group.loc[group[selected_value_type]==minValue]
    maxRow = group.loc[group[selected_value_type]==maxValue]

    containerEdgeValues1 = st.columns(2)
    tile = containerEdgeValues1[0].container(border=False)
    tile.write("Lowest Values:")
    tile = containerEdgeValues1[1].container(border=False)
    tile.write("Highest Values:")

    containerEdgeValues2 = st.columns(2)
    tile = containerEdgeValues2[0].container(border=False)
    tile.write(minRow)
    tile = containerEdgeValues2[1].container(border=False)
    tile.write(maxRow)

    containerLinks = st.columns(8)
    tile = containerLinks[0].container(height=60,border=False)
    tile.page_link("https://calmcode.io/datasets/bigmac", label="DataSet", icon="💾")
    tile = containerLinks[1].container(height=60,border=False)
    tile.page_link("https://github.com/Mikulej/analysis-pandas", label="Repository", icon="📕")



if __name__ == "__main__":
    main()