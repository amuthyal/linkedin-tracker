import smtplib
import os
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_email(post):
    body = f"New LinkedIn Hiring Post:\n\nAuthor: {post['author']}\n\n{post['text']}\n\nLink: {post['link']}"
    msg = MIMEText(body)
    msg['Subject'] = '🚨 New Hiring Post Detected!'
    msg['From'] = os.getenv("GMAIL_USER")
    msg['To'] = os.getenv("GMAIL_USER")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        server.login(os.getenv("GMAIL_USER"), os.getenv("GMAIL_PASS"))
        server.sendmail(msg['From'], [msg['To']], msg.as_string())
