# 🔍 LinkedIn Hiring Tracker

This project is an automated tracker that scans your LinkedIn feed for job posts using targeted hiring keywords and filters. It extracts relevant posts (such as those hiring **software developers, SDEs, frontend/full stack engineers**) and saves them to a connected Google Sheet. It can also send email notifications when new relevant posts are found.

---

## 🚀 Features

- ✅ Login to LinkedIn and scrape feed posts
- ✅ Match posts using **fuzzy keyword detection** (e.g., “we'r hiring”, “join our team”)
- ✅ Filter for **target roles only** (e.g., software engineer, SDE II, full stack developer)
- ✅ Extract hashtags from each post
- ✅ Store posts in a **Google Sheet** with timestamp, text, author, keyword, and hashtags
- ✅ Avoid duplicates using fingerprinting
- ✅ Remove false positives and off-topic roles using a cleanup script
- ✅ Send optional **email notifications** for new matches

---

## 📂 Project Structure

```
linkedin-tracker/
│
├── main.py                    # Main script to run the tracker
├── linkedin_scraper.py       # LinkedIn login and post scraping logic
├── google_sheets.py          # Google Sheets integration and post saving
├── notifier.py               # Optional email notifier
├── credentials.json          # Google Service Account credentials
├── keywords.txt              # List of hiring-related keywords (one per line)
├── cleanup.py                # One-time script to remove irrelevant rows from sheet
└── README.md                 # This file
```

---

## 🧠 Prerequisites

- Python 3.8+
- Google Sheets API credentials
- Google Chrome + ChromeDriver
- Gmail App Password (if using email notifications)

---

## 📦 Setup Instructions

### 1. Install dependencies
```bash
pip install gspread oauth2client selenium
```

### 2. Create `credentials.json` for Google Sheets API

Follow [this guide](https://gspread.readthedocs.io/en/latest/oauth2.html) to generate your `credentials.json`.

### 3. Update `keywords.txt`

Add relevant hiring phrases (one per line), e.g.:

```
we are hiring
my team is hiring
join our team
open positions
actively hiring
```

---

## 🛠️ Run the Tracker

```bash
python main.py
```

The script will:

- Login to LinkedIn
- Scrape the feed
- Match posts using keywords and role titles
- Save matches to Google Sheet
- Send notifications (if enabled)

---

## 🧹 Clean Old or Irrelevant Posts

To remove posts that aren't about your target roles:
```bash
python cleanup.py
```

This will clean the Google Sheet by removing rows that:
- Match known false positives
- Don’t mention a valid software developer role

---

## 📬 Email Notifications (Optional)

If enabled, emails are sent when new posts are saved.

### Setup:
- Enable 2FA in Gmail
- Create an [App Password](https://myaccount.google.com/apppasswords)
- Add your email and password in `notifier.py`

---

## 📄 License

MIT License – use freely and modify as needed!

---

## 👋 Contributions Welcome

Feel free to fork, enhance, or submit a PR! This is an open-source tool designed to help job seekers stay ahead of new openings.