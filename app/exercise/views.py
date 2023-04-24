from django.shortcuts import render
from api.models import Exercise
from api.permissions import AdminPermissions
from rest_framework import viewsets
from exercise.serializers import ExerciseSerializer, ExerciseDetailsSerializer


class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = ExerciseSerializer
    queryset = Exercise.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ExerciseSerializer
        return self.serializer_class