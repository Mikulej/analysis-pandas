import pandas as pd
import sys
import streamlit as st

def main():
    df = pd.read_csv("bigmac.csv")
    print(df.head(10))
    print(df.tail(10))
    st.write("""
# My first app
Hello *world!*
             """)

if __name__ == "__main__":
    main()