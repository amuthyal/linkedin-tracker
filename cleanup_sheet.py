import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Phrases that identify false positives
skip_if_contains = [
    "my interview experience", "accepted to harvard", "gofundme", "donate",
    "poster exhibit", "capstone", "deep learning course", "vocalvision",
    "debugging my limits", "professor support", "fundraising", "meta interview",
    "travel guide", "student intern", "moving to seattle", "ask anything",
    "rewarding experience", "hirevue", "ai is deciding", "future of hiring"
]

def connect_sheet(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    return client.open(sheet_name).sheet1

def clean_false_positives(sheet):
    rows = sheet.get_all_values()
    headers = rows[0]
    data = rows[1:]

    print(f"📊 Checking {len(data)} rows...")

    # Keep only rows that don't contain skip phrases
    cleaned = [row for row in data if not any(skip in row[2].lower() for skip in skip_if_contains)]

    # Clear and rewrite sheet
    sheet.clear()
    sheet.append_row(headers)
    for row in cleaned:
        sheet.append_row(row)

    print(f"✅ Removed {len(data) - len(cleaned)} false positives. {len(cleaned)} rows remain.")

if __name__ == "__main__":
    sheet = connect_sheet("LinkedIn Hiring Tracker")
    clean_false_positives(sheet)
