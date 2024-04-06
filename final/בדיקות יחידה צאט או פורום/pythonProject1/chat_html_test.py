import unittest
from app import app

class HtmlTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_html_structure(self):
        response = self.app.get('/')
        # וודא שהתגית <title> מכילה את השם "Chat Group"
        self.assertIn(b'<title>Chat Group</title>', response.data)
        # וודא קיום של תגיות הראשון והשני ברשימה
        self.assertIn(b'<h1>Chat Group</h1>', response.data)
        self.assertIn(b'<form class="message-form"', response.data)
        # וודא קיום של תגית ה-<ul> המכילה את המחרוזת "message-list"
        self.assertIn(b'<ul class="message-list">', response.data)
        # וודא קיום של תגית ה-<h2> המכילה את המחרוזת "participants"
        self.assertIn(b'<h2 class="participants">', response.data)



if __name__ == '__main__':
    unittest.main()
