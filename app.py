import streamlit as st
import pandas as pd

st.set_page_config(page_title="Bliss Tide FX Insights", layout="wide")

st.title("📊 Bliss Tide FX Insights")
st.write("Dashboard showing sample COT-based trends for major currency pairs.")

# Load sample data
df = pd.read_csv("sample_data.csv")
st.dataframe(df)

st.line_chart(df.set_index("Date"))
