import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_email(post):
    body = f"""🚨 New LinkedIn Hiring Post!

Author: {post['author']}
Link: {post['link']}

Post:
{post['text']}
"""

    msg = MIMEText(body)
    msg['Subject'] = 'New LinkedIn Hiring Post Found!'
    msg['From'] = os.getenv("GMAIL_USER")
    msg['To'] = os.getenv("GMAIL_USER")

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
            server.sendmail(msg['From'], [msg['To']], msg.as_string())
        print("📧 Email notification sent.")
    except Exception as e:
        print("⚠️ Failed to send email:", e)
