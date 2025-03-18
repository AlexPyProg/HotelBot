import asyncio
import re

import gspread
from google.oauth2.service_account import Credentials


SHEET_ID = "1npdLrlNTBeadyxa48hbT0vEi4Qs2V_QCj6w5mU7EzpI"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
CREDS_FILE = r"C:\Users\Александр\PycharmProjects\RegistryBot\app\google\creds.json"

creds = Credentials.from_service_account_file(CREDS_FILE, scopes=SCOPES)
client = gspread.authorize(creds)


def get_row(sheet_name):
    sheet = client.open_by_key(SHEET_ID).worksheet(sheet_name)
    data = sheet.get_all_values()
    data = data[2:]
    all_links = []
    captions = []
    for row in data:
        links = []
        try:
            captions.append(row[0])
            for link in row[1:]:
                if link.startswith('https://drive.google.com/file/d/'):
                    link = transform_google_drive_link(link)
                    links.append(link)
            if links:
                all_links.append(links)
        except IndexError:
            print('Нет данных')
    return captions, all_links


def transform_google_drive_link(link: str) -> str:
    """Преобразует обычную ссылку Google Диска в прямую ссылку для скачивания."""
    match = re.search(r"https://drive\.google\.com/file/d/([^/]+)/view", link)
    if match:
        file_id = match.group(1)
        return f"https://drive.google.com/uc?export=download&id={file_id}"
    return link

# sheet_names = [sheet.title for sheet in client.open_by_key(SHEET_ID).worksheets()]
# print("Список листов в таблице:", sheet_names)
# captions, all_links = get_row('Юсуповский сад')
# print("Captions:", captions)
# print("All links:", all_links)
