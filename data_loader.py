import pandas as pd
import streamlit as st

@st.cache_data
def load_data(path="data/hotel_data.csv"):
    df = pd.read_csv(path, parse_dates=['date', 'check_in', 'check_out'])
    df.fillna(0, inplace=True)
    return df