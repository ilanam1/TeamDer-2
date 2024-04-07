from datetime import date

from django.test import TestCase, Client
from django.urls import reverse
from .models import custumeUser, friends
from django.test import TestCase, Client
from django.urls import reverse


class ProfileUpdateTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.test_user = custumeUser.objects.create(
            email='test@ac.sce.ac.il',
            first_name='Test',
            last_name='User',
            degree='BSc',
            birth_day=date(1990, 3, 3)
        )

        # Initialize the client
        self.client = Client()

        # Log in the test user by setting session
        session = self.client.session
        session['user_email'] = 'test@ac.sce.ac.il'
        session.save()

    def test_update_profile_with_valid_email(self):
        response = self.client.post(reverse('update_profile'), {
            'first_name': 'Test',
            'last_name': 'User',
            'degree': 'MSc',
            'email': 'updated@ac.sce.ac.il'  # Valid email

        })

        # Fetch the updated user from the database
        user = custumeUser.objects.get(email='updated@ac.sce.ac.il')

        # Check that the user's information has been updated
        self.assertEqual(user.degree, 'MSc')
        self.assertEqual(response.status_code, 302)  # Assuming redirect to '/profile/'


from django.test import TestCase, Client
from django.urls import reverse
from .models import custumeUser, friends
from django.shortcuts import redirect


class AcceptFriendRequestTestCase(TestCase):
    def setUp(self):
        # Create two users to simulate sending a friend request between them
        self.user1 = custumeUser.objects.create(
            email='user1@ac.sce.ac.il',
            first_name='Test',
            last_name='user1',
            degree='BSc',
            birth_day=date(1990, 3, 3)
        )

        self.user2 = custumeUser.objects.create(
            email='user2@ac.sce.ac.il',
            first_name='Test',
            last_name='user2',
            degree='BSc',
            birth_day=date(1999, 5, 8)
        )

        # Simulate a friend request from user1 to user2
        self.friend_request_sent = friends.objects.create(
            userName=self.user1.email,
            friend=self.user2,
            status="sent request"
        )
        # Simulate the reverse - a received request from user1 for user2
        self.friend_request_received = friends.objects.create(
            userName=self.user2.email,
            friend=self.user1,
            status="received request"
        )

        # Initialize the client
        self.client = Client()

        # Log in user2 by setting session
        session = self.client.session
        session['user_email'] = self.user2.email
        session.save()

    def test_accept_friend_request(self):
        # Simulate the POST request to accept the friend request from user1 to user2
        response = self.client.post(reverse('accept_request'), {'email': self.user1.email})

        # Verify the friend request statuses have been updated correctly
        updated_sent_request = friends.objects.get(userName=self.user1.email)
        self.assertEqual(updated_sent_request.status, "accepted")

        updated_received_request = friends.objects.get(userName=self.user2.email)
        self.assertEqual(updated_received_request.status, "accepted")

        # Check for successful redirect after accepting the friend request
        self.assertRedirects(response, '/friend_requests/')


from django.test import TestCase, Client
from django.urls import reverse
from .models import custumeUser, friends


class SendFriendRequestTestCase(TestCase):
    def setUp(self):
        # Create two users to simulate sending a friend request between them
        self.user_sending = custumeUser.objects.create(
            email='user1@ac.sce.ac.il',
            first_name='Test',
            last_name='user1',
            degree='BSc',
            birth_day=date(1990, 3, 3)
        )

        self.user_receiving = custumeUser.objects.create(
            email='user2@ac.sce.ac.il',
            first_name='Test',
            last_name='user2',
            degree='BSc',
            birth_day=date(1999, 5, 8)
        )


        # Initialize the client and log in the user sending the friend request
        self.client = Client()
        session = self.client.session
        session['user_email'] = self.user_sending.email
        session.save()

    def test_send_friend_request(self):
        # Simulate sending a friend request from user_sending to user_receiving
        response = self.client.post(reverse('send_friend_request'), {'email': self.user_receiving.email})

        # Verify the friend request has been correctly created with "sent request" status
        sent_request = friends.objects.filter(userName=self.user_sending.email, friend=self.user_receiving,
                                              status="sent request").exists()
        self.assertTrue(sent_request, "Friend request 'sent request' status not created")

        # Verify the corresponding friend request has been created with "received request" status
        received_request = friends.objects.filter(userName=self.user_receiving.email, friend=self.user_sending,
                                                  status="received request").exists()
        self.assertTrue(received_request, "Corresponding friend request 'received request' status not created")

        # Check for successful redirect after sending the friend request
        self.assertRedirects(response, '/userHomePage/')
