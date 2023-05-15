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
