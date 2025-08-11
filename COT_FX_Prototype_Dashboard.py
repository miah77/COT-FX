import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="COT FX Dashboard", layout="wide")

st.title("💹 COT FX Prototype Dashboard (with Sample Data Fallback)")

@st.cache_data
def load_data():
    try:
        # Here you'd normally fetch live CFTC data
        # Simulate a failure to trigger sample data
        raise Exception("Simulated live data fetch failure")
    except:
        return pd.read_csv("sample_cot_data.csv")

df = load_data()

pairs = df["pair"].unique()
selected_pair = st.selectbox("Select Currency Pair", pairs)

pair_data = df[df["pair"] == selected_pair]

fig = px.line(pair_data, x="date", y="cot_index", title=f"COT Index for {selected_pair}")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Raw Data")
st.dataframe(pair_data)
