import csv

from app.google_sheets import GoogleSheetsService
from app.openlibrary import OpenLibraryService


def upload_to_google_sheets(db, spreadsheet_id):
    service = GoogleSheetsService()
    headers = ["Book ID", "Title", "Categories", "Author Names", "Price", "Description"]
    rows = [headers] + db.get_all_books()
    service.upload_data(spreadsheet_id, rows)


def read_book_price_csv():
    with open("book_price.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            yield row


def update_book_price(db):
    for row in read_book_price_csv():
        book_id, price, *_ = row
        if book_id == "Book ID":
            continue
        db.update(table_name="books", book_id=book_id, data={"price": price})


def update_book_data(db):
    update_book_price(db)
    book_ids = db.get_book_ids()
    service = OpenLibraryService()

    for book_id in book_ids:
        service.update_book(db, book_id)
