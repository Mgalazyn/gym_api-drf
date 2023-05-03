from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from api.models import Exercise, Tag
from exercise.serializers import ExerciseSerializer, ExerciseDetailsSerializer
from rest_framework.test import APIClient


EXERCISES_URL = reverse('exercise:exercise-list')

def create_exercise(**params):
    details = {
        'name': 'testexercise',
        'sets': 5,
        'reps': 5,
        'weight': '50kg',
        'description': 'just a test description to test....',
        'link': 'https://example.com/test_exercise',
    }
    details.update(params)
    exercise = Exercise.objects.create(**details)
    return exercise

 
def exercise_url(exercise_id):
    return reverse('exercise:exercise-detail', args=[exercise_id])


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a user."""
    return get_user_model().objects.create_user(email=email, password=password)


class ExerciseModelAPITests(TestCase):
    #testing exercise models


    def test_retrive_exercise_list(self):
        create_exercise()
        create_exercise()

        result = self.client.get(EXERCISES_URL)
        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)


    def test_exercise_details(self):
        #tessting  getting details about exercise
        exercise = create_exercise()
        url = exercise_url(exercise.id)
        result = self.client.get(url)
        serializer = ExerciseDetailsSerializer(exercise)

        self.assertEqual(result.data, serializer.data)

    def test_create_exercise(self):
        #testing creating exercise through api instead help funcs in tests
        credentials = {
            'name': 'test-exercise',
            'sets': 5,
            'reps': 5,
            'weight': '50test',
        }
        result = self.client.post(EXERCISES_URL, credentials)
        self.assertEqual(result.status_code, status.HTTP_201_CREATED)

    def test_partial_update_exercise(self):
        #testing partial update of exercise, with just required fields
        exercise = create_exercise()

        update_credentials = {
            'name': 'updated-test-exercise',
            'sets': 10,
            'reps': 10,
            'weight': 'new50test',
        }
        
        url = exercise_url(exercise.id)
        content_type = 'application/json'
        result = self.client.patch(url, data=update_credentials, content_type=content_type)
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        exercise.refresh_from_db()
        self.assertEqual(exercise.name, update_credentials['name'])
        self.assertEqual(exercise.sets, update_credentials['sets'])
        self.assertEqual(exercise.reps, update_credentials['reps'])
        self.assertEqual(exercise.weight, update_credentials['weight'])


    def test_delete_exercise(self):
        #TESTING deleteing exercise
        exercise = create_exercise()
        url = exercise_url(exercise.id)
        result = self.client.delete(url)

        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Exercise.objects.filter(id=exercise.id).exists())

    def test_creating_exercise_with_tags(self):
        #test creating exercise with tag

        payload = {
            'name': 'test-exercise',
            'sets': 5,
            'reps': 5,
            'weight': '50test',
            'tag': [{'name': 'chest'}]
        }

        result = self.client.post(EXERCISES_URL, payload, format='json')

        self.assertEqual(result.status_code, status.HTTP_201_CREATED)
        exercises = Exercise.objects.filter()
        self.assertEqual(exercises.count(), 1)
