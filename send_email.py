import smtplib
from email.mime.text import MIMEText
import json
import pandas as pd

def send_email():
    with open("config.json") as f:
        config = json.load(f)

    df = pd.read_csv("sample_data.csv")
    html_table = df.to_html(index=False)

    msg = MIMEText(f"<h3>Bliss Tide FX Insights Report</h3>{html_table}", "html")
    msg["Subject"] = "Bliss Tide FX Insights - Weekly Report"
    msg["From"] = config["email_from"]
    msg["To"] = config["email_to"]

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(config["email_from"], config["email_password"])
        server.send_message(msg)

if __name__ == "__main__":
    send_email()
