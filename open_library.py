import logging
import sqlite3
import time

import requests

logger = logging.getLogger(__name__)


def extract_book_fields(book):
    book_id = book["key"].split("/")[-1]
    title = book["title"]
    categories = "; ".join(subject for subject in book["subject"])
    author_names = "; ".join(author["name"] for author in book["authors"])

    return book_id, title, categories, author_names


class OpenLibraryService:
    OPEN_LIBRARY_API = "https://openlibrary.org"
    LIMIT = 50
    OFFSET = 0

    def __init__(self, category=None):
        self.category = category

    def get_total_books(self):
        response = requests.get(
            f"{self.OPEN_LIBRARY_API}/subjects/{self.category}.json"
        )
        response.raise_for_status()
        try:
            total_books = response.json()["work_count"]
        except KeyError:
            raise KeyError("work_count not found")
        return total_books

    def add_book_data_to_db(self, db):
        if not self.category:
            raise ValueError("Category is required")

        total_books = self.get_total_books()

        print(f"Found {total_books} books for category {self.category}")
        print(f"Adding books to database...")

        count = 0
        while self.OFFSET < total_books:
            response = requests.get(
                f"{self.OPEN_LIBRARY_API}/subjects/{self.category}.json?limit={self.LIMIT}&offset={self.OFFSET}"
            )

            response.raise_for_status()
            books_json = response.json()["works"]
            for book in books_json:
                book_id, title, categories, author_names = extract_book_fields(book)
                try:
                    db.insert(
                        table_name="books",
                        data={
                            "book_id": book_id,
                            "title": title,
                            "categories": categories,
                            "author_names": author_names,
                        },
                    )
                    print(f"Added book with id {book_id}")
                    count += 1

                except sqlite3.IntegrityError:
                    logger.warning(
                        f"Book with id {book_id} already exists, skipping..."
                    )

            self.OFFSET += self.LIMIT

        print(f"Added {count} books for category {self.category}")

    def get_book_response(self, book_id):
        max_retries = 3
        retries = 0

        while retries < max_retries:
            try:
                response = requests.get(f"{self.OPEN_LIBRARY_API}/books/{book_id}.json")
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logger.warning(
                    f"Error while getting book with id {book_id}, error: {e}, retrying..."
                )
                retries += 1
            else:
                return response.json()

            time.sleep(1)

        logger.error(f"Error while getting book with id {book_id}")

        return {}

    def update_book_description(self, db, book_id):
        response = self.get_book_response(book_id)

        description = response.get("description", "")
        excerpts = response.get("excerpts", "")

        if description:
            if isinstance(description, dict):
                description = description["value"]

        if excerpts:
            excerpts = "; ".join(excerpt["excerpt"]["value"] for excerpt in excerpts)
            print(f"Found excerpts for book with id {book_id}")

            description = excerpts

        if not description:
            print(f"Book with id {book_id} has no description or excerpts")
            return

        db.update(
            table_name="books",
            book_id=book_id,
            data={"description": description},
        )

        print(f"Updated description for book with id {book_id}")
