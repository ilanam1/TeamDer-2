import unittest
from app import app
import os
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

    def test_send_message_with_image(self):
        # בודק אם הודעה ותמונה נשלחות לשרת ומקבלות תגובה תקינה
        # יצירת תמונת קובץ זמנית
        with open('test_image.jpg', 'wb') as f:
            f.write(b'fake_image_data')
        # שליחת בקשת POST עם הודעה ותמונה
        with open('test_image.jpg', 'rb') as f:
            response = self.app.post('/send', data={'username': 'test_user', 'message': 'Hello, world!', 'file': f})
        # בדיקת תגובה מהשרת
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Message sent successfully')
        # מחיקת התמונה לאחר הבדיקה
        os.remove('test_image.jpg')

    def test_upload_file(self):
        # בדיקה שהשרת מקבל קובץ מצורף מהמשתמש ושומר אותו בתיקיית ההעלאות
        with open('test_file.txt', 'w') as f:
            f.write('Test file content')
        with open('test_file.txt', 'rb') as f:
            response = self.app.post('/send', data={'username': 'test_user', 'message': 'File upload test', 'file': f})
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
