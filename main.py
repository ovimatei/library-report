import csv
import enum
import datetime

from database import LibraryDatabase
from open_library_service import OpenLibraryService


class BookCategories(enum.Enum):
    RELATIONAL_DATABASES = "relational_databases"
    DATABASE_SOFTWARE = "database_software"
    PYTHON = "python"

    def __str__(self):
        return self.value


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


def update_description(db):
    book_ids = db.get_book_ids()
    service = OpenLibraryService()

    for book_id in book_ids:
        service.update_book_description(db, book_id)


if __name__ == "__main__":
    db = LibraryDatabase()
    db.db_cleanup()

    for category in BookCategories:
        service = OpenLibraryService(category)
        service.add_book_data_to_db(db)

    update_book_price(db)

    update_description(db)

    db.export_to_csv()

    db.conn.close()
