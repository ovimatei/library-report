import datetime
import enum

from app.database import Database
from app.helpers import update_book_data, upload_to_google_sheets
from app.openlibrary import OpenLibraryService

# ID of the target Google Spreadsheet
SPREADSHEET_ID = "12TDSBr797_EDzc0zM1SG7tLH_kkZqhfjugV1SA0xeN0"
DATABASE_NAME = "libraru_report.db"
CSV_FILE_PATH = "reports/library_report.csv"


class BookCategories(enum.Enum):
    RELATIONAL_DATABASES = "relational_databases"
    DATABASE_SOFTWARE = "database_software"
    PYTHON = "python"

    def __str__(self):
        return self.value


if __name__ == "__main__":
    db = Database(db_name=DATABASE_NAME)

    start = datetime.datetime.now()

    for category in BookCategories:
        service = OpenLibraryService(category)
        service.add_book_data_to_db(db)

    update_book_data(db)

    db.export_to_csv(CSV_FILE_PATH)

    upload_to_google_sheets(db, SPREADSHEET_ID)

    db.conn.close()
