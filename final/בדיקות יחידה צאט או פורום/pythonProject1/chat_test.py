import unittest
from app import app

class FlaskChatTestCase(unittest.TestCase):

    def setUp(self):
        # יצירת לקוח טסט עבור האפליקציה והגדרת סביבת טסט
        self.app = app.test_client()
        self.app.testing = True


    def test_index_page(self):
        # בודק אם הדף הראשי של האפליקציה נגיש ומכיל את הטקסט " Chat Group"
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Chat Group', response.data)

    def test_send_message(self):
        # בודק אם הודעה נשלחת לשרת ומקבלת תגובה תקינה עם פרטי ההודעה
        response = self.app.post('/send', data={'username': 'test_user', 'message': 'Hello, world!'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'"message": "Hello, world!"', response.data)

    def test_upload_file(self):
        # בדיקה שהשרת מקבל קובץ מצורף מהמשתמש ושומר אותו בתיקיית ההעלאות
        with open('test_file.txt', 'w') as f:
            f.write('Test file content')
        with open('test_file.txt', 'rb') as f:
            response = self.app.post('/send', data={'username': 'test_user', 'message': 'File upload test', 'file': f})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
