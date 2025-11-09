import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import os, sys
from data_loader import load_data
from cards import render_kpis
from charts import render_status_pie, render_occupancy_line, render_prediction
from sentiment_ui import sentiment_panel
from room_status_chart import show_room_status_chart
# --- Streamlit Setup ---
st.set_page_config(page_title="Sapphire Inn", layout="wide")
import streamlit as st

st.markdown("""
<div class="header-slideshow">
  <img src="https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1600&q=80">
  <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=1600&q=80">
  <img src="https://images.unsplash.com/photo-1582719471137-c3967ffb1f86?auto=format&fit=crop&w=1600&q=80">
  <img src="https://images.unsplash.com/photo-1600047509321-6d3fefc9b30c?auto=format&fit=crop&w=1600&q=80">
  <img src="https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=1600&q=80">
  <img src="https://images.unsplash.com/photo-1578683010236-d716f9a3f461?auto=format&fit=crop&w=1600&q=80">
</div>
""", unsafe_allow_html=True)

# --- CSS Styling ---
css_path = os.path.join(os.path.dirname(__file__), "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Data ---
df = load_data("data/hotel_data.csv")

# --- Sidebar Filters ---
st.sidebar.header("Filters")
min_date = df['date'].min().date()
max_date = df['date'].max().date()

date_range = st.sidebar.date_input(
    "📅 Booking Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

room_types = st.sidebar.multiselect(
    "🏠 Room Type",
    options=df['room_type'].unique().tolist(),
    default=df['room_type'].unique().tolist()
)

min_rating = st.sidebar.slider("⭐ Minimum Rating", 1, 5, 3)

# --- Toggle for Room Status ---
st.sidebar.markdown("### Room Status Filter")
status_filter = st.sidebar.radio(
    "Show Rooms:",
    ["All", "Booked Only", "Vacant Only"],
    index=0,
    horizontal=True
)

# --- Filter Logic ---
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

mask = (
    (df['date'] >= start_date) &
    (df['date'] <= end_date) &
    (df['room_type'].isin(room_types)) &
    (df['rating'] >= min_rating)
)

if status_filter == "Booked Only":
    mask &= (df['is_booked'] == 1)
elif status_filter == "Vacant Only":
    mask &= (df['is_booked'] == 0)

df_f = df[mask].copy()

# --- Header ---
st.markdown("<h1 class='page-title'>🏨 Sapphire Inn</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>AI-powered hotel analytics — bookings, reviews & predictions</p>", unsafe_allow_html=True)

# --- KPI Cards ---
render_kpis(df_f)

# --- Animated Charts ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        render_status_pie(df_f)
    with col2:
        render_occupancy_line(df_f)
        # --- Live Room Status Interactive Chart ---
st.markdown("<hr>", unsafe_allow_html=True)
show_room_status_chart(df_f)

# --- Prediction ---
render_prediction(df)

# --- Sentiment Analyzer ---
st.markdown("<hr>", unsafe_allow_html=True)
sentiment_panel()
