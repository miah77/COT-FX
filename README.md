# COT FX Prototype Dashboard

This is a prototype Streamlit dashboard that visualizes Commitment of Traders (COT) data for major currency pairs.

## Features
- Displays COT index trends for major FX pairs.
- Uses sample data for offline/demo mode.
- Can be adapted to fetch live CFTC data.

## Running Locally
```bash
pip install -r requirements.txt
streamlit run COT_FX_Prototype_Dashboard.py
```

## Deploying to Streamlit Cloud
1. Upload these files to a public GitHub repo.
2. Go to https://streamlit.io/cloud and create a new app.
3. Select this repo and set the entrypoint file to `COT_FX_Prototype_Dashboard.py`.
4. Deploy and enjoy.

