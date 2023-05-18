import sqlite3

import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from app.logger import logger


def extract_book_fields(book):
    book_id = book["key"].split("/")[-1]
    title = book["title"]
    categories = "; ".join(subject for subject in book["subject"])

    return book_id, title, categories


def get_total_books(category_book_response):
    try:
        total_books = category_book_response["work_count"]
    except KeyError:
        raise KeyError("work_count not found")
    return total_books


def get_book_description(response):
    description = response.get("description", None)
    excerpts = response.get("excerpts", None)

    if description:
        if isinstance(description, dict):
            description = description["value"]

    if excerpts:
        excerpts = "; ".join(excerpt["excerpt"]["value"] for excerpt in excerpts)

        description = excerpts if not description else f"{description}; {excerpts}"

    return description


class OpenLibraryService:
    OPEN_LIBRARY_API = "https://openlibrary.org"
    LIMIT = 50
    OFFSET = 0
    MAX_RETRIES = 3
    status_forcelist = [500, 502, 503, 504]

    def __init__(self, category=None):
        self.category = category
        self.session = requests.Session()
        self.adapter = HTTPAdapter(
            max_retries=Retry(
                total=self.MAX_RETRIES,
                backoff_factor=1,
                status_forcelist=self.status_forcelist,
            )
        )
        self.session.mount(self.OPEN_LIBRARY_API, self.adapter)

    def add_book_data_to_db(self, db):
        if not self.category:
            raise ValueError("Category is required")

        category_books_response = self.session.get(
            f"{self.OPEN_LIBRARY_API}/subjects/{self.category}.json"
        )

        total_books = get_total_books(category_books_response.json())

        logger.info(f"Found {total_books} books for category {self.category}")
        logger.info(f"Adding books to database...")

        count = 0
        while self.OFFSET < total_books:
            response = self.session.get(
                f"{self.OPEN_LIBRARY_API}/subjects/{self.category}.json",
                params={"limit": self.LIMIT, "offset": self.OFFSET},
            )

            response.raise_for_status()

            books_json = response.json()["works"]
            for book in books_json:
                book_id, title, categories = extract_book_fields(book)
                try:
                    db.insert(
                        table_name="books",
                        data={
                            "book_id": book_id,
                            "title": title,
                            "categories": categories,
                        },
                    )
                    logger.info(f"Added book with id {book_id}")
                    count += 1

                except sqlite3.IntegrityError:
                    logger.warning(
                        f"Book with id {book_id} already exists, skipping..."
                    )

            self.OFFSET += self.LIMIT

        logger.info(f"Added {count} books for category {self.category}")

    def get_book_response(self, book_id):
        response = self.session.get(f"{self.OPEN_LIBRARY_API}/works/{book_id}.json")
        response.raise_for_status()
        return response.json()

    def get_book_author_names(self, response):
        authors = response.get("authors", None)
        author_names = []
        if authors:
            for author in authors:
                try:
                    author_key = author["author"]["key"]
                except KeyError:
                    try:
                        author_key = author["key"]
                    except KeyError:
                        raise KeyError("author key not found")

                author_response = self.session.get(
                    f"{self.OPEN_LIBRARY_API}{author_key}.json"
                )
                author_response.raise_for_status()
                author_names.append(author_response.json()["name"])

        return "; ".join(author_names)

    def update_book(self, db, book_id):
        response = self.get_book_response(book_id)
        description = get_book_description(response)
        author_names = self.get_book_author_names(response)

        data = {"author_names": author_names}
        if description:
            data["description"] = description

        db.update(
            table_name="books",
            book_id=book_id,
            data=data,
        )
        logger.info(
            f"Updated book with id {book_id}, description: {description}, author_names: {author_names}"
        )
