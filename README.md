# bliss-tide-fx-insights

Prototype COT-based FX insights dashboard and automated weekly updater.

## Files in this repo
- `app.py` — Streamlit dashboard (loads `cot_data_latest.csv` if present, else uses `sample_cot_data.csv`)
- `update_cot_data.py` — weekly updater script that saves `cot_data_latest.csv` and sends email alerts
- `config.example.json` — example config. Copy to `config.json` and add your SMTP/password and alert email.
- `.github/workflows/update_cot.yml` — GitHub Actions workflow to run updater every Friday.
- `sample_cot_data.csv` — included demo dataset (so the app works immediately)
- `requirements.txt` — dependencies for Streamlit Cloud and GitHub Actions

## Quickstart
1. Extract files and push to a new GitHub repo named **bliss-tide-fx-insights**.
2. Copy `config.example.json` → `config.json` and fill in SMTP + `alerts.email_to`.
3. On GitHub, enable Actions (should be on by default) and add repository secrets if needed.
4. Deploy `app.py` to Streamlit Cloud (set entrypoint to `app.py`).
5. The updater will run weekly and commit `cot_data_latest.csv` back to the repo; Streamlit Cloud will pick up changes.

## Email Alerts (Default)
- The updater uses SMTP credentials in `config.json` to send an HTML email with inline PNG charts.
- For Gmail, create an App Password and use it in `config.json` (do not store your primary password).

## Notes & Next Steps
- The current updater uses a sample data generator. Replace `build_sample_dataframe()` or implement parsing from CFTC PRE CSVs for production.
- Optionally add Discord webhook to `config.json` to enable Discord alerts.
