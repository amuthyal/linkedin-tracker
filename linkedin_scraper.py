from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from time import sleep
import os
from dotenv import load_dotenv

load_dotenv()

def login_to_linkedin(driver):
    driver.get("https://www.linkedin.com/login")
    sleep(2)

    email_input = driver.find_element(By.ID, "username")
    password_input = driver.find_element(By.ID, "password")

    email_input.send_keys(os.getenv("LINKEDIN_EMAIL"))
    password_input.send_keys(os.getenv("LINKEDIN_PASSWORD"))
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    sleep(3)

def scrape_feed(driver, keywords):
    driver.get("https://www.linkedin.com/feed/")
    sleep(4)

    posts = driver.find_elements(By.CSS_SELECTOR, 'div.update-components-actor')
    results = []

    for post in posts:
        try:
            text_element = post.find_element(By.XPATH, ".//span[contains(@class,'update-components-text')]")
            text = text_element.text.lower()
            link = post.find_element(By.XPATH, ".//a[contains(@href,'/posts/')]").get_attribute("href")
            author = post.find_element(By.XPATH, ".//span[contains(@class,'feed-shared-actor__name')]").text

            if any(k.lower() in text for k in keywords):
                results.append({
                    "text": text,
                    "author": author,
                    "link": link
                })
        except Exception:
            continue
    return results
