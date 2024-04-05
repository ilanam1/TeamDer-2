from django.test import TestCase
import unittest
import createUser
from django.contrib.auth.models import User
from teamDer.models import User
from unittest.mock import MagicMock
import teamDer

class TestDeleteUser(unittest.TestCase):
    def setUp(self):
        self.user_email = "test@example.com"
#my code

    #בדיקת מחיקה תקינה
    def test_user_deleted(self):
        user = "topi2244@walla.co.il"
        self.assertTrue(teamDer.delete_user_by_email(user))

#copilot code

#בדיקת מחיקה תקינה
    def test_delete_user_valid_characters(self):
        result= teamDer.delete_user_by_email("topi2244@walla.co.il")
        self.assertTrue(result)

#בדיקת מחיקה עבור משתמש עם תווים מיוחדים
    def test_delete_user_special_characters(self):
        result= teamDer.delete_user_by_email("topi2&44@walla.co.il")
        self.assertFalse(result)

#בדיקת מחיקה למשתמש לא קיים
    def test_delete_user_nonexistent(self):
        result = teamDer.delete_user_by_email("topi22%44@walla.co.il")
        self.asserFalse(result)



if __name__ == '__main__':
    unittest.main()



