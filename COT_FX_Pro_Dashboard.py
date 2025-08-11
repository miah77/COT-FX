import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="COT FX Pro Dashboard", layout="wide")

st.title("💹 COT FX Pro Dashboard (with Sample Data Fallback)")

@st.cache_data
def load_data():
    try:
        # Here you'd normally fetch live CFTC data
        raise Exception("Simulated live data fetch failure")
    except:
        return pd.read_csv("sample_cot_data.csv")

df = load_data()
df['date'] = pd.to_datetime(df['date'])

# Sidebar filters
st.sidebar.header("Filter Options")
pairs = df["pair"].unique()
selected_pair = st.sidebar.selectbox("Select Currency Pair", pairs)
date_range = st.sidebar.date_input("Select Date Range", [df['date'].min(), df['date'].max()])

# Filter data
mask = (df['pair'] == selected_pair) & (df['date'] >= pd.to_datetime(date_range[0])) & (df['date'] <= pd.to_datetime(date_range[1]))
pair_data = df[mask]

# Layout: two columns for charts
col1, col2 = st.columns(2)

# Chart 1: Line plot of COT Index
with col1:
    fig_line = px.line(pair_data, x="date", y="cot_index", title=f"COT Index Trend for {selected_pair}",
                       markers=True)
    fig_line.update_traces(line_color="royalblue")
    st.plotly_chart(fig_line, use_container_width=True)

# Chart 2: Signal distribution over time (bar chart)
with col2:
    signal_counts = pair_data.groupby("signal").size().reset_index(name="count")
    fig_bar = px.bar(signal_counts, x="signal", y="count", title=f"Signal Distribution for {selected_pair}",
                     color="signal", color_discrete_map={"Bullish": "green", "Bearish": "red", "Neutral": "gray"})
    st.plotly_chart(fig_bar, use_container_width=True)

# Sentiment heatmap for all pairs
st.subheader("📊 Sentiment Heatmap (All Pairs)")
heatmap_data = df.pivot_table(index="pair", columns="date", values="cot_index")
fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale="RdYlGn",
    colorbar=dict(title="COT Index")
))
fig_heatmap.update_layout(height=500)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Raw data table
st.subheader("📄 Raw Data")
st.dataframe(pair_data.reset_index(drop=True))
