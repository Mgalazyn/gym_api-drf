from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


CREATE_USER_URL = reverse('user:create')
# TOKEN_URL = reverse('user:token')


class ModelTests(TestCase):

    def test_create_user(self):
        email = 'test@example.com'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email(self):
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@EXAmple.com', 'Test2@example.com'],
        ]
        
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'test123')
            self.assertEqual(user.email, expected)

    def test_create_superuser(self):
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


#help func for creating user through API for testing
def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)


class PublicUser(TestCase):
    def set_up(self):
        self.client = APIClient()

    def test_creating_user_successful(self):
        credentials = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'test',
        }
        result = self.client.post(CREATE_USER_URL, credentials)

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

        user = get_user_model().objects.get(email=credentials['email'])
        self.assertTrue(user.check_password(credentials['password']))
        self.assertNotIn('password', result.data)

    def test_user_with_email(self):
        credentials = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'test',
        }

        create_user(**credentials)
        result = self.client.post(CREATE_USER_URL, credentials)

        #checking unique emails, if exist returns bad request
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_error(self):
        credentials = {
            'email': 'test@example.com',
            'password': 'test',
            'name': 'test',
        }

        result = self.client.post(CREATE_USER_URL, credentials)
        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)

        user_exist = get_user_model().objects.filter(
            email=credentials['email']
        ).exists()
        self.assertFalse(user_exist)

    # def test_creating_token_for_user(self):
    #     user_credentials = {
    #         'name': 'test',
    #         'email': 'test@example.com',
    #         'password': 'testpassword123',
    #     }

    #     create_user(**user_credentials)

    #     payload = {
    #         'email': user_credentials['email'],
    #         'password': user_credentials['password']
    #     }

    #     result = self.client.post(TOKEN_URL, payload)

    #     self.assertIn('token', result.data)
    #     self.assertEqual(result.status_code, status.HTTP_200_OK)

    # def test_creating_token_error(self):
    #     create_user(email='test@example.com', password='goodpasword123')

    #     payload = {'email':'test@example.com', 'password': 'badpassword'}
    #     result = self.client.post(TOKEN_URL, payload)

    #     self.assertNotIn('token', result.data)
    #     self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)
    
