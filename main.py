from linkedin_scraper import login_to_linkedin, scrape_feed
from google_sheets import connect_sheet, save_post
from notifier import send_email
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
import difflib
import re

# Set up error logging
logging.basicConfig(
    filename='error.log',
    level=logging.ERROR,
    format='%(asctime)s %(levelname)s:%(message)s'
)

def load_keywords():
    with open("keywords.txt") as f:
        return [line.strip() for line in f.readlines()]

# Filter out posts not related to hiring
skip_if_contains = [
    "my interview experience", "accepted to harvard", "gofundme", "donate",
    "poster exhibit", "capstone", "deep learning course", "vocalvision",
    "debugging my limits", "professor support", "fundraising", "meta interview",
    "travel guide", "student intern", "moving to seattle", "ask anything",
    "rewarding experience", "hirevue", "ai is deciding", "future of hiring",
    "what to bring", "living in seattle", "finding housing", "power point for your reference"
]

# Only allow these software-related job roles
target_roles = [
    "software engineer", "software developer", "sde", "sde i", "sde ii", "sde iii",
    "frontend developer", "front end developer", "full stack developer", "fullstack developer",
    "senior software engineer", "software development engineer"
]

def should_skip(text):
    return any(phrase in text for phrase in skip_if_contains)

def get_match(text, keywords, threshold=0.8):
    words = text.split()
    for kw in keywords:
        if kw in text:
            return kw, "exact"
        for word in words:
            ratio = difflib.SequenceMatcher(None, kw, word).ratio()
            if ratio >= threshold:
                return kw, f"fuzzy ({word}, {ratio:.2f})"
    return None, None

def matches_role(text, roles, threshold=0.8):
    words = text.lower().split()
    for role in roles:
        role_words = role.split()
        for i in range(len(words) - len(role_words) + 1):
            window = " ".join(words[i:i+len(role_words)])
            ratio = difflib.SequenceMatcher(None, role, window).ratio()
            if ratio >= threshold:
                return True
    return False

def extract_hashtags(text):
    return " ".join(re.findall(r"#\w+", text)) or "n/a"

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

        matched_kw, match_type = get_match(text, keywords)
        if matched_kw:
            if not matches_role(text, target_roles):
                print(f"❌ Skipping post — role not relevant:\n{text[:100]}")
                continue
            print(f"✔️ Match ({match_type}) for keyword '{matched_kw}' in post:", text[:100])
            post['matched_keyword'] = matched_kw
            post['hashtags'] = extract_hashtags(post['text'])
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
