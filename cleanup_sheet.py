import gspread
from oauth2client.service_account import ServiceAccountCredentials
import difflib

# Phrases that identify false positives
skip_if_contains = [
    "my interview experience", "accepted to harvard", "gofundme", "donate",
    "poster exhibit", "capstone", "deep learning course", "vocalvision",
    "debugging my limits", "professor support", "fundraising", "meta interview",
    "travel guide", "student intern", "moving to seattle", "ask anything",
    "rewarding experience", "hirevue", "ai is deciding", "future of hiring"
]

# Only allow these software-related job roles
target_roles = [
    "software engineer", "software developer", "sde", "sde i", "sde ii", "sde iii",
    "frontend developer", "front end developer", "full stack developer", "fullstack developer",
    "senior software engineer", "software development engineer"
]

def connect_sheet(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

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

def clean_sheet(sheet):
    rows = sheet.get_all_values()
    headers = rows[0]
    data = rows[1:]

    print(f"📊 Scanning {len(data)} rows...")

    cleaned = []
    for row in data:
        text = row[2].lower()  # assuming column 2 is post text
        if any(skip in text for skip in skip_if_contains):
            continue
        if not matches_role(text, target_roles):
            continue
        cleaned.append(row)

    # Clear and rewrite sheet
    sheet.clear()
    sheet.append_row(headers)
    for row in cleaned:
        sheet.append_row(row)

    print(f"✅ Cleaned sheet: {len(data) - len(cleaned)} removed, {len(cleaned)} remain.")

if __name__ == "__main__":
    sheet = connect_sheet("LinkedIn Hiring Tracker")
    clean_sheet(sheet)
