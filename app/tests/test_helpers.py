import unittest


class TestBookId(unittest.TestCase):
    payload = {
        "key": "/works/OL19897070W",
        "title": "Professional Oracle programming",
        "edition_count": 0,
        "cover_id": 8710482,
        "cover_edition_key": None,
        "subject": ["Relational databases", "Oracle (Computer file)"],
        "ia_collection": [""],
        "lendinglibrary": False,
        "printdisabled": False,
        "lending_edition": "",
        "lending_identifier": "",
        "authors": [{"key": "/authors/OL27732A", "name": "Rick Greenwald"}],
        "first_publish_year": None,
        "ia": None,
        "publi2c_scan": False,
        "has_fulltext": False,
    }

    def test_book_id(self):
        book_id = self.payload["key"].split("/")[-1]
        self.assertEqual(book_id, "OL19897070W")


class TestBookResponse(unittest.TestCase):
    book_response = {
        "title": "Reconfigurable Processor Array A Bit Sliced Parallel Computer (USA)",
        "covers": [8237007, 4979295],
        "first_sentence": {
            "type": "/type/text",
            "value": "Even a cursory glance at The Wall Street Journal reveals a bewildering collection of securities, markets, and financial institutions.",
        },
        "first_publish_date": "January 1, 1986",
        "key": "/works/OL2829091W",
        "authors": [
            {
                "type": {"key": "/type/author_role"},
                "author": {"key": "/authors/OL422557A"},
            }
        ],
        "excerpts": [
            {
                "excerpt": {
                    "type": "/type/text",
                    "value": "Even a cursory glance at The Wall Street Journal reveals a bewildering collection of securities, markets, and financial institutions.",
                },
                "page": "First sentence",
            }
        ],
        "type": {"key": "/type/work"},
        "description": "The main character of Fantastic Mr. Fox is an extremely clever anthropomorphized fox named Mr. Fox. He lives with his wife and four little foxes. In order to feed his family, he steals food from the cruel, brutish farmers named Boggis, Bunce, and Bean every night.\r\n\r\nFinally tired of being constantly outwitted by Mr. Fox, the farmers attempt to capture and kill him. The foxes escape in time by burrowing deep into the ground. The farmers decide to wait outside the hole for the foxes to emerge. Unable to leave the hole and steal food, Mr. Fox and his family begin to starve. Mr. Fox devises a plan to steal food from the farmers by tunneling into the ground and borrowing into the farmer's houses.\r\n\r\nAided by a friendly Badger, the animals bring the stolen food back and Mrs. Fox prepares a great celebratory banquet attended by the other starving animals and their families. Mr. Fox invites all the animals to live with him underground and says that he will provide food for them daily thanks to his underground passages. All the animals live happily and safely, while the farmers remain waiting outside in vain for Mr. Fox to show up.",
        "subjects": [
            "Industrial safety",
            "Management",
            "Macroeconomics",
            "Microeconomics",
            "Economics",
            "Database management",
            "DBase III plus (Computer file)",
            "Marketing",
            "Case studies",
            "Cases",
            "Collective labor agreements",
            "IBM Personal Computer",
            "Lotus 1-2-3 (Computer file)",
            "Programming",
            "PC-DOS (Computer file)",
            "WordPerfect (Computer file)",
            "Problems, exercises",
            "Business mathematics",
            "Economic conditions",
            "Managerial accounting",
            "Examinations, questions",
            "Corporations",
            "Finance",
            "Heat",
            "Transmission",
            "DBASE III plus (Computer file)",
            "Capital market",
            "Study and teaching",
            "Financial analysis",
        ],
        "latest_revision": 22,
        "revision": 22,
        "created": {"type": "/type/datetime", "value": "2009-12-10T00:32:12.342469"},
        "last_modified": {
            "type": "/type/datetime",
            "value": "2022-04-06T05:31:37.165083",
        },
    }

    def test_extract_excerpts(self):
        e = self.book_response["excerpts"]
        excerpts = "; ".join(excerpt["excerpt"]["value"] for excerpt in e)
        self.assertEqual(
            excerpts,
            "Even a cursory glance at The Wall Street Journal reveals a bewildering collection of securities, markets, and financial institutions.",
        )

    def test_author_key(self):
        authors = self.book_response["authors"]
        for author in authors:
            author_key = author["author"]["key"]
            print(author_key)


class TestCategoryBooksResponse(unittest.TestCase):
    category_books_response = {
        "key": "/subjects/python",
        "name": "python",
        "subject_type": "subject",
        "work_count": 95,
        "works": [
            {
                "key": "/works/OL2784125W",
                "title": "Learning Python",
                "edition_count": 20,
                "cover_id": 1312568,
                "cover_edition_key": "OL9497269M",
                "subject": [
                    "Python",
                    "Computer Science",
                ],
                "ia_collection": [
                    "americana",
                    "inlibrary",
                    "internetarchivebooks",
                    "librarygenesis",
                    "printdisabled",
                    "schroederlibrary-ol",
                ],
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
                "availability": {
                    "status": "borrow_available",
                    "available_to_browse": True,
                    "available_to_borrow": False,
                    "available_to_waitlist": False,
                    "is_printdisabled": True,
                    "is_readable": False,
                    "is_lendable": True,
                    "is_previewable": True,
                    "identifier": "learningpython00lutz",
                    "isbn": "1565924649",
                    "oclc": None,
                    "openlibrary_work": "OL2784132W",
                    "openlibrary_edition": "OL6804857M",
                    "last_loan_date": "2020-09-07T02:46:52Z",
                    "num_waitlist": "0",
                    "last_waitlist_date": "2020-08-26T12:48:18Z",
                    "is_restricted": True,
                    "is_browseable": True,
                    "__src__": "core.models.lending.get_availability",
                },
            },
        ],
    }

    def test_extract_book_fields(self):
        from app.openlibrary import extract_book_fields

        payload = self.category_books_response["works"][0]
        book_id, title, categories = extract_book_fields(payload)
        self.assertEqual(book_id, "OL2784125W")
        self.assertEqual(title, "Learning Python")
        self.assertEqual(categories, "Python; Computer Science")

    def test_get_total_books_number(self):
        from app.openlibrary import get_total_books

        self.assertEqual(get_total_books(self.category_books_response), 95)
