import pandas as pd 
import streamlit as st
from china_japan import generate_forecast

# Set page config
st.set_page_config(page_title="HRC Price Forecasting Model Dashboard", layout="wide")

# --- Custom Dashboard Title ---
st.markdown("""
    <div style='text-align: center; padding: 1rem 0; background-color: #0080C7; color: white; border-radius: 8px;'>
        <h1 style='margin-bottom: 0.3rem;'>HRC Price Forecasting Model Dashboard</h1>
        <p style='font-size: 18px;'>Forecasting HRC prices for China & Japan: Landed Price Determination in India for TATA Steel</p>
    </div>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.header("Model Parameters")

# Upside Inputs
st.sidebar.markdown("**Upside Adjustments**")
up_iron_ore = st.sidebar.number_input("Iron Ore (CFR, $/t) (Upside)", min_value=0, max_value=1000, value=100)
up_hcc = st.sidebar.number_input("HCC (Aus FOB, $/t) (Upside)", min_value=0, max_value=1000, value=220)
up_scrap = st.sidebar.number_input("Domestic Scrap (DDP Jiangsu incl. VAT $/t) (Upside)", min_value=0, max_value=1000, value=400)
up_export = st.sidebar.number_input("Monthly Export of Semis & Finished Steel as % of Production (Upside)", min_value=0, max_value=100, value=9)
up_fai = st.sidebar.number_input("FAI in urban real estate development (y-o-y) Growth (Upside)", min_value=0, max_value=100, value=5)

# Downside Inputs
st.sidebar.markdown("**Downside Adjustments**")
down_iron_ore = st.sidebar.number_input("Iron Ore (CFR, $/t) (Downside)", min_value=0, max_value=1000, value=85)
down_hcc = st.sidebar.number_input("HCC (Aus FOB, $/t) (Downside)", min_value=0, max_value=1000, value=180)
down_scrap = st.sidebar.number_input("Domestic Scrap (DDP Jiangsu incl. VAT $/t) (Downside)", min_value=0, max_value=1000, value=350)
down_export = st.sidebar.number_input("Monthly Export of Semis & Finished Steel as % of Production (Downside)", min_value=-100, max_value=100, value=12)
down_fai = st.sidebar.number_input("FAI in urban real estate development (y-o-y) Growth (Downside)", min_value=-100, max_value=100, value=1)

# Select countries to be displayed
st.sidebar.markdown("**Country Selection**")
selected_countries = st.sidebar.multiselect(
    "Select country to view:",
    options=["China", "Japan"],
    default=["China", "Japan"]
)

# --- Plot graph ---
fig, CN_JP_forecast = generate_forecast(up_iron_ore, up_hcc, up_scrap, up_export, up_fai, down_iron_ore, down_hcc, down_scrap, down_export, down_fai, selected_countries)
st.plotly_chart(fig, use_container_width=True)

# --- Export China's and Japan's forecasted HRC prices as csv ---
CN_JP_forecast_csv = CN_JP_forecast.to_csv(index=True).encode("utf-8")
 
# Download button
st.download_button(
    label="📥 Download China's and Japan's forecasted HRC prices as CSV",
    data=CN_JP_forecast_csv,
    file_name="hrc_forecast.csv",
    mime="text/csv"
)
st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

# Obtain list of forecasted dates
date_options = CN_JP_forecast.index.tolist()

# Dropdown for date selection
selected_date = st.selectbox("📅 Select Month for Landed Price Calculation", date_options)

# Obtain China's and Japan's forecasted HRC price
CN_forecasted_value = CN_JP_forecast.loc[selected_date, 'China HRC Forecast (FOB, $/t)']
JP_forecasted_value = CN_JP_forecast.loc[selected_date, 'Japan HRC Forecast (FOB, $/t)']

col1, col2 = st.columns(2)
# --- India Landed Price (China) Calculator ---
with col1:
    st.subheader("Landed Price of China's HRC in India")

    # Editable fields
    sea_freight = st.number_input("Sea Freight ($/t)", value=30, key=1)
    basic_customs_duty = st.number_input("Basic Customs Duty (%)", value=7.5, key=2)
    antidumping = st.number_input("Antidumping from 8th Aug'16 to 7th Aug'21 ($/t)", value=0, key=3)
    mip = st.number_input("MIP (5th Feb 2016 to 4th Aug 2016) ($/t)", value=0, key=4)
    safeguard_duty = st.number_input("Safeguard Duty (%)", value=0, key=5)
    applicable_SGD = st.number_input("Applicable SGD ($/t)", value=0, key=6)
    LC_Port_charges = st.number_input("LC Charges & Port Charges ($/t)", value=10, key=7)
    exchange_rate = st.number_input("Exchange Rate (INR/$)", value=86, key=8)
    freight_port_city = st.number_input("Freight (from port to city) (Rs/t)", value=500, key=9)

    china_landed_price = pd.DataFrame({
        "HRC FOB China ($/t)": [CN_forecasted_value],
        "Sea Freight ($/t)": [sea_freight],
        "HRC CFR at Mumbai Port (A) ($/t)": [0],
        "Insurance @1% on CFR ($/t)": [0],
        "CIF / Assessable Value ($/t)": [0],
        "Basic Customs Duty (%)": [basic_customs_duty],
        "Basic Customs Duty (Absolute) ($/t)": [0],
        "Social Welfare Surcharge @10% on BCD ($/t)": [0],
        "Landed Value ($/t)": [0],
        "Antidumping from 8th Aug'16 to 7th Aug'21 ($/t)": [antidumping],
        "MIP (5th Feb 2016 to 4th Aug 2016) ($/t)": [mip],
        "Safeguard Duty (%)": [safeguard_duty],
        "Safeguard Duty (Absolute) ($/t)": [0],
        "Applicable SGD ($/t)": [applicable_SGD],
        "LC Charges & Port Charges ($/t)": [LC_Port_charges],
        "Landed Price at Port ($/t)": [0],
        "Exchange Rate (INR/$)": [exchange_rate],
        "Landed Price @ Mumbai Port (Rs/t)": [0],
        "Freight (from port to city) (Rs/t)": [freight_port_city],
        "HRC Basic Landed @ Mumbai Market (Rs/t)": [0]
    })

    # Recalculate rows that are dependent on other rows
    china_landed_price["HRC CFR at Mumbai Port (A) ($/t)"] = china_landed_price["HRC FOB China ($/t)"] + china_landed_price["Sea Freight ($/t)"]
    china_landed_price["Insurance @1% on CFR ($/t)"] = china_landed_price["HRC CFR at Mumbai Port (A) ($/t)"] * 0.01
    china_landed_price["CIF / Assessable Value ($/t)"] = china_landed_price["Insurance @1% on CFR ($/t)"] + china_landed_price["HRC CFR at Mumbai Port (A) ($/t)"]
    china_landed_price["Basic Customs Duty (Absolute) ($/t)"] = china_landed_price["CIF / Assessable Value ($/t)"] * (china_landed_price["Basic Customs Duty (%)"]/100)
    china_landed_price["Social Welfare Surcharge @10% on BCD ($/t)"] = china_landed_price["Basic Customs Duty (Absolute) ($/t)"] * 0.1
    china_landed_price["Landed Value ($/t)"] = china_landed_price["CIF / Assessable Value ($/t)"] + china_landed_price["Basic Customs Duty (Absolute) ($/t)"] + china_landed_price["Social Welfare Surcharge @10% on BCD ($/t)"]
    china_landed_price["Safeguard Duty (Absolute) ($/t)"] = china_landed_price["Landed Value ($/t)"] * china_landed_price["Safeguard Duty (%)"]
    china_landed_price["Landed Price at Port ($/t)"] = china_landed_price["LC Charges & Port Charges ($/t)"] + china_landed_price["Applicable SGD ($/t)"] + china_landed_price["Antidumping from 8th Aug'16 to 7th Aug'21 ($/t)"] + china_landed_price["Landed Value ($/t)"] + china_landed_price["MIP (5th Feb 2016 to 4th Aug 2016) ($/t)"]
    china_landed_price["Landed Price @ Mumbai Port (Rs/t)"] = china_landed_price["Exchange Rate (INR/$)"] * china_landed_price["Landed Price at Port ($/t)"]
    china_landed_price["HRC Basic Landed @ Mumbai Market (Rs/t)"] = china_landed_price["Landed Price @ Mumbai Port (Rs/t)"] + china_landed_price["Freight (from port to city) (Rs/t)"]
    
    # Transform dataframe
    china_landed_price_modified = china_landed_price.T
    china_landed_price_modified.columns = ["Price"]
    china_landed_price_modified.index.name = "Breakdown"
    st.dataframe(china_landed_price_modified, use_container_width=True)
    final_price = china_landed_price_modified["Price"]["HRC Basic Landed @ Mumbai Market (Rs/t)"]

    # Display India landed price
    st.markdown(f"<span style='color:#0080C7; font-weight:bold;'>The landed price of China's HRC in India is: ₹ {final_price:.0f}/t</span>", unsafe_allow_html=True)

# --- India Landed Price (Japan) Calculator ---
with col2:
    st.subheader("Landed Price of Japan's HRC in India")

    # Editable fields
    sea_freight_JP = st.number_input("Sea Freight ($/t)", value=30, key=11)
    basic_customs_duty_JP = st.number_input("Basic Customs Duty (%)", value=0, key=22)
    antidumping_JP = st.number_input("Antidumping from 8th Aug'16 to 7th Aug'21 ($/t)", value=0, key=33)
    mip_JP = st.number_input("MIP (5th Feb 2016 to 4th Aug 2016) ($/t)", value=0, key=44)
    safeguard_duty_JP = st.number_input("Safeguard Duty (%)", value=0, key=55)
    applicable_SGD_JP = st.number_input("Applicable SGD ($/t)", value=0, key=66)
    LC_Port_charges_JP = st.number_input("LC Charges & Port Charges ($/t)", value=10, key=77)
    exchange_rate_JP = st.number_input("Exchange Rate (INR/$)", value=86, key=88)
    freight_port_city_JP = st.number_input("Freight (from port to city) (Rs/t)", value=500, key=99)

    japan_landed_price = pd.DataFrame({
        "HRC FOB Japan ($/t)": [JP_forecasted_value],
        "Sea Freight ($/t)": [sea_freight_JP],
        "HRC CFR at Mumbai Port (A) ($/t)": [0],
        "Insurance @1% on CFR ($/t)": [0],
        "CIF / Assessable Value ($/t)": [0],
        "Basic Customs Duty (%)": [basic_customs_duty_JP],
        "Basic Customs Duty (Absolute) ($/t)": [0],
        "Social Welfare Surcharge @10% on BCD ($/t)": [0],
        "Landed Value ($/t)": [0],
        "Antidumping from 8th Aug'16 to 7th Aug'21 ($/t)": [antidumping_JP],
        "MIP (5th Feb 2016 to 4th Aug 2016) ($/t)": [mip_JP],
        "Safeguard Duty (%)": [safeguard_duty_JP],
        "Safeguard Duty (Absolute) ($/t)": [0],
        "Applicable SGD ($/t)": [applicable_SGD_JP],
        "LC Charges & Port Charges ($/t)": [LC_Port_charges_JP],
        "Landed Price at Port ($/t)": [0],
        "Exchange Rate (INR/$)": [exchange_rate_JP],
        "Landed Price @ Mumbai Port (Rs/t)": [0],
        "Freight (from port to city) (Rs/t)": [freight_port_city_JP],
        "HRC Basic Landed @ Mumbai Market (Rs/t)": [0]
    })

    # Recalculate rows that are dependent on other rows
    japan_landed_price["HRC CFR at Mumbai Port (A) ($/t)"] = japan_landed_price["HRC FOB Japan ($/t)"] + japan_landed_price["Sea Freight ($/t)"]
    japan_landed_price["Insurance @1% on CFR ($/t)"] = japan_landed_price["HRC CFR at Mumbai Port (A) ($/t)"] * 0.01
    japan_landed_price["CIF / Assessable Value ($/t)"] = japan_landed_price["Insurance @1% on CFR ($/t)"] + japan_landed_price["HRC CFR at Mumbai Port (A) ($/t)"]
    japan_landed_price["Basic Customs Duty (Absolute) ($/t)"] = japan_landed_price["CIF / Assessable Value ($/t)"] * (japan_landed_price["Basic Customs Duty (%)"]/100)
    japan_landed_price["Social Welfare Surcharge @10% on BCD ($/t)"] = japan_landed_price["Basic Customs Duty (Absolute) ($/t)"] * 0.1
    japan_landed_price["Landed Value ($/t)"] = japan_landed_price["CIF / Assessable Value ($/t)"] + japan_landed_price["Basic Customs Duty (Absolute) ($/t)"] + japan_landed_price["Social Welfare Surcharge @10% on BCD ($/t)"]
    japan_landed_price["Safeguard Duty (Absolute) ($/t)"] = japan_landed_price["Landed Value ($/t)"] * japan_landed_price["Safeguard Duty (%)"]
    japan_landed_price["Landed Price at Port ($/t)"] = japan_landed_price["LC Charges & Port Charges ($/t)"] + japan_landed_price["Applicable SGD ($/t)"] + japan_landed_price["Antidumping from 8th Aug'16 to 7th Aug'21 ($/t)"] + japan_landed_price["Landed Value ($/t)"] + japan_landed_price["MIP (5th Feb 2016 to 4th Aug 2016) ($/t)"]
    japan_landed_price["Landed Price @ Mumbai Port (Rs/t)"] = japan_landed_price["Exchange Rate (INR/$)"] * japan_landed_price["Landed Price at Port ($/t)"]
    japan_landed_price["HRC Basic Landed @ Mumbai Market (Rs/t)"] = japan_landed_price["Landed Price @ Mumbai Port (Rs/t)"] + japan_landed_price["Freight (from port to city) (Rs/t)"]
    
    # Transform dataframe
    japan_landed_price_modified = japan_landed_price.T
    japan_landed_price_modified.columns = ["Price"]
    japan_landed_price_modified.index.name = "Breakdown"
    st.dataframe(japan_landed_price_modified, use_container_width=True)
    final_price_JP = japan_landed_price_modified["Price"]["HRC Basic Landed @ Mumbai Market (Rs/t)"]

    # Display India landed price
    st.markdown(f"<span style='color:#0080C7; font-weight:bold;'>The landed price of Japan's HRC in India is: ₹ {final_price_JP:.0f}/t</span>", unsafe_allow_html=True)
    