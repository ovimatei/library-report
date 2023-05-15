import enum

from database import LibraryDatabase
from helpers import update_book_price, update_description, upload_to_google_sheets
from open_library import OpenLibraryService

# ID of the target Google Spreadsheet
SPREADSHEET_ID = "12TDSBr797_EDzc0zM1SG7tLH_kkZqhfjugV1SA0xeN0"

CSV_FILE_PATH = "csv_reports/library_report.csv"


class BookCategories(enum.Enum):
    RELATIONAL_DATABASES = "relational_databases"
    DATABASE_SOFTWARE = "database_software"
    PYTHON = "python"

    def __str__(self):
        return self.value


if __name__ == "__main__":
    db = LibraryDatabase()

    for category in BookCategories:
        service = OpenLibraryService(category)
        service.add_book_data_to_db(db)

    update_book_price(db)

    update_description(db)

    db.export_to_csv(CSV_FILE_PATH)

    upload_to_google_sheets(db, SPREADSHEET_ID)

    db.conn.close()
