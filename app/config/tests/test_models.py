from django.test import TestCase
from django.contrib.auth import get_user_model


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