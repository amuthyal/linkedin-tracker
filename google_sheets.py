import gspread
from oauth2client.service_account import ServiceAccountCredentials

def connect_sheet(sheet_name):
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet

def save_post(sheet, post):
    existing = sheet.col_values(1)
    if post['link'] not in existing:
        sheet.append_row([post['link'], post['text'], post['author']])
        return True
    return False
