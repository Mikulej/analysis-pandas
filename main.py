import pandas as pd
import sys
import streamlit as st
import matplotlib

def main():

    #load dataset
    df = pd.read_csv("bigmac.csv")

    #get names of countries
    print("List of countries: ", df['name'].unique())

    #filter rows between 2005-2015
    mask = (df['date'] > '2005-1-01') & (df['date'] <= '2015-1-01')
    df = df.loc[mask]

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
    #create business dashboard
    #     st.write("""
# # My first app
# Hello *world!*
#              """)


if __name__ == "__main__":
    main()