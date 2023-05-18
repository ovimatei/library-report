import unittest


class TestHelpers(unittest.TestCase):
    book_payload = {
        "title": "Fantastic Mr Fox",
        "key": "/works/OL45804W",
        "authors": ["test author"],
        "type": {"key": "/type/work"},
        "description": "Test description string",
        "covers": [],
        "subject_places": [],
        "subjects": ["test", "book"],
        "subject_people": [],
        "subject_times": [],
        "location": "/works/OL45883W",
        "latest_revision": 14,
        "revision": 14,
        "created": {},
        "last_modified": {},
    }

    book_payload2 = book_payload.copy()
    book_payload2["description"] = {
        "value": "Test description string",
        "type": "/type/text",
    }

    book_category_payload = {
        "key": "/works/OL2784125W",
        "title": "Learning Python",
        "edition_count": 20,
        "cover_id": 1312568,
        "cover_edition_key": "OL9497269M",
        "subject": [
            "Python",
            "Computer Science",
        ],
        "ia_collection": [],
        "lendinglibrary": False,
        "printdisabled": True,
        "lending_edition": "OL6804857M",
        "lending_identifier": "learningpython00lutz",
        "authors": [
            {"key": "/authors/OL411267A", "name": "Mark Lutz"},
            {"key": "/authors/OL2726848A", "name": "David Ascher"},
        ],
        "first_publish_year": 1999,
        "ia": "learningpython00lutz",
        "public_scan": False,
        "has_fulltext": True,
        "availability": {},
    }

    book_payload_with_excerpt = book_payload.copy()
    del book_payload_with_excerpt["description"]
    book_payload_with_excerpt["excerpts"] = [
        {
            "excerpt": {
                "value": "Test excerpt string",
                "type": "/type/text",
            },
        }
    ]

    def setUp(self) -> None:
        from app.database import Database

        self.db = Database(db_name="test.db")
        self.db.insert(
            "books",
            {
                "book_id": "123",
                "title": "Test Book",
                "categories": "Test, Book",
                "author_names": "Test Author",
                "price": 10.0,
                "description": "Test description",
            },
        )

    def tearDown(self) -> None:
        self.db.db_cleanup()
        self.db.conn.close()

    def test_read_book_price_csv(self):
        from app.helpers import read_book_price_csv

        book_price_csv = read_book_price_csv()
        self.assertEqual(next(book_price_csv), ["Book ID", "Price"])

    def test_update_book_price(self):
        from app.helpers import update_book_price

        update_book_price(self.db)
        self.assertEqual(self.db.get_by_book_id("books", "123")[4], 10.0)

    def test_get_book_description(self):
        from app.openlibrary import get_book_description

        description = get_book_description(response=self.book_payload)
        self.assertEqual(description, "Test description string")

    def test_get_book_description2(self):
        from app.openlibrary import get_book_description

        description = get_book_description(response=self.book_payload2)
        self.assertEqual(description, "Test description string")

    def test_get_book_description_with_excerpt(self):
        from app.openlibrary import get_book_description

        description = get_book_description(response=self.book_payload_with_excerpt)
        self.assertEqual(description, "Test excerpt string")

    def test_get_book_description_with_no_description(self):
        from app.openlibrary import get_book_description

        self.book_payload["description"] = None
        description = get_book_description(response=self.book_payload)
        self.assertEqual(description, None)

    def test_extract_book_fields(self):
        from app.openlibrary import extract_book_fields

        book_fields = extract_book_fields(book=self.book_category_payload)
        self.assertEqual(
            book_fields,
            ("OL2784125W", "Learning Python", "Python; Computer Science"),
        )

    def test_extract_book_fields_with_no_subjects(self):
        from app.openlibrary import extract_book_fields

        self.book_category_payload["subject"] = []
        book_fields = extract_book_fields(book=self.book_category_payload)
        self.assertEqual(
            book_fields,
            ("OL2784125W", "Learning Python", ""),
        )
