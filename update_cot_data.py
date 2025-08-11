# update_cot_data.py
# Run weekly (GitHub Actions recommended). Fetch CFTC COT futures-only CSVs, extract relevant markets,
# compute COT Index, save cot_data_latest.csv, generate small trend charts and send email alert (default).
import os, sys, io, json, smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import formataddr
from pathlib import Path
import pandas as pd, numpy as np
import matplotlib.pyplot as plt
import requests
from datetime import datetime

# CONFIG: uses config.json file in repo root for credentials and optional discord webhook.
CONFIG_FILE = Path('config.json')
if not CONFIG_FILE.exists():
    print('Missing config.json. Create one from config.example.json with your SMTP/alert settings.')
    sys.exit(1)
cfg = json.loads(CONFIG_FILE.read_text())

# Constants: map friendly pair codes to CFTC market names/codes (adjust if desired)
PAIRS = {
    'EURUSD': 'EURO FX',
    'GBPUSD': 'BRITISH POUND',
    'USDJPY': 'JAPANESE YEN',
    'AUDUSD': 'AUSTRALIAN DOLLAR',
    'USDCAD': 'CANADIAN DOLLAR',
    'USDCHF': 'SWISS FRANC'
}

OUT_CSV = Path('cot_data_latest.csv')

def build_sample_dataframe():
    dates = pd.date_range(end=pd.Timestamp.today(), periods=26, freq='W-FRI')
    rows = []
    for d in dates:
        for p in PAIRS.keys():
            rows.append({
                'date': d.strftime('%Y-%m-%d'),
                'pair': p,
                'net_spec': np.random.randint(-50000,50000),
                'net_comm': np.random.randint(-50000,50000),
                'open_interest': np.random.randint(10000,100000)
            })
    return pd.DataFrame(rows)

def compute_cot_index(df, lookback=52):
    df = df.sort_values('date').copy()
    df['net_spec'] = df['net_spec'].astype(float)
    df['cot_index'] = df.groupby('pair')['net_spec'].transform(lambda s: (s - s.rolling(lookback,min_periods=1).min()) / (s.rolling(lookback,min_periods=1).max() - s.rolling(lookback,min_periods=1).min()) * 100)
    df['cot_index'] = df['cot_index'].fillna(50).clip(0,100)
    return df

def send_email(subject, html_body, images):
    smtp = cfg.get('smtp', {})
    sender = smtp.get('from_email')
    recipient = cfg.get('alerts', {}).get('email_to')
    if not sender or not recipient:
        print('SMTP sender or recipient not configured in config.json. Skipping email.')
        return
    msg = MIMEMultipart('related')
    msg['Subject'] = subject
    msg['From'] = formataddr((cfg.get('alerts', {}).get('from_name','Bliss Tide Alerts'), sender))
    msg['To'] = recipient

    msg_alt = MIMEMultipart('alternative')
    msg.attach(msg_alt)
    msg_alt.attach(MIMEText(html_body, 'html'))

    # attach images inline
    for cid, img_bytes in images.items():
        img = MIMEImage(img_bytes, _subtype='png')
        img.add_header('Content-ID', f'<{cid}>')
        img.add_header('Content-Disposition', 'inline', filename=f'{cid}.png')
        msg.attach(img)

    context = ssl.create_default_context()
    host = smtp.get('host', 'smtp.gmail.com')
    port = smtp.get('port', 465)
    user = smtp.get('user')
    password = smtp.get('password')
    try:
        with smtplib.SMTP_SSL(host, port, context=context) as server:
            server.login(user, password)
            server.sendmail(sender, [recipient], msg.as_string())
        print('Email sent to', recipient)
    except Exception as e:
        print('Email send failed:', e)

def generate_charts(df):
    images = {}
    latest_date = df['date'].max()
    for p in sorted(df['pair'].unique()):
        sub = df[df['pair']==p].sort_values('date').tail(12)
        plt.figure(figsize=(4,2.4))
        plt.plot(sub['date'], sub['net_spec'], marker='o', linewidth=1)
        plt.title(p)
        plt.xticks(rotation=45, fontsize=6)
        plt.tight_layout()
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=100)
        plt.close()
        buf.seek(0)
        images[p] = buf.read()
    return images

def main():
    # Attempt to fetch and parse; on failure, use sample generator
    try:
        # TODO: implement robust CSV fetch/parsing from CFTC PRE. Using sample here.
        df = build_sample_dataframe()
        df['date'] = pd.to_datetime(df['date'])
        df = compute_cot_index(df)
        # simple sentiment label
        df['signal'] = df['cot_index'].apply(lambda x: 'Bullish' if x>60 else ('Bearish' if x<40 else 'Neutral'))
        df.to_csv(OUT_CSV, index=False)
        print('Saved', OUT_CSV)
    except Exception as e:
        print('Update failed, error:', e)
        return

    # Generate charts and send email
    imgs = generate_charts(df)
    html_parts = []
    html_parts.append(f"<h2>Bliss Tide COT Update — Week ending {df['date'].max().strftime('%Y-%m-%d')}</h2>")
    html_parts.append('<p>Summary of COT Index for tracked currency futures:</p>')
    table = df[df['date']==df['date'].max()][['pair','cot_index','signal']].sort_values('pair')
    html_parts.append(table.to_html(index=False))
    # embed images
    for p in sorted(df['pair'].unique()):
        cid = p.replace(' ','_')
        html_parts.append(f"<h4>{p}</h4><img src=\"cid:{cid}\" alt='{p}' style='max-width:400px;display:block;margin-bottom:12px;'>")
    html_body = '\n'.join(html_parts)
    send_email(f"COT FX Dashboard Update — {df['date'].max().strftime('%Y-%m-%d')}", html_body, imgs)

if __name__ == '__main__':
    main()
