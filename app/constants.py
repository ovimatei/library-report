import os

PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOOK_PRICE_FILE_PATH = os.path.join(PROJECT_ROOT_PATH, "data", "book_price.csv")
DB_NAME = "library_report.db"
