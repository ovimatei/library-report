import csv
import enum

from database import LibraryDatabase
from google_sheets import GoogleSheetsService
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


def upload_to_google_sheets(db):
    service = GoogleSheetsService()
    service.upload_data(SPREADSHEET_ID, db.get_all_books())


def read_book_price_csv():
    with open("csv_reports/book_price.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            yield row


def update_book_price(db):
    for row in read_book_price_csv():
        book_id, price, *_ = row
        if book_id == "Book ID":
            continue
        db.update(table_name="books", book_id=book_id, data={"price": price})


def update_description(db):
    book_ids = db.get_book_ids()
    service = OpenLibraryService()

    for book_id in book_ids:
        service.update_book_description(db, book_id)


if __name__ == "__main__":
    db = LibraryDatabase()

    for category in BookCategories:
        service = OpenLibraryService(category)
        service.add_book_data_to_db(db)

    update_book_price(db)

    update_description(db)

    db.export_to_csv(CSV_FILE_PATH)

    upload_to_google_sheets(db)

    db.conn.close()
