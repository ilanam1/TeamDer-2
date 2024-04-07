from django.test import TestCase, Client
from django.urls import reverse
from .models import custumeUser
import unittest

class ViewsTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user_data = {
            'first_name': 'אילן',
            'last_name': 'אמוייב',
            'gender': 'זכר',
            'degree': 'software',
            'birth_date': '2002-10-23',
            'email': 'ilan@ac.sce.ac.il',
            'password': '12345678iA@',
            'passwordAgain': '12345678iA@',
            'summary': 'hello'
        }

    def test_home_view(self):
        response = self.client.get(reverse('Home'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.post(reverse('register'), self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirects after successful registration

    def test_login_view(self):
        response = self.client.post(reverse('login'), self.user_data)
        self.assertEqual(response.status_code, 302)  # Redirects after successful login

    def test_dikant_page_view(self):
        response = self.client.get(reverse('dikanatPage'))
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects after logout

    def test_invalid_user_login(self):
        invalid_user_data = {
            'email': 'invalid@example.com',
            'password': 'InvalidPassword123'
        }
        response = self.client.post(reverse('login'), invalid_user_data)
        self.assertContains(response, 'המשתמש אינו קיים במערכת')  # Assert error message



