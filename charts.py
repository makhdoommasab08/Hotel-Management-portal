import streamlit as st
import plotly.express as px
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

def render_status_pie(df):
    st.subheader("Room Status")
    if df.empty:
        st.info("No data found.")
        return
    counts = df['is_booked'].value_counts().rename({0: 'Vacant', 1: 'Booked'})
    values = [counts.get(1,0), counts.get(0,0)]
    labels = ['Booked','Vacant']
    fig = px.pie(values=values, names=labels, hole=0.4, title="Booked vs Vacant")
    st.plotly_chart(fig, use_container_width=True)

def render_occupancy_line(df):
    st.subheader("Occupancy Over Time")
    if df.empty:
        st.info("No data available.")
        return
    daily = df.groupby('date')['is_booked'].sum().reset_index()
    fig = px.line(daily, x='date', y='is_booked', title="Daily Bookings")
    st.plotly_chart(fig, use_container_width=True)

def render_prediction(df):
    st.subheader("Booking Prediction (Next 7 Days)")
    daily = df.groupby('date')['is_booked'].sum().reset_index().sort_values('date')
    if len(daily) < 5:
        st.warning("Not enough data for prediction.")
        return
    daily['day_num'] = (daily['date'] - daily['date'].min()).dt.days
    X, y = daily[['day_num']], daily['is_booked']
    model = LinearRegression().fit(X, y)
    future_days = np.arange(daily['day_num'].max() + 1, daily['day_num'].max() + 8).reshape(-1, 1)
    preds = model.predict(future_days)
    pred_df = pd.DataFrame({'date': [daily['date'].max() + pd.Timedelta(days=i) for i in range(1, 8)], 'Predicted': preds})
    fig = px.line(pred_df, x='date', y='Predicted', title="Predicted Bookings")
    st.plotly_chart(fig, use_container_width=True)