import os

import dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build

dotenv.load_dotenv(".env")


class GoogleSheetsService:
    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_info(
            info={
                "type": "service_account",
                "client_email": os.getenv("CLIENT_EMAIL"),
                "private_key": os.getenv("PRIVATE_KEY").replace("\\n", "\n"),
                "token_uri": "https://oauth2.googleapis.com/token",
            },
            scopes=["https://www.googleapis.com/auth/spreadsheets"],
        )
        self.service = build("sheets", "v4", credentials=self.credentials)

    def upload_data(self, spreadsheet_id, rows):
        request = (
            self.service.spreadsheets()
            .values()
            .append(
                spreadsheetId=spreadsheet_id,
                range="Sheet1",
                valueInputOption="USER_ENTERED",
                body={"values": rows},
            )
        )
        try:
            response = request.execute()
            print(response)
        except Exception as e:
            print(e)
            raise e
