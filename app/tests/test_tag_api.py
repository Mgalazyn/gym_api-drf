from django.test import TestCase
from api import models
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from exercise.serializers import TagSerializer


TAGS_URL = reverse('exercise:tag-list')

#help funcs
def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)

def tag_url(tag_id):
    return reverse('exercise:tag-detail', args=[tag_id])


class TagModelAPITest(TestCase):
    #testing api requests for tags
    def setUp(self):
        self.user = create_user()
        self.client = APIClient()

    def test_retrive_tags(self):
        #testing retriving list of tags

        models.Tag.objects.create(user=self.user, name='chest')
        models.Tag.objects.create(user=self.user, name='back')

        result = self.client.get(TAGS_URL)

        tags = models.Tag.objects.all().order_by('-name')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)
    
    def test_tags_limited_to_user(self):
        #testing list of tags is limited to authenitacted user

        user2 = create_user(email='test@example.com', password='testpass123')
        models.Tag.objects.create(user=user2, name='shoulders')
        tag = models.Tag.objects.create(user=self.user, name='shoulders')
        
        result = self.client.get(TAGS_URL)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data[0]['name'], tag.name)

    def test_updating_tag(self):
        #testing updating tag
        tag = models.Tag.objects.create(user=self.user, name='chest')

        credentails = {'name': 'chest updated'}
        url = tag_url(tag.id)
        result = self.client.patch(url, data=credentails)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        tag.refresh_from_db()
        self.assertEqual(tag.name, credentails['name'])

    def test_deleting_tag(self):
        tag = models.Tag.objects.create(user=self.user, name='chest')
        url = tag_url(tag.id)
        result = self.client.delete(url)
    
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Tag.objects.filter(user=self.user).exists())

    