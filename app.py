import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="Bliss Tide FX Insights", layout="wide")
st.title("Bliss Tide — COT FX Insights (Prototype)")
st.markdown("Auto-updating COT-based FX dashboard. Data updates weekly via GitHub Actions.")

DATA_FILE = Path('cot_data_latest.csv')
SAMPLE_FILE = Path('sample_cot_data.csv')

@st.cache_data
def load_data():
    if DATA_FILE.exists():
        df = pd.read_csv(DATA_FILE, parse_dates=['date'])
    else:
        df = pd.read_csv(SAMPLE_FILE, parse_dates=['date'])
    return df

df = load_data()

st.sidebar.header('Filters')
pairs = sorted(df['pair'].unique().tolist())
pair = st.sidebar.selectbox('Select pair', pairs)
min_date = df['date'].min().date()
max_date = df['date'].max().date()
date_range = st.sidebar.date_input('Date range', [min_date, max_date])

mask = (df['pair'] == pair) & (df['date'] >= pd.to_datetime(date_range[0])) & (df['date'] <= pd.to_datetime(date_range[1]))
df_pair = df.loc[mask].sort_values('date')

st.subheader(f'📈 {pair} — COT Index & Signal')
fig = go.Figure()
fig.add_trace(go.Scatter(x=df_pair['date'], y=df_pair['cot_index'], name='COT Index', mode='lines+markers'))
fig.update_yaxes(title_text='COT Index (0-100)', secondary_y=False)
st.plotly_chart(fig, use_container_width=True, height=450)

st.subheader('📊 Sentiment & Signals (Recent)')
recent = df[df['date'] == df['date'].max()].sort_values('pair')
st.table(recent[['pair','cot_index','signal']].set_index('pair'))

st.subheader('📄 Raw Data (filtered)')
st.dataframe(df_pair.reset_index(drop=True))

st.markdown('---')
st.write('Data source: `cot_data_latest.csv` (auto-updated) or `sample_cot_data.csv` fallback.')
