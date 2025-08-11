import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import yfinance as yf
import requests
from io import StringIO

st.set_page_config(page_title="COT FX Prototype Dashboard", layout="wide")

st.title("Commitment of Traders (COT) FX Prototype Dashboard")
st.write("Prototype dashboard showing COT trends for major currency futures and corresponding FX pairs.")

# Currency futures tickers (CFTC codes)
futures_tickers = {
    "EURUSD": "099741",  # Euro FX
    "GBPUSD": "096742",  # British Pound
    "JPYUSD": "097741",  # Japanese Yen
    "AUDUSD": "232741",  # Australian Dollar
    "CADUSD": "090741",  # Canadian Dollar
    "CHFUSD": "092741"   # Swiss Franc
}

# Function to fetch COT data (placeholder approach)
def fetch_cot_data(cftc_code):
    try:
        url = f"https://www.cftc.gov/dea/futures/deacot{cftc_code}.txt"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        df = pd.read_csv(StringIO(response.text))
        return df
    except Exception:
        # Fallback: create dummy data
        dates = pd.date_range(end=pd.Timestamp.today(), periods=52, freq="W")
        df = pd.DataFrame({
            "Date": dates,
            "Net_Position": np.random.randint(-50000, 50000, len(dates))
        })
        return df

# Fetch and prepare data
cot_data = {}
for pair, code in futures_tickers.items():
    df = fetch_cot_data(code)
    df["COT_Index"] = (df["Net_Position"] - df["Net_Position"].rolling(52).min()) / (
        df["Net_Position"].rolling(52).max() - df["Net_Position"].rolling(52).min()
    ) * 100
    cot_data[pair] = df

# Dashboard layout
pair_choice = st.sidebar.selectbox("Select Currency Pair", list(futures_tickers.keys()))

df_selected = cot_data[pair_choice]

fig = go.Figure()
fig.add_trace(go.Scatter(x=df_selected["Date"], y=df_selected["Net_Position"],
                         name="Net Position", line=dict(color="blue")))
fig.add_trace(go.Scatter(x=df_selected["Date"], y=df_selected["COT_Index"],
                         name="COT Index", line=dict(color="orange"), yaxis="y2"))

fig.update_layout(
    title=f"COT Data for {pair_choice} Futures",
    yaxis=dict(title="Net Position"),
    yaxis2=dict(title="COT Index", overlaying="y", side="right"),
    legend=dict(x=0, y=1)
)

st.plotly_chart(fig, use_container_width=True)

# Download button
csv = df_selected.to_csv(index=False).encode("utf-8")
st.download_button("Download COT Data (CSV)", csv, f"{pair_choice}_COT.csv", "text/csv")
