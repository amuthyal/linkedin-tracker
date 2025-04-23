from linkedin_scraper import login_to_linkedin, scrape_feed
from google_sheets import connect_sheet, save_post
from notifier import send_email
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging

# Set up error logging
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s:%(message)s'
)

def load_keywords():
    with open("keywords.txt") as f:
        return [line.strip() for line in f.readlines()]

# Expanded filtering for non-hiring posts
skip_if_contains = [
    "my interview experience",
    "accepted to harvard",
    "my story",
    "debugging my limits",
    "gofundme",
    "donate",
    "grateful for the opportunity",
    "scholarship",
    "financial aid",
    "got cut from my job",
    "meta interview",
    "fundraising",
    "my journey",
    "ask anything",
    "internship roommate",
    "roomie",
    "things to do in",
    "moving to seattle",
    "student intern tips",
    "places to eat",
    "travel guide",
    "power point for your reference",
    "what to bring",
    "living in seattle",
    "finding housing",
    "future of hiring",
    "death of opportunity",
    "hirevue",
    "fair ai",
    "ai is deciding",
    "invisible gatekeepers",
    "ai and hiring bias",
    "scored people based on",
    "voice and facial movements",
    "accent-based rejection",
    "poster exhibit",
    "presented my project",
    "deep learning course",
    "vocalvision",
    "this project is close to my heart",
    "academic project",
    "image captioning model",
    "professor support",
    "rewarding experience",
    "coursework",
    "final year project",
    "capstone"


]

def should_skip(text):
    return any(phrase in text for phrase in skip_if_contains)

def get_match(text, keywords):
    for kw in keywords:
        if kw in text:
            return kw
    return None

def main():
    print("\n🚀 Starting LinkedIn Tracker...")

    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    login_to_linkedin(driver)
    print("✅ Logged into LinkedIn.")

    keywords = load_keywords()
    print("🔍 Loaded keywords:", keywords)

    posts = scrape_feed(driver, keywords)
    driver.quit()

    print(f"🔎 Found {len(posts)} total post(s) scraped from feed.")

    matched_posts = []
    for post in posts:
        text = post['text'].lower()
        if should_skip(text):
            print("🚫 Skipping post — flagged as non-hiring content.")
            continue

        matched_kw = get_match(text, keywords)
        if matched_kw:
            print(f"✔️ Match found for keyword '{matched_kw}' in post:", text[:100])
            post['matched_keyword'] = matched_kw
            matched_posts.append(post)

    print(f"📄 Found {len(matched_posts)} post(s) matching keywords.")

    sheet = connect_sheet("LinkedIn Hiring Tracker")

    for post in matched_posts:
        print("👉 Checking post:", post['link'])
        if save_post(sheet, post):
            print("✅ New post saved.")
            send_email(post)
        else:
            print("🔁 Already in sheet – skipping.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logging.error("Script failed", exc_info=True)
        print("❌ Something went wrong. Check error.log.")
