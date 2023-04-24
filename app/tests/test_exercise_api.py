from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from api.models import Exercise
from exercise.serializers import ExerciseSerializer, ExerciseDetailsSerializer



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

 
class ExerciseModelAPITests(TestCase):
    #testing exercise models
    def test_retrive_exercise_list(self):
        create_exercise()
        create_exercise()

        result = self.client.get('http://127.0.0.1:8000/api/exercise/exercises/')

        exercises = Exercise.objects.all()
        serializer = ExerciseSerializer(exercises, many=True)
        
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)


    # def test_get_exercise_details(self):
    #     exercise = create_exercise()
    #     url = f'http://127.0.0.1:8000/api/exercise/exercises/<str:{exercise.name}>'

    #     result = self.client.get(url)

    #     serializer = ExerciseDetailsSerializer(exercise)
    #     self.assertEqual(result.data, serializer.data)