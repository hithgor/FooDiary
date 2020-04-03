from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.contrib import auth

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
LOGIN_USER_URL = reverse('user:login')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    """Test creating user (public)"""

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': 'test@dctest.com',
            'password': 'testpass',
        }

    def test_create_user_no_email(self):
        pass


    def test_create_valid_user_success(self):
        """Creating user with valid payload is successful"""
        res = self.client.post(CREATE_USER_URL, self.payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=self.payload['email'])
        self.assertTrue(user.check_password(self.payload['password']))
        self.assertNotIn('password', res)

    def test_create_existing_user(self):
        """Test creating a user that already exists fails"""
        create_user(**self.payload)
        res = self.client.post(CREATE_USER_URL, self.payload)
        userList = get_user_model().objects.filter(email=self.payload['email'])

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(len(userList), 1)

    def test_created_user_needs_activation(self):
        """Test user is_active value equals False after registration"""
        create_user(**self.payload)
        user = get_user_model().objects.get(email=self.payload['email'])

        self.assertFalse(user.is_active)


    def test_created_user_cannot_login(self):
        """Test user with is_active=False cannot log-in"""
        create_user(**self.payload)
        res = self.client.post(LOGIN_USER_URL, self.payload)
        user = get_user_model().objects.get(email=self.payload['email'])
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateUserApiTests(TestCase):
    """TEST API requests that require authentication"""


