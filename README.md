
# 🧠 LinkedIn Job Post Tracker

A Python-based tool that scrapes your LinkedIn feed for hiring-related posts, filters them by software roles, and saves the results to Google Sheets. You also get email notifications for newly detected job posts.

---

## 🚀 Features

- ✅ Automatically logs into LinkedIn using secure `.env` credentials
- 🔍 Scrapes feed for posts containing hiring-related keywords
- 🎯 Filters for **software-related job roles** (e.g., SDE, Full Stack, Frontend)
- 🚫 Skips irrelevant or personal story posts (e.g., "my journey", "scholarship")
- 📄 Saves unique posts to a **Google Sheet**
- ✉️ Sends **email notifications** for new matches

---

## 📦 Tech Stack

- Python + Selenium (for scraping)
- Google Sheets API via `gspread`
- `.env` for credentials (via `python-dotenv`)
- Gmail or SMTP for email alerts (customizable)
- OpenAI API (optional) for summarization or enrichment

---

## ⚙️ Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/yourusername/linkedin-job-tracker.git
cd linkedin-job-tracker
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup `.env` File

```env
LINKEDIN_EMAIL=your_email@example.com
LINKEDIN_PASSWORD=your_linkedin_password
SENDER_EMAIL=your_email@gmail.com
SENDER_PASSWORD=your_app_password
RECEIVER_EMAIL=your_email@gmail.com
```

> ⚠️ Use an **app password** if using Gmail with 2FA enabled.

### 4. Setup Google Sheets

- Enable the **Google Sheets API** and download the `credentials.json` file from Google Cloud Console.
- Place it in the root directory.

### 5. Add Keywords

Edit the `keywords.txt` file to include hiring-related phrases (one per line).

```txt
we are hiring
we're hiring
my team is hiring
join our team
hiring now
software engineers wanted
```

---

## ▶️ Running the Tracker

```bash
python main.py
```

---

## 📊 Output Example (Google Sheet Columns)

| Timestamp           | Post Link                        | Text Sample          | Author         | Matched Keyword    | Hashtags     |
|---------------------|----------------------------------|----------------------|----------------|---------------------|--------------|
| 2025-04-23 14:52:03 | https://linkedin.com/...         | We're hiring a...    | John Doe       | we're hiring        | #hiring #tech|

---

## 📌 Disclaimer

> This tool is for **educational and personal use only**.  
> **LinkedIn’s Terms of Service prohibit automated scraping or login automation.**  
> Do not use this tool with professional or production accounts.  
> Respect privacy, platform integrity, and data usage policies.

---

## 💡 Future Improvements

- Add support for pagination and multi-page scraping
- Use GraphQL endpoints (if ever accessible via API)
- Enrich posts using OpenAI summarization
- Frontend dashboard for visualization

---

## 🧑‍💻 Author

Built with 💙 by [Akhila Muthyala](https://www.linkedin.com/in/akhila-muthyala-48b776209/)
