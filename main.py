from linkedin_scraper import login_to_linkedin, scrape_feed
from google_sheets import connect_sheet, save_post
from notifier import send_email
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def load_keywords():
    with open("keywords.txt") as f:
        return [line.strip() for line in f.readlines()]

def main():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    login_to_linkedin(driver)

    keywords = load_keywords()
    posts = scrape_feed(driver, keywords)
    driver.quit()

    sheet = connect_sheet("LinkedIn Hiring Tracker")

    for post in posts:
        if save_post(sheet, post):
            send_email(post)
            print("✅ New post saved and notified.")
        else:
            print("🔁 Already exists, skipping.")

if __name__ == "__main__":
    main()
