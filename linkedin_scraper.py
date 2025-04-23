from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

def login_to_linkedin(driver):
    driver.get("https://www.linkedin.com/login")
    sleep(3)

    driver.find_element(By.ID, "username").send_keys(os.getenv("LINKEDIN_EMAIL"))
    driver.find_element(By.ID, "password").send_keys(os.getenv("LINKEDIN_PASSWORD"))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    sleep(5)

def scrape_feed(driver, keywords):
    driver.get("https://www.linkedin.com/feed/")
    sleep(5)

    SCROLL_PAUSE_TIME = 3
    last_height = driver.execute_script("return document.body.scrollHeight")

    for _ in range(5):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    posts_data = []
    posts = driver.find_elements(By.CSS_SELECTOR, "div.feed-shared-update-v2")
    print(f"🔎 Found {len(posts)} total feed items...")

    for post in posts:
        try:
            # Extract multiple span blocks for content
            span_elements = post.find_elements(By.XPATH, ".//span[contains(@class, 'break-words') or contains(@dir, 'ltr')]")
            all_text = " ".join([elem.text.strip() for elem in span_elements if elem.text.strip()])

            if not all_text:
                print("⚠️ No text extracted from this post.")
                continue

            text = all_text.lower()

            # Extract author (fallback: Unknown)
            try:
                author_elem = post.find_element(By.XPATH, ".//span[contains(@class, 'update-components-actor__name') or contains(@class, 'feed-shared-actor__name')]")
                author = author_elem.text.strip()
            except:
                author = "Unknown"

            # Extract or generate unique link
            try:
                post_links = post.find_elements(By.XPATH, ".//a[contains(@href, '/posts/')]")
                link = post_links[0].get_attribute("href") if post_links else None
                if not link:
                    raise Exception("No post link found")
            except:
                # Generate pseudo-unique fallback link
                link = f"https://linkedin.com/post-fallback-{hash(text) % 1000000}"

            print("📝 Extracted post preview:", text[:100])

            posts_data.append({
                "text": text,
                "author": author,
                "link": link
            })

        except Exception as e:
            print("⚠️ Post skipped due to unexpected error:", e)
            continue

    print(f"🔎 Found {len(posts_data)} total post(s) scraped from feed.")
    return posts_data
