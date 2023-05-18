import csv
import sqlite3

from app.constants import DB_NAME
from app.openlibrary import logger


class Database:
    def __init__(self, db_name=DB_NAME):
        self.conn = sqlite3.connect(db_name)
        self.c = self.conn.cursor()
        self.create_books_table()

    def create_books_table(self):
        logger.info("Creating books table if not exists...")

        self.execute_query(
            """CREATE TABLE IF NOT EXISTS books (
                book_id VARCHAR(250) PRIMARY KEY NOT NULL,
                title VARCHAR(250) NOT NULL,
                categories TEXT,
                author_names TEXT,
                price FLOAT,
                description TEXT
                )"""
        )

    def db_cleanup(self):
        logger.info("Cleaning up database...")
        self.execute_query("DROP TABLE IF EXISTS books")
        logger.info("Creating books table...")
        self.create_books_table()

    def execute_query(self, query, params=None):
        if params:
            self.c.execute(query, params)
        else:
            self.c.execute(query)
        self.conn.commit()

    def insert(self, table_name, data):
        keys = ", ".join(data.keys())
        values = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"
        self.execute_query(query, tuple(data.values()))

    def update(self, table_name, book_id, data):
        keys = ", ".join([f"{key} = ?" for key in data.keys()])
        query = f"UPDATE {table_name} SET {keys} WHERE book_id=?"
        self.execute_query(query, tuple(data.values()) + (book_id,))

    def get_by_book_id(self, table_name, book_id):
        query = f"SELECT * FROM {table_name} WHERE book_id=?"
        self.execute_query(query, (book_id,))
        return self.c.fetchone()

    def get_book_ids(self):
        query = f"SELECT book_id FROM books"
        self.execute_query(query)
        return [x[0] for x in self.c.fetchall()]

    def get_all_books(self):
        query = f"SELECT * FROM books"
        self.execute_query(query)
        return self.c.fetchall()

    def export_to_csv(self, filename="library_report.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "book_id",
                    "title",
                    "categories",
                    "author_names",
                    "price",
                    "description",
                ]
            )
            writer.writerows(self.get_all_books())
        logger.info(f"Exported data to {filename}")
