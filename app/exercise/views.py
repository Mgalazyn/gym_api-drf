from django.shortcuts import render
from rest_framework.response import Response
from api.models import Exercise, Tag
from rest_framework import viewsets, mixins
from exercise import serializers


class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ExerciseDetailsSerializer
    queryset = Exercise.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ExerciseSerializer
        return self.serializer_class
    

class TagViewSet(mixins.UpdateModelMixin, 
                 mixins.DestroyModelMixin,
                 mixins.ListModelMixin, 
                 viewsets.GenericViewSet):
    serializer_class = serializers.TagSerializer
    queryset = Tag.objects.all()

    