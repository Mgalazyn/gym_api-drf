from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from api.serializers import UserSerializer
from unittest.mock import patch
from api import models
import os 
import tempfile
from PIL import Image


CREATE_USER_URL = reverse('user:create')


#help funcs for creating user through API for testing
def create_user(**kwargs):
    return get_user_model().objects.create_user(**kwargs)

def create_user_default(email='test@example.com', password='testpassword123'):
    return get_user_model().objects.create_user(email, password)

def user_url(user_id):
    #genereate url for vewing user details
    return reverse('user:user-detail', args=[user_id])


def image_upload_url(user_id):
    #creating and return url for uploading image
    return reverse('user:user-upload-image', args=[user_id])


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


    def test_viewing_user_details(self):
        credentials = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'test',
        }

        user = create_user(**credentials)
        url = user_url(user.id)
        result = self.client.get(url)
        serializer = UserSerializer(user)

        self.assertEqual(result.data, serializer.data)


    @patch('api.models.uuid.uuid4')
    def test_user_file_name_uuid(self, mock_uuid):
        #testing generate image path
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.user_image_file_path(None, 'example.jpg')
        self.assertEquals(file_path, f"uploads\\user\\{uuid}.jpg")


class ImageUploadTests(TestCase):
    #test for image model
    def tear_down(self):
        self.user.image.delete()

    def test_upload_image(self):
        #testing uploading image for user
        credentials = {
                    'email': 'test@example.com',
                    'password': 'testpass123',
                    'name': 'test',
                }
        self.user = create_user(**credentials)

        url = image_upload_url(self.user.id)
        with tempfile.NamedTemporaryFile(suffix='.jpg') as image_file:
            img = Image.new('RGB', (10, 10))
            img.save(image_file, format='JPEG')
            image_file.seek(0)
            payload = {'image': image_file}
            result = self.client.post(url, payload, format='multipart')

        self.user.refresh_from_db()
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertIn('image', result.data)
        self.assertTrue(os.path.exists(self.user.image.path))

    def test_upload_image_bad_request(self):
        #testing invalid image
        credentials = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'test',
        }
        self.user = create_user(**credentials)

        url = image_upload_url(self.user.id)
        payload = {'image': 'notanimage'}
        result = self.client.post(url, payload, format='multipart')

        self.assertEqual(result.status_code, status.HTTP_400_BAD_REQUEST)


class TagsTests(TestCase): 
    #testing tag model
    def test_create_tag(self):
        #creating tags for exercise, checking succesfull
        tag = models.Tag.objects.create(name='test-tag')

        self.assertEqual(str(tag), tag.name)

