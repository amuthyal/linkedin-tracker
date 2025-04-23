import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

def connect_sheet(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet

def generate_fingerprint(post):
    text_sample = post['text'][:150].strip().lower().replace('\n', ' ')
    return f"{post['author'].strip().lower()}|{text_sample}"

def save_post(sheet, post):
    fingerprint = generate_fingerprint(post)

    existing_rows = sheet.get_all_values()[1:]  # Skip header row
    existing_fingerprints = [
        f"{row[3].strip().lower()}|{row[2][:150].strip().lower().replace(chr(10), ' ')}"
        for row in existing_rows if len(row) >= 4
    ]

    if fingerprint not in existing_fingerprints:
        matched_kw = post.get('matched_keyword', 'n/a')
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([timestamp, post['link'], post['text'], post['author'], matched_kw])
        return True
    return False
