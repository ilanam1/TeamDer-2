from django.test import TestCase
import unittest
import createUser
from django.contrib.auth.models import User
from .models import User
from .createUser import createNewUser

from unittest.mock import MagicMock



class UserTests(TestCase):

    #בדיקת היחידה שאני יצרתי-בודקת האם המשתמש קיים בבסיס הנתונים
    def test_user_exists(self):
        user = createNewUser("אילן","אמוייב","זכר","הנדסת תוכנה","2002-10-23","ilanam1@ac.sce.ac.il","213208671iA.")
        self.assertTrue(User.objects.filter(email=user.email).exists())

    #שלוש בדיקות היחידה שהבינה המלאכותית יצרה
    def test_createNewUser_returns_user_with_correct_details(self):
        # Arrange
        Fn = "John"
        Ln = "Doe"
        g = "Male"
        d = "BSc"
        date = "1990-01-01"
        em = "john.doe@example.com"
        passW = "password123"

        # Act
        user = createNewUser(Fn, Ln, g, d, date, em, passW)

        # Assert
        assert user.first_name == Fn
        assert user.last_name == Ln
        assert user.gender == g


    def test_createNewUser_calls_User_objects_create(self):
        # Arrange
        Fn = "John"
        Ln = "Doe"
        g = "Male"
        d = "BSc"
        date = "1990-01-01"
        em = "john.doe@example.com"
        passW = "password123"

        mock_user_create = MagicMock()
        User.objects.create = mock_user_create

        # Act
        createNewUser(Fn, Ln, g, d, date, em, passW)

        # Assert
        mock_user_create.assert_called_once_with(
            first_name=Fn,
            last_name=Ln,
            gender=g,
            degree=d,
            birth_date=date,
            email=em,
            password=passW
        )

    def test_createNewUser_with_valid_values(self):
        # Arrange
        Fn = "John"
        Ln = "Doe"
        g = "Male"
        d = "BSc"
        date = "1990-01-01"
        em = "john.doe@example.com"
        passW = "password123"

        # Act
        user = createNewUser(Fn, Ln, g, d, date, em, passW)

        # Assert
        assert user is not None



if __name__=='__main__':
    unittest.main()
