import unittest
import password

class TestPasswordValidation(unittest.TestCase):

    def test_1_password(self):
        self.assertTrue(password.check_password("Test123!")) #return true,this password is a legal

    def test_short_password(self):
        """
        Test that the function returns False for a password less than 8 characters.
        """
        password1 = "short"
        self.assertFalse(password.check_password(password1))

    def test_missing_uppercase(self):
        """
        Test that the function returns False for a password without an uppercase letter.
        """
        password1 = "password123!"
        self.assertFalse(password.check_password(password1))

    def test_valid_password(self):
        """
        Test that the function returns True for a password meeting all criteria.
        """
        password1 = "StrongPassword123!"
        self.assertTrue(password.check_password(password1))

    if __name__ == '__main__':
        unittest.main()
