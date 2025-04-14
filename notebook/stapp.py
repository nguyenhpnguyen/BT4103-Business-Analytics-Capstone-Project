import os
import pandas as pd 
import streamlit as st

from china_japan import generate_forecast

# --- Sidebar ---
st.sidebar.header("Model Parameters")

# Upside Inputs
st.sidebar.markdown("**Upside Adjustments**")
up_iron_ore = st.sidebar.number_input("Iron Ore (Upside)", min_value=0, max_value=1000, value=100)
up_hcc = st.sidebar.number_input("HCC (Upside)", min_value=0, max_value=1000, value=220)
up_scrap = st.sidebar.number_input("Scrap (Upside)", min_value=0, max_value=1000, value=400)
up_export = st.sidebar.number_input("Export (Upside)", min_value=0, max_value=100, value=9)
up_fai = st.sidebar.number_input("FAI (Upside)", min_value=0, max_value=100, value=5)

# Downside Inputs
st.sidebar.markdown("**Downside Adjustments**")
down_iron_ore = st.sidebar.number_input("Iron Ore (Downside)", min_value=0, max_value=1000, value=85)
down_hcc = st.sidebar.number_input("HCC (Downside)", min_value=0, max_value=1000, value=180)
down_scrap = st.sidebar.number_input("Scrap (Downside)", min_value=0, max_value=1000, value=350)
down_export = st.sidebar.number_input("Export (Downside)", min_value=-100, max_value=100, value=12)
down_fai = st.sidebar.number_input("FAI (Downside)", min_value=-100, max_value=100, value=1)

months = st.sidebar.slider("Months ahead from 2024-10-01", min_value=6, max_value=30, value=17)

line_options = st.multiselect(
    "Select lines to plot:",
    options=["China", "Japan"],
    default=["China", "Japan"]
)

fig, CN_forecast, JP_forecast = generate_forecast(up_iron_ore, up_hcc, up_scrap, up_export, up_fai, down_iron_ore, down_hcc, down_scrap, down_export, down_fai, months, line_options)
st.plotly_chart(fig, use_container_width=True)

# Get list of dates (convert to string for dropdown)
date_options = JP_forecast.index.strftime('%Y-%m-%d').tolist()

# Dropdown for date selection
selected_date = st.selectbox("Select a date:", date_options)

# Convert selected date back to datetime to filter df
selected_date_dt = pd.to_datetime(selected_date)

# Display corresponding value from df1 and df2
CN_forecasted_value = CN_forecast.loc[selected_date_dt, 'HRC (FOB, $/t)_f']
JP_forecasted_value = JP_forecast.loc[selected_date_dt, 'Japan HRC (FOB, $/t)_f']

st.metric("China's HRC price", CN_forecasted_value)
st.metric("Japan's HRC price", JP_forecasted_value)