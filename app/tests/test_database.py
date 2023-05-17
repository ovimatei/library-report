import unittest


class TestDatabase(unittest.TestCase):
    def setUp(self):
        from app.database import Database

        db = Database(db_name="test.db")
        self.db = db

    def tearDown(self):
        self.db.db_cleanup()
        self.db.conn.close()

    def test_db_connection(self):
        self.assertIsNotNone(self.db.conn)

    def test_create_books_table(self):
        self.db.create_books_table()

    def test_db_cleanup(self):
        self.db.db_cleanup()

    def test_insert(self):
        data = {
            "book_id": "123",
            "title": "Test Book",
            "categories": "Test, Book",
            "author_names": "Test Author",
            "price": 10.0,
            "description": "Test description",
        }
        self.db.insert("books", data)
        assert self.db.get_by_book_id("books", "123") == (
            "123",
            "Test Book",
            "Test, Book",
            "Test Author",
            10.0,
            "Test description",
        )

    def test_update(self):
        data = {
            "book_id": "123",
            "title": "Test Book",
            "categories": "Test, Book",
            "author_names": "Test Author",
            "price": 10.0,
            "description": "Test description",
        }
        self.db.insert("books", data)
        self.db.update("books", "123", {"price": 20.0})
        assert self.db.get_by_book_id("books", "123") == (
            "123",
            "Test Book",
            "Test, Book",
            "Test Author",
            20.0,
            "Test description",
        )

    def test_get_by_book_id(self):
        data = {
            "book_id": "123",
            "title": "Test Book",
            "categories": "Test, Book",
            "author_names": "Test Author",
            "price": 10.0,
            "description": "Test description",
        }
        self.db.insert("books", data)
        assert self.db.get_by_book_id("books", "123") == (
            "123",
            "Test Book",
            "Test, Book",
            "Test Author",
            10.0,
            "Test description",
        )

    def test_get_book_ids(self):
        data = {
            "book_id": "123",
            "title": "Test Book",
            "categories": "Test, Book",
            "author_names": "Test Author",
            "price": 10.0,
            "description": "Test description",
        }
        self.db.insert("books", data)
        assert self.db.get_book_ids() == ["123"]

    def test_get_all_books(self):
        data = {
            "book_id": "123",
            "title": "Test Book",
            "categories": "Test, Book",
            "author_names": "Test Author",
            "price": 10.0,
            "description": "Test description",
        }
        self.db.insert("books", data)
        assert self.db.get_all_books() == [
            (
                "123",
                "Test Book",
                "Test, Book",
                "Test Author",
                10.0,
                "Test description",
            )
        ]
