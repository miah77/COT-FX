# COT FX Prototype Dashboard

A prototype Streamlit dashboard to visualize Commitment of Traders (COT) data for major currency futures and FX pairs.

## Features
- Fetches COT data (with fallback to random sample data if unavailable)
- Calculates a 52-week COT Index
- Interactive chart with Net Position & COT Index
- CSV download

## Installation
```bash
pip install -r requirements.txt
```

## Run
```bash
streamlit run COT_FX_Prototype_Dashboard.py
```

## Deploy to Streamlit Cloud
1. Push this repo to GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Create a new app and select `COT_FX_Prototype_Dashboard.py` as the entry point
