from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient
from api import models
from plan.serializers import PlanSerializer, PlanDetailsSerializer


PLAN_URL = reverse('plan:plan-list')


#help funcs for testing
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
    exercise = models.Exercise.objects.create(**details)
    return exercise


def create_plan(**params):
    test_exercise1 = create_exercise()
    test_exercise2 = create_exercise()
    plan = models.Plan.objects.create(name='test plan')
    plan.exercises.add(test_exercise1, test_exercise2)
    return plan


def plan_url(plan_id):
    return reverse('plan:plan-detail', args=[plan_id])


class PlanModelAPITests(TestCase):
    def test_create_plan(self):
        #Creating plan 
        exercise1 = create_exercise()
        exercise2 = create_exercise()

        plan = models.Plan.objects.create(
            name='test plan'
        )
        plan.exercises.add(exercise1, exercise2)
        saved_plan = models.Plan.objects.get(pk=plan.pk)
        
        self.assertEqual(saved_plan.exercises.count(), 2)

    def test_retrive_plan_list(self):
        #creating tests for retriving list of plans
        create_plan()

        result = self.client.get(PLAN_URL)
        plans = models.Plan.objects.all()
        serializer = PlanSerializer(plans, many=True)
        
        self.assertEqual(result.status_code, status.HTTP_200_OK)
        self.assertEqual(result.data, serializer.data)

    def test_retrive_plan_details(self):
        #test for getting plan details
        plan = create_plan()
        url = plan_url(plan.id)
        result = self.client.get(url)
        serializer = PlanDetailsSerializer(plan)

        self.assertEqual(result.data, serializer.data)

    def test_delete_plan(self):
        #TESTING deleteing plan
        plan = create_plan()
        url = plan_url(plan.id)
        result = self.client.delete(url)

        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Plan.objects.filter(id=plan.id).exists())

    def test_updating_plan(self):
        #testing updating plan
        plan = models.Plan.objects.create(name='test plan1')

        credentials = {'name': 'test plan updated'}
        url = plan_url(plan.id)
        content_type = 'application/json'
        result = self.client.patch(url, data=credentials, content_type=content_type)

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        plan.refresh_from_db()
        self.assertEqual(plan.name, credentials['name'])

    def test_deleting_plan(self):
        #Testing deleting plan
        plan = models.Plan.objects.create(name='testplan1')
        url = plan_url(plan.id)
        result = self.client.delete(url)
        
        self.assertEqual(result.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(models.Plan.objects.filter(id=plan.id).exists())