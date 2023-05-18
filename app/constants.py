import os

project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BOOK_PRICE_FILE_PATH = os.path.join(project_root_path, "data", "book_price.csv")
DB_NAME = "library_report.db"
